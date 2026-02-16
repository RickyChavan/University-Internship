import pandas as pd

# -----------------------------
# File paths
# -----------------------------
csv_file = "v2_final_output_with_author_metrics.csv"
excel_file = "v2_final_output.xlsx"
output_file = "v2_updated_final_output.xlsx"

# -----------------------------
# Load files
# -----------------------------
df_csv = pd.read_csv(csv_file, dtype=str)
df_excel = pd.read_excel(excel_file, dtype=str)

# -----------------------------
# Clean full_names for matching
# -----------------------------
df_csv['full_names'] = df_csv['full_names'].str.strip().str.lower()
df_excel['full_names'] = df_excel['full_names'].str.strip().str.lower()

# -----------------------------
# Select required columns from CSV
# -----------------------------
df_csv_selected = df_csv[['full_names',
                           'h_index',
                           'i10_index',
                           'total_citations',
                           'orcid_id']]

# -----------------------------
# LEFT MERGE (keeps all Excel rows)
# -----------------------------
df_merged = df_excel.merge(
    df_csv_selected,
    on='full_names',
    how='left'
)

# -----------------------------
# Replace empty values in ranking columns with "NA"
# -----------------------------
ranking_columns = ['QS RANK 2024', 'REPEC RANKING']

for col in ranking_columns:
    if col in df_merged.columns:
        df_merged[col] = df_merged[col].fillna("NA")

# -----------------------------
# Save updated file
# -----------------------------
df_merged.to_excel(output_file, index=False)

print("✔ File updated successfully.")
print("✔ NA written in QS RANK 2024 and REPEC RANKING where empty.")