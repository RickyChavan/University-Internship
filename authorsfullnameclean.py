import pandas as pd
import re

INPUT_CSV = "authors_only.csv"
OUTPUT_CSV = "author_full_name_cleaned.csv"

# 1. Read CSV
df = pd.read_csv(INPUT_CSV)

# 2. Remove everything inside parentheses ()
df["author_full_name"] = df["author_full_name"].astype(str)
df["author_full_name"] = df["author_full_name"].str.replace(
    r"\(.*?\)", "", regex=True
)

# 3. Split authors by ';' into lists
df["author_full_name"] = df["author_full_name"].str.split(";")

# 4. Explode list → one author per row
df = df.explode("author_full_name")

# 5. Remove commas and extra spaces
df["author_full_name"] = (
    df["author_full_name"]
      .str.replace(",", "", regex=False)
      .str.strip()
)

# 6. Drop empty rows
df = df[df["author_full_name"] != ""]
df = df.dropna(subset=["author_full_name"])

# 7. Reset index
df = df.reset_index(drop=True)

# 8. Save result
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Cleaned author names saved to {OUTPUT_CSV}")
