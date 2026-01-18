import pandas as pd
from rapidfuzz import process, fuzz
import re

# =============================
# PATHS
# =============================
QS_PATH = "extracted_qs_rankings2024.csv"
SCOPUS_PATH = "scopus_finlit_with_country.csv"
OUTPUT_PATH = "scopus_finlit_with_qs2024.csv"

# =============================
# LOAD
# =============================
qs = pd.read_csv(QS_PATH)
scopus = pd.read_csv(SCOPUS_PATH)

# =============================
# NORMALIZATION
# =============================
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()

    replacements = {
        "università": "university",
        "universitat": "university",
        "université": "university",
        "universidade": "university",
        "univ ": "university ",
        "univ.": "university",
        "&": "and",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(
        r"(department|faculty|school|institute|centre|center|lab|laboratory|unit|division).*?,",
        "",
        text,
    )

    return (
        text.replace(".", "")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("  ", " ")
            .strip()
    )

def normalize_country(c):
    if pd.isna(c):
        return ""
    c = c.lower().strip()
    return {
        "usa": "united states",
        "u s a": "united states",
        "uk": "united kingdom",
        "england": "united kingdom",
    }.get(c, c)

# =============================
# QS PREP
# =============================
qs["inst_norm"] = qs["Institution Name"].apply(normalize)
qs["country_norm"] = qs["Country"].apply(normalize_country)
qs["rank_clean"] = qs["2024 RANK"]

qs_by_country = {
    c: list(zip(g["inst_norm"], g["rank_clean"]))
    for c, g in qs.groupby("country_norm")
}

# =============================
# SCOPUS PREP
# =============================
scopus["affil_norm"] = scopus["Affiliations"].apply(normalize)
scopus["country_norm"] = scopus["country"].apply(normalize_country)

# =============================
# MATCH FUNCTION (STRONG)
# =============================
def match_qs_rank(affil, country):
    if not affil or country not in qs_by_country:
        return None

    qs_inst = qs_by_country[country]
    inst_names = [i[0] for i in qs_inst]

    # Split affiliation intelligently
    chunks = [c.strip() for c in re.split(r",|;", affil) if len(c.strip()) > 6]
    chunks.append(affil)  # also try full string

    best_score = 0
    best_rank = None

    for chunk in chunks:
        match = process.extractOne(
            chunk,
            inst_names,
            scorer=fuzz.token_set_ratio
        )
        if match and match[1] > best_score:
            best_score = match[1]
            for inst, rank in qs_inst:
                if inst == match[0]:
                    best_rank = rank

    return best_rank if best_score >= 72 else None

# =============================
# APPLY
# =============================
scopus["qs_rank_2024"] = scopus.apply(
    lambda r: match_qs_rank(r["affil_norm"], r["country_norm"]),
    axis=1
)

# =============================
# SAVE
# =============================
scopus.to_csv(OUTPUT_PATH, index=False)

print("✅ DONE")
print(f"Matched: {scopus['qs_rank_2024'].notna().sum()} / {len(scopus)}")
