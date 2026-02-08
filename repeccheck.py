import pandas as pd
from rapidfuzz import fuzz
from tqdm import tqdm

# =========================
# FILE PATHS
# =========================
FILE_1 = "output_with_qs_match.csv"
FILE_2 = "repeccomplete.csv"
OUTPUT_FILE = "output_with_repec_match.csv"

# =========================
# LOAD DATA
# =========================
df1 = pd.read_csv(FILE_1)
df2 = pd.read_csv(FILE_2)

# =========================
# NORMALIZATION
# =========================
def norm(x):
    return str(x).strip().lower()

df1["uni_norm"] = df1["university"].apply(norm)
df2["inst_norm"] = df2["institution"].apply(norm)

# =========================
# MATCH FUNCTION
# =========================
def match_repec(row):
    uni = row["uni_norm"]
    repec_rank_local = str(row["repec_rank"]).strip()

    best_score = 0
    best_row = None

    for _, r in df2.iterrows():
        score = fuzz.token_set_ratio(uni, r["inst_norm"])
        if score > best_score:
            best_score = score
            best_row = r

    if best_score < 80:
        return (
            "University not found",
            "NA",
            "NA",
            round(best_score * 0.4, 2)
        )

    repec_rank_global = str(best_row["rank"]).strip()

    # =========================
    # RANK MATCH LOGIC (FINAL)
    # =========================
    if repec_rank_local == repec_rank_global:
        rank_result = "Correctly rank matched"
        rank_score = 100
    else:
        rank_result = repec_rank_global
        rank_score = 70

    confidence_score = (
        best_score * 0.6 +
        rank_score * 0.3 +
        10   # match bonus
    )

    confidence_score = min(round(confidence_score, 2), 100)

    return (
        "University exists",
        rank_result,
        repec_rank_global,
        confidence_score
    )

# =========================
# APPLY MATCHING
# =========================
tqdm.pandas(desc="Matching RePEc institutions")

results = df1.progress_apply(
    match_repec,
    axis=1,
    result_type="expand"
)

df1[
    [
        "repec_university_match_status",
        "repec_rank_match_result",
        "repec_rank_matched",
        "repec_confidence_score"
    ]
] = results

# =========================
# CLEAN & SAVE
# =========================
df1.drop(columns=["uni_norm"], inplace=True)

df1.to_csv(OUTPUT_FILE, index=False)

print("✅ RePEc matching completed successfully")
print(f"📁 Output saved as: {OUTPUT_FILE}")