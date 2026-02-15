import pandas as pd
import requests
from tqdm import tqdm

# =========================
# CONFIG
# =========================
INPUT_CSV = "scopus_finlit_wc_authorposition.csv"
OUTPUT_CSV = "v2_output_with_university.csv"
AFFILIATION_COL = "Affiliations_cleaned"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:7b-instruct"   # switch to "phi3:mini" if you want faster

# =========================
# LLM CALL
# =========================
def extract_university(affiliation: str) -> str:
    prompt = f"""Extract ONLY the official university name.

Rules:
- Return ONLY the university/college name
- NO department, faculty, city, country
- NO explanations
- If no university is present, return exactly: NA

Text:
{affiliation}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.0
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return "NA"

        text = response.json().get("response", "").strip()

        # -------- HARD CLEANUP --------
        text = text.replace('"', '')
        text = text.replace("The university name is", "")
        text = text.replace("the university name is", "")
        text = text.strip()

        # remove country / city if model leaks it
        if "," in text:
            text = text.split(",")[0].strip()

        # reject explanations or garbage
        if len(text.split()) > 8:
            return "NA"

        return text if text else "NA"

    except Exception as e:
        print("❌ Ollama error:", e)
        return "NA"

# =========================
# MAIN PIPELINE
# =========================
def main():
    print("🚀 Script started (FULL DATASET)")

    df = pd.read_csv(INPUT_CSV)
    df.columns = df.columns.str.strip()

    if AFFILIATION_COL not in df.columns:
        raise ValueError(f"Column '{AFFILIATION_COL}' not found")

    print("🔥 Warming up model...")
    extract_university("University of Oxford, UK")

    cache = {}
    universities = []

    for aff in tqdm(df[AFFILIATION_COL], desc="Extracting universities"):
        if pd.isna(aff) or str(aff).strip() == "":
            universities.append("NA")
            continue

        aff = aff.strip()

        if aff in cache:
            universities.append(cache[aff])
            continue

        uni = extract_university(aff)
        cache[aff] = uni
        universities.append(uni)

    df["university"] = universities
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n✅ DONE")
    print(f"📁 Saved: {OUTPUT_CSV}")
    print(f"🧠 Unique LLM calls: {len(cache)}")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
