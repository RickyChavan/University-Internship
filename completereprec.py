import pandas as pd

# ================================
# FILE PATHS
# ================================
CSV_INPUT = "repecranking.csv"
EXCEL_INPUT = "remainingrank.xlsx"
OUTPUT_FILE = "repeccomplete.csv"

# ================================
# LOAD CSV
# ================================
df = pd.read_csv(CSV_INPUT)

# ================================
# AUTO-DETECT RANK COLUMN
# ================================
rank_col = next(col for col in df.columns if "rank" in col.lower())

# ================================
# REMOVE % RANK ROWS
# ================================
REMOVE_RANKS = ["Top 6%", "Top 7%", "Top 8%", "Top 9%", "Top 10%"]
df = df[~df[rank_col].astype(str).isin(REMOVE_RANKS)]

# ================================
# DROP UNWANTED COLUMNS
# ================================
COLUMNS_TO_DROP = ["Score", "Authors", "Author"]
df = df.drop(columns=[c for c in COLUMNS_TO_DROP if c in df.columns])

# ================================
# LOAD NEW ROWS FROM EXCEL
# ================================
new_rows = pd.read_excel(EXCEL_INPUT)

# AUTO-DETECT Institution + Rank in Excel
excel_rank_col = next(col for col in new_rows.columns if "rank" in col.lower())
excel_inst_col = next(col for col in new_rows.columns if "institution" in col.lower())

new_rows = new_rows[[excel_rank_col, excel_inst_col]]
new_rows.columns = [rank_col, "Institution"]

# ================================
# APPEND NEW ROWS
# ================================
df_final = pd.concat([df, new_rows], ignore_index=True)

# ================================
# SAVE RESULT
# ================================
df_final.to_csv(OUTPUT_FILE, index=False)

print("✅ Rows cleaned")
print("✅ Rank column used:", rank_col)
print("✅ New rows appended")
print("📄 Output saved to:", OUTPUT_FILE)