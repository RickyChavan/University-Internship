import pandas as pd
from rapidfuzz import process, fuzz
from unidecode import unidecode

# ============================
# FILE PATHS
# ============================
RANK_FILE = "repeccomplete.csv"
DATA_FILE = "scopus_finlit_qs_rank_2024_final.csv"
OUTPUT_FILE = "scopus_finlit_qs2024_repec.csv"

# ============================
# LOAD FILES
# ============================
rank_df = pd.read_csv(RANK_FILE)
data_df = pd.read_csv(DATA_FILE)

# ============================
# COLUMN NAMES
# ============================
INST_COL = "institution"
RANK_COL = "rank"
AFF_COL = "Affiliations"
QS_COL = "qs_rank_2024"   # column to fill NA

FUZZY_THRESHOLD = 85

# ============================
# NORMALIZE TEXT
# ============================
def normalize(text):
    if pd.isna(text):
        return ""
    return unidecode(str(text).lower().strip())

rank_df["norm_inst"] = rank_df[INST_COL].apply(normalize)
data_df["norm_aff"] = data_df[AFF_COL].apply(normalize)

inst_list = rank_df["norm_inst"].tolist()
rank_map = dict(zip(rank_df["norm_inst"], rank_df[RANK_COL]))

# ============================
# MATCH FUNCTION
# ============================
def match_rank(affiliation):
    if not affiliation:
        return "NA"

    match, score, _ = process.extractOne(
        affiliation,
        inst_list,
        scorer=fuzz.token_set_ratio
    )

    if score >= FUZZY_THRESHOLD:
        return rank_map.get(match)

    return "NA"

# ============================
# APPLY MATCHING
# ============================
data_df["repec_rank"] = data_df["norm_aff"].apply(match_rank)

# ============================
# FILL EMPTY QS_RANK_2024 WITH NA
# ============================
if QS_COL in data_df.columns:
    data_df[QS_COL] = data_df[QS_COL].replace("", pd.NA)
    data_df[QS_COL] = data_df[QS_COL].fillna("NA")
else:
    # Create column if missing
    data_df[QS_COL] = "NA"

# ============================
# COUNT MATCHES
# ============================
total_rows = len(data_df)
matched_count = (data_df["repec_rank"] != "NA").sum()
na_count = (data_df["repec_rank"] == "NA").sum()
match_rate = (matched_count / total_rows) * 100

print("✅ Matching complete")
print(f"📊 Total rows: {total_rows}")
print(f"✅ Matches found: {matched_count}")
print(f"❌ Not matched (NA): {na_count}")
print(f"📈 Match rate: {match_rate:.2f}%")

print("🧾 NA count in qs_rank_2024:", (data_df[QS_COL] == "NA").sum())

# ============================
# CLEAN & SAVE OUTPUT
# ============================
data_df.drop(columns=["norm_aff"], inplace=True)

data_df.to_csv(OUTPUT_FILE, index=False)

print("📄 Output saved to:", OUTPUT_FILE)
