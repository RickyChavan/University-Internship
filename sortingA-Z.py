import pandas as pd

INPUT_CSV = "v2_output_with_university.csv"
OUTPUT_CSV = "sorted_by_university.csv"
UNIVERSITY_COLUMN = "university"

# Explicit NA handling
NA_VALUES = ["NA", "N/A", "na", "n/a", "NULL", "null", ""]

# Read CSV and force NA parsing
df = pd.read_csv(
    INPUT_CSV,
    na_values=NA_VALUES,
    keep_default_na=True
)

# Clean column names
df.columns = df.columns.str.strip()

print("Detected columns:", df.columns.tolist())

# Sort A → Z, NA at the end
df_sorted = df.sort_values(
    by=UNIVERSITY_COLUMN,
    ascending=True,
    na_position="last"
)

# Save result
df_sorted.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ Sorted with NA values handled correctly → {OUTPUT_CSV}")
