import pandas as pd
import requests
import re
import time
from rapidfuzz import fuzz

# =========================
# CONFIG
# =========================
INPUT_EXCEL = "scopus_finlit.xlsx"
OUTPUT_EXCEL = "authors_with_orcid_first100.xlsx"
AUTHOR_COLUMN = "Author_full_names"

MAILTO = "hrishichavan193@gmail.com"
OPENALEX_AUTHORS = "https://api.openalex.org/authors"

DELAY = 0.3
NAME_MATCH_THRESHOLD = 85
MAX_ROWS = 100   # <<< IMPORTANT

# =========================
# HELPERS
# =========================

df = pd.read_excel(INPUT_EXCEL, header=None)

# Promote first row to header
df.columns = df.iloc[0]

# Drop the header row from data
df = df.drop(index=0).reset_index(drop=True)

# Clean column names (remove quotes & spaces)
df.columns = (
    df.columns
      .astype(str)
      .str.replace('"', '', regex=False)
      .str.strip()
)

print("Detected columns:", df.columns.tolist())

def clean_author_string(text):
    if not isinstance(text, str):
        return []
    text = re.sub(r"\(.*?\)", "", text)  # remove brackets
    authors = [a.strip() for a in text.split(";") if a.strip()]
    return authors

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z ,]", "", text)
    return text.strip()

def to_surname_comma_name(name):
    if "," in name:
        return name.strip()
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[-1]}, {' '.join(parts[:-1])}"
    return name

def search_openalex_author(name):
    r = requests.get(
        OPENALEX_AUTHORS,
        params={
            "search": name,
            "per-page": 3,
            "mailto": MAILTO
        },
        timeout=30
    )
    if r.status_code == 200:
        return r.json()["results"]
    return []

# =========================
# MAIN
# =========================
df = pd.read_excel(INPUT_EXCEL).head(MAX_ROWS)

rows = []

for idx, row in df.iterrows():
    raw_authors = row[AUTHOR_COLUMN]
    authors = clean_author_string(raw_authors)

    print(f"[Row {idx+1}] Processing {len(authors)} authors")

    for author in authors:
        formatted = to_surname_comma_name(author)
        norm_author = normalize(formatted)

        matches = search_openalex_author(formatted)
        time.sleep(DELAY)

        best_orcid = None
        best_match_name = None
        best_score = 0

        for m in matches:
            oa_name = m.get("display_name", "")
            score = fuzz.token_sort_ratio(norm_author, normalize(oa_name))

            if score > best_score and score >= NAME_MATCH_THRESHOLD:
                best_score = score
                best_match_name = oa_name
                best_orcid = m.get("orcid")

        rows.append({
            "row_number": idx + 1,
            "original_author_string": author,
            "clean_author_name": formatted,
            "matched_openalex_name": best_match_name,
            "orcid_url": best_orcid,
            "match_score": best_score
        })

# =========================
# SAVE
# =========================
out = pd.DataFrame(rows)
out.to_excel(OUTPUT_EXCEL, index=False)

print(f"\n✅ Saved first 100-row results to {OUTPUT_EXCEL}")
