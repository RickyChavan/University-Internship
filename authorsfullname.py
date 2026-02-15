import pandas as pd

INPUT_EXCEL = "scopus_finlit.xlsx"
OUTPUT_CSV = "authors_only.csv"


# 1. Read Excel without headers
df_raw = pd.read_excel(INPUT_EXCEL, header=None)

# 2. Find header row containing 'Authors'
header_row = None
for i in range(len(df_raw)):
    if df_raw.iloc[i].astype(str).str.contains("Authors", case=False).any():
        header_row = i
        break

if header_row is None:
    raise ValueError("❌ Could not find 'Authors' column in Excel")

# 3. Promote that row to header
df = df_raw.copy()
df.columns = df.iloc[header_row]

# 4. Drop rows above header
df = df.drop(index=range(header_row + 1)).reset_index(drop=True)

# 5. Clean column names
df.columns = (
    df.columns
      .astype(str)
      .str.replace('"', '', regex=False)
      .str.strip()
)

print("Detected columns:", df.columns.tolist())

# 6. Extract Authors column and rename it
authors_df = df[["Author full names"]].rename(
    columns={"Author full names": "author_full_name"}
)

# 7. Save to CSV
authors_df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ Saved author full names to {OUTPUT_CSV}")
