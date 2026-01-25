import pandas as pd

INPUT_FILE = "scopus_finlit_qs_rank_2024_filled.csv"
OUTPUT_FILE = "scopus_finlit_qs_rank_2024_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

# Columns to drop (DO NOT include qs_rank_2024)
COLUMNS_TO_DROP = [
    "affil_norm",
    "country_norm",
    "norm_country",
    "aff_part_1",
    "MATCHED_INSTITUTION",
    "MATCH_LEVEL",
    "FUZZY_SCORE"
]

# Drop only existing columns
df = df.drop(columns=[c for c in COLUMNS_TO_DROP if c in df.columns])

# Save cleaned output
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Cleaning completed")
print("Remaining columns:", df.columns.tolist())
print("NA count in qs_rank_2024:", df["qs_rank_2024"].isna().sum())
