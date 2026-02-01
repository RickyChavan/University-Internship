import pandas as pd
import requests
import json
from tqdm import tqdm

# =========================
# CONFIG
# =========================
INPUT_CSV = "scopus_finlit_qs2024_repec_author_position.csv"
OUTPUT_CSV = "output_with_university.csv"
AFFILIATION_COL = "Affiliations"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:7b-instruct"

# =========================
# LLM CALL
# =========================
def extract_university(affiliation: str) -> str:
    prompt = f"""
Extract ONLY the university name from the affiliation below.

Rules:
- Return ONLY the university name
- If no university is present, return NA
- No explanations, no punctuation, no extra words

Affiliation:
{affiliation}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.0
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)

    if response.status_code != 200:
        return "NA"

    text = response.json().get("response", "").strip()
    return text if text else "NA"

# =========================
# MAIN PIPELINE
# =========================
def main():
    df = pd.read_csv(INPUT_CSV)

    # Cache to avoid repeated calls
    cache = {}

    universities = []

    for aff in tqdm(df[AFFILIATION_COL], desc="Extracting universities"):
        if pd.isna(aff):
            universities.append("NA")
            continue

        if aff in cache:
            universities.append(cache[aff])
            continue

        uni = extract_university(aff)
        cache[aff] = uni
        universities.append(uni)

    df["university"] = universities
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"✅ Done. Saved to {OUTPUT_CSV}")
    print(f"🧠 Unique LLM calls: {len(cache)}")

if __name__ == "__main__":
    main()
