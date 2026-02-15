import pandas as pd
import re
from rapidfuzz import fuzz
from tqdm import tqdm

# =========================
# CONFIG
# =========================
MAIN_CSV = "sorted_by_university_filled.csv"
QS_CSV = "extracted_qs_rankings2024.csv"
OUTPUT_CSV = "main_with_qs_rank_2024.csv"

UNIV_COL = "university"
AFFIL_COL = "Affiliations_cleaned"
COUNTRY_COL = "country"

QS_UNIV_COL = "Institution Name"
QS_COUNTRY_COL = "Country"
QS_RANK_COL = "2024 RANK"

FUZZY_THRESHOLD = 85

# =========================
# LOAD
# =========================
NA_VALUES = ["NA", "N/A", "na", "n/a", "NULL", "null", ""]

main_df = pd.read_csv(
    MAIN_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)

qs_df = pd.read_csv(
    QS_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)


main_df.columns = main_df.columns.str.strip()
qs_df.columns = qs_df.columns.str.strip()

# =========================
# NORMALIZATION
# =========================
def normalize(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"department.*|faculty.*|school.*|institute.*", "", text)
    text = re.sub(r"[^a-z ]", "", text)
    return text.strip()

main_df["norm_university"] = main_df[UNIV_COL].apply(normalize)
main_df["norm_affiliation"] = main_df[AFFIL_COL].apply(normalize)

qs_df["norm_university"] = qs_df[QS_UNIV_COL].apply(normalize)
qs_df["norm_country"] = qs_df[QS_COUNTRY_COL].astype(str).str.upper()

# =========================
# QS LOOKUP FUNCTION
# =========================
def find_qs_rank(univ, affil, country):
    country = str(country).upper()

    # Decide which text to use
    if not isinstance(univ, str) or "(" in univ or ")" in univ or univ.strip() == "":
        search_text = affil
    else:
        search_text = univ

    search_text = normalize(search_text)
    if not search_text:
        return "NA"

    # Restrict search by country
    candidates = qs_df[qs_df["norm_country"] == country]

    best_score = 0
    best_rank = None

    for _, row in candidates.iterrows():
        score = fuzz.token_sort_ratio(search_text, row["norm_university"])
        if score > best_score and score >= FUZZY_THRESHOLD:
            best_score = score
            best_rank = row[QS_RANK_COL]

    # ✅ EXPLICIT fallback
    if best_rank is None:
        return "NA"

    return best_rank

# =========================
# APPLY MATCHING WITH PROGRESS BAR
# =========================
tqdm.pandas(desc="Matching QS Rank 2024")

main_df["QS RANK 2024"] = main_df.progress_apply(
    lambda r: find_qs_rank(
        r[UNIV_COL],
        r[AFFIL_COL],
        r[COUNTRY_COL]
    ),
    axis=1
)

# =========================
# CLEANUP & SAVE
# =========================
main_df.drop(columns=["norm_university", "norm_affiliation"], inplace=True)

main_df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ QS Rank 2024 added. Output saved to {OUTPUT_CSV}")
