import pandas as pd
from rapidfuzz import process, fuzz
from unidecode import unidecode

# ===============================
# FILE PATHS
# ===============================
INPUT_FILE = "scopus_finlit_with_qs2024.csv"
QS_FILE = "extracted_qs_rankings2024.csv"
OUTPUT_FILE = "scopus_finlit_qs_rank_2024_filled.csv"

# ===============================
# COLUMN NAMES
# ===============================
AFFILIATION_COL = "Affiliations"
SCOPUS_COUNTRY_COL = "country"

QS_RANK_COL = "qs_rank_2024"   # already exists in input file

QS_INST_COL = "Institution Name"
QS_COUNTRY_COL = "Country"
QS_QS_RANK_COL = "2024 RANK"

FUZZY_THRESHOLD = 85

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(INPUT_FILE)
qs_df = pd.read_csv(QS_FILE)

# ===============================
# NORMALIZATION
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

df["norm_country"] = df[SCOPUS_COUNTRY_COL].apply(normalize_country)
qs_df["norm_country"] = qs_df[QS_COUNTRY_COL].apply(normalize_country)

qs_df["norm_inst"] = qs_df[QS_INST_COL].apply(normalize)

# ===============================
# SPLIT FIRST AFFILIATION ONLY
# ===============================
df["aff_part_1"] = (
    df[AFFILIATION_COL]
    .str.split(",", expand=True)[0]
    .str.strip()
)

# ===============================
# UNIVERSITY VARIANTS
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
# STRICT LEVEL-1 MATCHING
# ===============================
def match_level_1(row):
    # Skip already-filled ranks
    if pd.notna(row["qs_rank_2024"]) and row["qs_rank_2024"] != "":
        return pd.Series([row["qs_rank_2024"], None, None, None])

    candidate = row.get("aff_part_1")
    country = row.get("norm_country")

    if not candidate or pd.isna(candidate):
        return pd.Series(["NA", "EMPTY_NAME", None, None])

    candidate_norm = normalize(candidate)

    # 🚨 Reject ultra-generic names
    GENERIC_WORDS = {"university", "college", "institute", "school"}
    tokens = set(candidate_norm.split())

    if len(tokens) <= 2 and tokens.issubset(GENERIC_WORDS):
        return pd.Series(["NA", "TOO_GENERIC", None, None])

    # Filter QS to same country ONLY
    qs_subset = qs_df[qs_df["norm_country"] == country]

    if qs_subset.empty:
        return pd.Series(["NA", "NO_COUNTRY_MATCH", None, None])

    inst_list = qs_subset["norm_inst"].tolist()
    rank_map = dict(zip(qs_subset["norm_inst"], qs_subset["2024 RANK"]))

    # Get top 5 matches
    matches = process.extract(
        candidate_norm,
        inst_list,
        scorer=fuzz.token_set_ratio,
        limit=5
    )

    if not matches:
        return pd.Series(["NA", "NO_MATCHES", None, None])

    best_match, best_score = matches[0][0], matches[0][1]

    # 🚨 HARD BLOCK: if similarity too low → NA
    if best_score < 90:
        return pd.Series(["NA", "LOW_CONFIDENCE", best_match, best_score])

    # 🚨 Extra safety: ensure name overlap exists
    overlap = set(candidate_norm.split()) & set(best_match.split())
    if len(overlap) == 0:
        return pd.Series(["NA", "NO_TOKEN_OVERLAP", best_match, best_score])

    return pd.Series([
        rank_map.get(best_match),
        "aff_part_1",
        best_match,
        best_score
    ])


# ===============================
# APPLY ONLY TO EMPTY QS RANKS
# ===============================
df[
    ["qs_rank_2024", "MATCH_LEVEL", "MATCHED_INSTITUTION", "FUZZY_SCORE"]
] = df.apply(match_level_1, axis=1)

# ===============================
# SAVE OUTPUT
# ===============================
df.to_csv(OUTPUT_FILE, index=False)

# ===============================
# SUMMARY
# ===============================
na_count = (df[QS_RANK_COL] == "NA").sum()
total = len(df)

print("✅ Incremental matching completed")
print(f"📊 Total rows: {total}")
print(f"❌ Still NA: {na_count}")
print(f"✅ Newly matched: {total - na_count}")
