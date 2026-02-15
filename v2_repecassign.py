import pandas as pd
import re
from rapidfuzz import fuzz
from tqdm import tqdm

# =========================
# CONFIG
# =========================
MAIN_CSV = "main_with_qs_rank_2024.csv"
REPEC_CSV = "repeccomplete.csv"
OUTPUT_CSV = "v2_main_with_qs_and_repec.csv"

UNIV_COL = "university"
AFFIL_COL = "Affiliations_cleaned"

REPEC_UNIV_COL = "institution"
REPEC_RANK_COL = "rank"

FUZZY_THRESHOLD = 90

# =========================
# LOAD
# =========================
NA_VALUES = ["NA", "N/A", "na", "n/a", "NULL", "null", ""]
main_df = pd.read_csv(
    MAIN_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)
repec_df = pd.read_csv(
    REPEC_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)

main_df.columns = main_df.columns.str.strip()
repec_df.columns = repec_df.columns.str.strip()

# =========================
# NORMALIZATION (same as QS)
# =========================
def normalize(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(
        r"department.*|faculty.*|school.*|institute.*|college.*",
        "",
        text
    )
    text = re.sub(r"[^a-z ]", "", text)
    return text.strip()

main_df["norm_university"] = main_df[UNIV_COL].apply(normalize)
main_df["norm_affiliation"] = main_df[AFFIL_COL].apply(normalize)

repec_df["norm_university"] = repec_df[REPEC_UNIV_COL].apply(normalize)

# =========================
# REPEC LOOKUP FUNCTION
# =========================
def find_repec_rank(univ, affil):
    # Decide which text to use
    if not isinstance(univ, str) or "(" in univ or ")" in univ or univ.strip() == "":
        search_text = affil
    else:
        search_text = univ

    search_text = normalize(search_text)
    if not search_text:
        return "NA"

    best_score = 0
    best_rank = None

    for _, row in repec_df.iterrows():
        score = fuzz.token_sort_ratio(search_text, row["norm_university"])
        if score > best_score and score >= FUZZY_THRESHOLD:
            best_score = score
            best_rank = row[REPEC_RANK_COL]

    # Explicit fallback
    if best_rank is None:
        return "NA"

    return best_rank

# =========================
# APPLY WITH PROGRESS BAR
# =========================
tqdm.pandas(desc="Matching RePEc Ranking")

main_df["REPEC RANKING"] = main_df.progress_apply(
    lambda r: find_repec_rank(
        r[UNIV_COL],
        r[AFFIL_COL]
    ),
    axis=1
)

# =========================
# CLEANUP & SAVE
# =========================
main_df.drop(
    columns=["norm_university", "norm_affiliation"],
    inplace=True,
    errors="ignore"
)

main_df.to_csv(OUTPUT_CSV, index=False)

# =========================
# SUMMARY STATISTICS
# =========================
def print_summary(df, column_name):
    total = len(df)
    na_count = (df[column_name] == "NA").sum()
    assigned_count = total - na_count

    print(f"\n📊 {column_name}")
    print(f"  Total rows     : {total}")
    print(f"  Assigned values: {assigned_count}")
    print(f"  NA values      : {na_count}")
    print(f"  Coverage (%)   : {assigned_count / total * 100:.2f}%")

print_summary(main_df, "QS RANK 2024")
print_summary(main_df, "REPEC RANKING")

print(f"\n✅ RePEc ranking assigned and saved → {OUTPUT_CSV}")
