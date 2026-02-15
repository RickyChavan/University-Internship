import pandas as pd

# =========================
# CONFIG
# =========================
INPUT_FILE = "v2_main_with_qs_and_repec.csv"
OUTPUT_FILE = "v2_final_sorted_output.csv"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(INPUT_FILE)

# Clean column names (important)
df.columns = df.columns.str.strip()

# =========================
# 1️⃣ Fill NA in ranking columns
# =========================
ranking_cols = ["QS RANK 2024", "REPEC RANKING"]

for col in ranking_cols:
    if col in df.columns:
        df[col] = df[col].fillna("NA")
        df[col] = df[col].replace("", "NA")
    else:
        print(f"⚠ Column not found: {col}")

# =========================
# 2️⃣ Sort by University (A-Z)
# =========================
if "university" not in df.columns:
    raise ValueError("Column 'university' not found")

df["university"] = df["university"].fillna("NA")

# Sort alphabetically (A-Z)
df = df.sort_values(by="university", ascending=True, na_position="last")


# =========================
# SAVE FILE
# =========================
df.to_csv(OUTPUT_FILE, index=False)
df["QS RANK 2024"].value_counts().head()
df["REPEC RANKING"].value_counts().head()

print("✅ Done")
print(f"📁 Saved as: {OUTPUT_FILE}")
