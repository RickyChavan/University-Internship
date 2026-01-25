import pandas as pd

INPUT_FILE = "scopus_finlit_qs_rank_2024_cleaned.csv"
OUTPUT_FILE = "scopus_finlit_qs_rank_2024_final.csv"

df = pd.read_csv(INPUT_FILE)

QS_RANK_COL = "qs_rank_2024"  # change if column name differs

# Convert empty strings to NA first
df[QS_RANK_COL] = df[QS_RANK_COL].replace("", pd.NA)

# Fill missing ranks explicitly with "NA"
df[QS_RANK_COL] = df[QS_RANK_COL].fillna("NA")

# Save output
df.to_csv(OUTPUT_FILE, index=False)

print("✅ NA restored explicitly in qs_rank_2024")
print("Total NA count:", (df[QS_RANK_COL] == "NA").sum())
