import pandas as pd
import re
import requests
import json
from rapidfuzz import process, fuzz
from tqdm import tqdm

# ======================
# FILE PATHS
# ======================
SCOPUS_FILE = "scopus_finlit_qs2024_repec_author_position.csv"
QS_FILE = "extracted_qs_rankings2024.csv"
OUTPUT_FILE = "output_phi3_qs.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"
REQUEST_TIMEOUT = 60

# ======================
# LOAD DATA
# ======================
scopus = pd.read_csv(SCOPUS_FILE)
qs = pd.read_csv(QS_FILE)

# ======================
# NORMALIZE FUNCTION
# ======================
def normalize(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = text.replace("&", "and")
    text = re.sub(r"(department|faculty|school|centre|center|lab|institute).*?,", "", text)
    text = re.sub(r"[.,;]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ======================
# NORMALIZE QS DATA
# ======================
qs["inst_norm"] = qs["Institution Name"].apply(normalize)
qs_list = qs["inst_norm"].tolist()
qs_rank_map = dict(zip(qs["inst_norm"], qs["2024 RANK"]))

# ======================
# LLM CACHE (CRITICAL)
# ======================
llm_cache = {}

# ======================
# CALL PHI-3 MINI (SAFE)
# ======================
def phi3_extract_institution(affiliation):
    if affiliation in llm_cache:
        return llm_cache[affiliation]

    prompt = f"""
You are a data-cleaning function.

TASK:
Identify the most likely UNIVERSITY from the affiliation.

RULES:
- Respond ONLY in valid JSON
- NO explanations
- NO extra text
- NO markdown

FORMAT:
{{"institution": "<name or null>", "confidence": <0-100>}}

Affiliation: {affiliation}
"""

    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 60
                }
            },
            timeout=REQUEST_TIMEOUT
        )
        r.raise_for_status()
        response = json.loads(r.json()["response"])
        institution = response.get("institution")

    except Exception:
        institution = None

    llm_cache[affiliation] = institution
    return institution

# ======================
# MATCH TO QS (FAST)
# ======================
def match_qs(inst_name):
    if not inst_name:
        return None, 0

    inst_norm = normalize(inst_name)
    match = process.extractOne(
        inst_norm,
        qs_list,
        scorer=fuzz.token_set_ratio,
        score_cutoff=60
    )

    if match:
        return match[0], match[1]

    return None, 0

# ======================
# PROCESS ROWS
# ======================
results = []

for _, row in tqdm(scopus.iterrows(), total=len(scopus), desc="Processing"):
    affil = row["Affiliations"]

    extracted_inst = phi3_extract_institution(affil)
    matched_inst, score = match_qs(extracted_inst)

    qs_rank = qs_rank_map.get(matched_inst, "NA")

    # Confidence scoring
    if score >= 90:
        confidence = 0.95
    elif score >= 80:
        confidence = 0.85
    elif score >= 70:
        confidence = 0.65
    else:
        confidence = 0.40

    needs_review = confidence < 0.75

    results.append({
        **row,
        "phi3_institution": extracted_inst,
        "matched_institution": matched_inst,
        "qs_rank_2024_verified": qs_rank,
        "match_score": score,
        "confidence_score": confidence,
        "needs_manual_review": needs_review
    })

# ======================
# SAVE OUTPUT
# ======================
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

print("✅ DONE — Output saved to", OUTPUT_FILE)
print(f"🧠 LLM cache size: {len(llm_cache)} unique affiliations")
