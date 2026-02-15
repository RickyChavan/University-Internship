import pandas as pd

# =========================
# FILE PATHS
# =========================
INPUT_CSV = "v2_final_sorted_output.csv" 
OUTPUT_EXCEL = "v2_final_output.xlsx"

# =========================
# LOAD CSV
# =========================
df = pd.read_csv(
    INPUT_CSV,
    na_values=["NA", "N/A", "na", ""],
    keep_default_na=True
)
df.columns = df.columns.str.strip()

# =========================
# REQUIRED COLUMN ORDER
# =========================
column_order = [
    "EID",
    "Authors",
    "full_names",
    "Author_Position",
    "QS RANK 2024",
    "REPEC RANKING",
    "university",
    "Affiliations_cleaned",
    "country",
    "Title"
]

# Check if any columns are missing
missing_cols = [col for col in column_order if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in file: {missing_cols}")

# =========================
# WRITE "NA" FOR EMPTY RANK CELLS
# =========================
ranking_cols = ["QS RANK 2024", "REPEC RANKING"]

for col in ranking_cols:
    df[col] = df[col].fillna("NA")
    df[col] = df[col].replace("", "NA")


# Reorder columns
df = df[column_order]

# =========================
# SAVE AS EXCEL
# =========================
df.to_excel(OUTPUT_EXCEL, index=False)
print(df["QS RANK 2024"].unique()[:20])
print(df["REPEC RANKING"].unique()[:20])

print("✅ Excel file created successfully.")
print(f"📁 Saved as: {OUTPUT_EXCEL}")
