import pandas as pd
from rapidfuzz import process, fuzz
from unidecode import unidecode

# ===============================
# FILE PATHS
# ===============================
SCOPUS_FILE = "scopus_finlit_without_qs_rank_2024.csv"
QS_FILE = "extracted_qs_rankings2024.csv"
OUTPUT_FILE = "scopus_finlit_with_qs_rank_2024.csv"

# ===============================
# COLUMN NAMES
# ===============================
AFFILIATION_COL = "Affiliations"
SCOPUS_COUNTRY_COL = "country"

QS_INST_COL = "Institution Name"
QS_COUNTRY_COL = "Country"
QS_RANK_COL = "2024 RANK"

FUZZY_THRESHOLD = 85

# ===============================
# LOAD DATA
# ===============================
scopus_df = pd.read_csv(SCOPUS_FILE)
qs_df = pd.read_csv(QS_FILE)

# ===============================
# NORMALIZATION HELPERS
# ===============================
def normalize(text):
    if pd.isna(text):
        return ""
    return unidecode(str(text).lower().strip())

def normalize_country(country):
    c = normalize(country)
    if c in {"china mainland", "china (mainland)", "mainland china"}:
        return "china"
    return c

# ===============================
# NORMALIZE COUNTRIES
# ===============================
scopus_df["norm_country"] = scopus_df[SCOPUS_COUNTRY_COL].apply(normalize_country)
qs_df["norm_country"] = qs_df[QS_COUNTRY_COL].apply(normalize_country)

qs_df["norm_inst"] = qs_df[QS_INST_COL].apply(normalize)

# ===============================
# SPLIT AFFILIATION (ONLY FIRST)
# ===============================
scopus_df["aff_part_1"] = (
    scopus_df[AFFILIATION_COL]
    .str.split(",", expand=True)[0]
    .str.strip()
)

# ===============================
# UNIVERSITY TRANSLATIONS
# ===============================
UNIVERSITY_VARIANTS = [
    "university", "universite", "universita",
    "universidad", "universitat", "universiteit",
    "universidade"
]

def expand_with_university(name):
    expanded = [name]
    for u in UNIVERSITY_VARIANTS:
        expanded.append(f"{u} {name}")
        expanded.append(f"{name} {u}")
    return expanded

# ===============================
# COUNTRY-FIRST FUZZY MATCH (LEVEL 1 ONLY)
# ===============================
def match_level_1(row):
    candidate = row["aff_part_1"]
    country = row["norm_country"]

    if not candidate or pd.isna(candidate):
        return pd.Series(["NA", "NONE", None, None])

    candidate = normalize(candidate)

    qs_subset = qs_df[qs_df["norm_country"] == country]
    if qs_subset.empty:
        return pd.Series(["NA", "NONE", None, None])

    inst_list = qs_subset["norm_inst"].tolist()
    rank_map = dict(zip(qs_subset["norm_inst"], qs_subset[QS_RANK_COL]))

    best_score = 0
    best_match = None

    for variant in expand_with_university(candidate):
        match, score, _ = process.extractOne(
            variant,
            inst_list,
            scorer=fuzz.token_set_ratio
        )
        if score > best_score:
            best_score = score
            best_match = match

    if best_score >= FUZZY_THRESHOLD:
        return pd.Series([
            rank_map.get(best_match),
            "aff_part_1",
            best_match,
            best_score
        ])

    return pd.Series(["NA", "NONE", None, best_score])

# ===============================
# APPLY MATCHING
# ===============================
scopus_df[
    ["QS_RANK_2024", "MATCH_LEVEL", "MATCHED_INSTITUTION", "FUZZY_SCORE"]
] = scopus_df.apply(match_level_1, axis=1)

# ===============================
# SAVE OUTPUT
# ===============================
scopus_df.to_csv(OUTPUT_FILE, index=False)

# ===============================
# SUMMARY
# ===============================
na_count = (scopus_df["QS_RANK_2024"] == "NA").sum()
total = len(scopus_df)

print("✅ Strict level-1 country-aware matching completed")
print(f"📊 Total rows: {total}")
print(f"❌ NA ranks: {na_count}")
print(f"✅ Matched: {total - na_count}")
print(f"📈 Match rate: {((total - na_count) / total) * 100:.2f}%")
