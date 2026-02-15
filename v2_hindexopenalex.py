import pandas as pd
import requests
import time
import os
import sys
from tqdm import tqdm

# =========================
# SETTINGS
# =========================
INPUT_CSV = "v2_final_sorted_output.csv"
OUTPUT_CSV = "v2_final_output_with_author_metrics.csv"
OPENALEX_API_KEY = "0gNGJzrC3W8SseitbXSQ5n"

# =========================
# LOAD OR RESUME
# =========================
if os.path.exists(OUTPUT_CSV):
    print("Resuming from saved file...")
    df = pd.read_csv(OUTPUT_CSV, dtype=str, keep_default_na=True)
else:
    print("Starting fresh...")
    df = pd.read_csv(INPUT_CSV, dtype=str, keep_default_na=True)
    df["h_index"] = pd.NA
    df["i10_index"] = pd.NA
    df["total_citations"] = pd.NA
    df["orcid_id"] = pd.NA

# =========================
# CACHES
# =========================
title_cache = {}
metrics_cache = {}

# =========================
# SAFE REQUEST (STOP ON 429)
# =========================
def safe_request(url, params=None):

    try:
        r = requests.get(url, params=params, timeout=20)

        if r.status_code == 200:
            return r

        elif r.status_code == 429:
            print("\n429 Rate Limit Hit.")
            print("Saving progress and exiting safely...")
            df.to_csv(OUTPUT_CSV, index=False)
            print("Progress saved.")
            sys.exit(0)

        else:
            print(f"Non-429 error: {r.status_code}")
            return None

    except Exception as e:
        print("Request error:", e)
        return None

# =========================
# GET AUTHOR ID
# =========================
def get_author_id(title, full_name):

    if title in title_cache:
        return title_cache[title]

    url = "https://api.openalex.org/works"
    params = {
        "search": title,
        "per-page": 5,
        "api_key": OPENALEX_API_KEY
    }

    response = safe_request(url, params=params)
    if not response:
        return None

    data = response.json()

    try:
        last, first = [x.strip() for x in full_name.split(",", 1)]
        formatted_name = f"{first} {last}".lower()
    except:
        formatted_name = full_name.lower()

    for work in data.get("results", []):
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            if author.get("display_name", "").lower() == formatted_name:
                title_cache[title] = author.get("id")
                return author.get("id")

    title_cache[title] = None
    return None

# =========================
# GET AUTHOR METRICS
# =========================
def get_author_metrics(author_id):

    if author_id in metrics_cache:
        return metrics_cache[author_id]

    if not author_id:
        return None

    short_id = author_id.split("/")[-1]

    url = f"https://api.openalex.org/authors/{short_id}"
    params = {"api_key": OPENALEX_API_KEY}

    response = safe_request(url, params=params)
    if not response:
        return None

    author = response.json()

    metrics = (
        author.get("summary_stats", {}).get("h_index"),
        author.get("summary_stats", {}).get("i10_index"),
        author.get("cited_by_count"),
        author.get("orcid")
    )

    metrics_cache[author_id] = metrics
    return metrics

# =========================
# MAIN LOOP
# =========================
for idx in tqdm(df.index, desc="Processing dataset"):

    # Resume logic
    if pd.notna(df.loc[idx, "h_index"]):
        continue

    title = df.loc[idx, "Title"]
    full_name = df.loc[idx, "full_names"]

    if pd.isna(title) or pd.isna(full_name):
        continue

    try:
        author_id = get_author_id(title, full_name)
        metrics = get_author_metrics(author_id)

        if metrics:
            df.loc[idx, "h_index"] = metrics[0]
            df.loc[idx, "i10_index"] = metrics[1]
            df.loc[idx, "total_citations"] = metrics[2]
            df.loc[idx, "orcid_id"] = metrics[3]

    except Exception as e:
        print(f"Row error at index {idx}:", e)
        df.to_csv(OUTPUT_CSV, index=False)
        print("Progress saved after error.")
        continue

    time.sleep(0.2)

# Final save
df.to_csv(OUTPUT_CSV, index=False)
print("\nAll rows processed successfully.")
