import pandas as pd
import requests
import time

# =========================
# CONFIG
# =========================
INPUT_CSV = "sorted_by_university.csv"
OUTPUT_CSV = "sorted_by_university_filled.csv"

UNIVERSITY_COL = "university"
AFFILIATION_COL = "Affiliations_cleaned"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:7b-instruct"

NA_VALUES = ["NA", "N/A", "na", "n/a", "", "NULL", "null"]
DELAY = 0.4  # be polite to the model

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    INPUT_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)

df.columns = df.columns.str.strip()

# =========================
# LLM CALL
# =========================
def infer_university(affiliation):
    prompt = f"""
Extract the main university name from the affiliation text below.
Return ONLY the university name.
If no university is present, return NA.

Affiliation:
{affiliation}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["response"].strip()
    except Exception as e:
        print("LLM error:", e)

    return None

# =========================
# FILL MISSING UNIVERSITY
# =========================
for idx, row in df.iterrows():
    if pd.isna(row[UNIVERSITY_COL]) and pd.notna(row[AFFILIATION_COL]):
        print(f"[{idx}] Inferring university...")
        inferred = infer_university(row[AFFILIATION_COL])

        if inferred and inferred.upper() != "NA":
            df.at[idx, UNIVERSITY_COL] = inferred

        time.sleep(DELAY)

# =========================
# SORT A → Z (NA LAST)
# =========================
df_sorted = df.sort_values(
    by=UNIVERSITY_COL,
    ascending=True,
    na_position="last"
)

# =========================
# SAVE
# =========================
df_sorted.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ University filled (via Mistral) and sorted A–Z → {OUTPUT_CSV}")
