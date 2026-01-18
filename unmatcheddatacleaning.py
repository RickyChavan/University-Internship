import pandas as pd
import requests
import json
import re

# =============================
# CONFIG
# =============================
INPUT_PATH = "scopus_finlit_with_qs2024.csv"
OUTPUT_JSON = "mistral_affiliation_debug.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:instruct"

MAX_ROWS = 50  # inspect first N unmatched rows

# =============================
# LOAD DATA
# =============================
df = pd.read_csv(INPUT_PATH)
unmatched = df[df["qs_rank_2024"].isna()].head(MAX_ROWS)

# =============================
# PROMPT
# =============================
PROMPT = """
You are an information extraction system.

Task:
Extract the PRIMARY university or higher education institution name
from the affiliation text.

Rules:
- Ignore departments, faculties, labs, hospitals, NGOs, banks.
- If no university is clearly present, return null.
- Do NOT guess.
- Do NOT explain.
- Do NOT include extra text.

Return EXACTLY one JSON object and nothing else:
{"institution": string | null}
"""

# =============================
# JSON EXTRACTION
# =============================
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None

# =============================
# RUN DEBUG
# =============================
results = []

for _, row in unmatched.iterrows():
    affiliation = str(row["Affiliations"])
    eid = row.get("EID")

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{PROMPT}\n\nAffiliation:\n{affiliation}",
        "stream": False,
        "options": {"temperature": 0}
    }

    r = requests.post(OLLAMA_URL, json=payload)
    raw_response = r.json().get("response", "")

    parsed = extract_json(raw_response)

    results.append({
        "eid": eid,
        "affiliation": affiliation,
        "phi3_raw_response": raw_response,
        "phi3_parsed_json": parsed
    })

# =============================
# SAVE JSON
# =============================
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ JSON debug output saved to: {OUTPUT_JSON}")
