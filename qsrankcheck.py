import pandas as pd
from rapidfuzz import fuzz
from tqdm import tqdm

# =========================
# FILE PATHS
# =========================
FILE_1 = "output_with_university.csv"
FILE_2 = "extracted_qs_rankings2024.csv"
OUTPUT_FILE = "output_with_qs_match.csv"

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
df1["country_norm"] = df1["country"].apply(norm)

df2["inst_norm"] = df2["Institution Name"].apply(norm)
df2["country_norm"] = df2["Country"].apply(norm)

# =========================
# MATCH FUNCTION
# =========================
def match_university(row):
    uni = row["uni_norm"]
    country = row["country_norm"]
    qs_rank = str(row["qs_rank_2024"]).strip()

    candidates = df2[df2["country_norm"] == country]

    if candidates.empty:
        return (
            "University not found",
            "NA",
            "NA",
            0
        )

    best_score = 0
    best_row = None

    for _, r in candidates.iterrows():
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

    qs_2024_rank = str(best_row["2024 RANK"]).strip()

    # =========================
    # RANK LOGIC (FINAL)
    # =========================
    if qs_rank == qs_2024_rank:
        rank_result = "Correctly rank matched"
        rank_score = 100
    else:
        rank_result = qs_2024_rank
        rank_score = 70

    confidence_score = (
        best_score * 0.6 +
        rank_score * 0.3 +
        10  # country exact match bonus
    )

    confidence_score = min(round(confidence_score, 2), 100)

    return (
        "University exists",
        rank_result,
        qs_2024_rank,
        confidence_score
    )

# =========================
# APPLY MATCHING
# =========================
tqdm.pandas(desc="Matching universities")

results = df1.progress_apply(
    match_university,
    axis=1,
    result_type="expand"
)

df1[
    [
        "university_match_status",
        "rank_match_result",
        "qs_2024_rank_matched",
        "confidence_score"
    ]
] = results

# =========================
# CLEAN & SAVE
# =========================
df1.drop(columns=["uni_norm", "country_norm"], inplace=True)

df1.to_csv(OUTPUT_FILE, index=False)

print("✅ Matching completed successfully")
print(f"📁 Output saved as: {OUTPUT_FILE}")
