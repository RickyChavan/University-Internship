import pandas as pd

excel_file = "/Users/hrishikeshchavan/Desktop/ADREA_FAZIO_STAGE/repec rankings/croped2.xlsx"

# Load all sheets
all_sheets = pd.read_excel(excel_file, sheet_name=None)

merged_data = []

for sheet_name, df in all_sheets.items():
    # Normalize column names (lowercase, strip spaces)
    df.columns = df.columns.str.strip().str.lower()

    # Columns to remove (normalized)
    remove_cols = ["score", "author shares", "source_sheet"]

    # Drop if exists
    df = df.drop(columns=[col for col in remove_cols if col in df.columns], errors="ignore")

    merged_data.append(df)

# Merge all sheets into one dataframe
final_df = pd.concat(merged_data, ignore_index=True)

# Save final CSV
final_df.to_csv("repecranking.csv", index=False)

print("✅ Done! Saved as repecranking.csv")