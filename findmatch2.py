import pandas as pd
import re

# =============================
# FILE PATHS
# =============================
QS_PATH = "extracted_qs_rankings2024.csv"
SCOPUS_PATH = "scopus_finlit_with_aff_split.csv"
OUTPUT_PATH = "scopus_finlit_with_qs_2024_rank2.csv"

# =============================
# LOAD FILES
# =============================
qs = pd.read_csv(QS_PATH)
scopus = pd.read_csv(SCOPUS_PATH)

# =============================
# NORMALIZATION FUNCTIONS
# =============================
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[.,;()\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_country(country):
    if pd.isna(country):
        return ""
    country = country.lower().strip()
    mapping = {
        "usa": "united states",
        "u s a": "united states",
        "uk": "united kingdom",
        "england": "united kingdom",
    }
    return mapping.get(country, country)

# =============================
# NORMALIZE QS DATA
# =============================
qs["country_norm"] = qs["Country"].apply(normalize_country)
qs["inst_norm"] = qs["Institution Name"].apply(normalize_text)
qs["rank_2024"] = qs["2024 RANK"]

# =============================
# NORMALIZE SCOPUS DATA
# =============================
scopus["country_norm"] = scopus["country"].apply(normalize_country)

# Use Affiliations OR Institution if available
if "Institution" in scopus.columns:
    scopus["affil_source"] = (
        scopus["Affiliations"].fillna("") + " " +
        scopus["Institution"].fillna("")
    )
else:
    scopus["affil_source"] = scopus["Affiliations"]

scopus["affil_norm"] = scopus["affil_source"].apply(normalize_text)

# =============================
# BUILD QS LOOKUP BY COUNTRY
# =============================
qs_by_country = {}
for country, group in qs.groupby("country_norm"):
    qs_by_country[country] = list(
        zip(group["inst_norm"], group["rank_2024"])
    )

# =============================
# MATCH FUNCTION
# =============================
def match_qs_rank(affil_norm, country_norm):
    if country_norm not in qs_by_country:
        return None

    for inst_name, rank in qs_by_country[country_norm]:
        if inst_name and inst_name in affil_norm:
            return rank

    return None

# =============================
# APPLY MATCHING
# =============================
scopus["2024 rank"] = scopus.apply(
    lambda row: match_qs_rank(
        row["affil_norm"],
        row["country_norm"]
    ),
    axis=1
)

# =============================
# SAVE OUTPUT
# =============================
scopus.drop(
    columns=["affil_norm", "affil_source", "country_norm"],
    errors="ignore"
).to_csv(OUTPUT_PATH, index=False)

print("✅ DONE")
print(f"📄 Output saved to: {OUTPUT_PATH}")
print(f"🎯 Matched rows: {scopus['2024 rank'].notna().sum()} / {len(scopus)}")
total_rows = len(scopus)
matched_rows = scopus["2024 rank"].notna().sum()
unmatched_rows = total_rows - matched_rows

print("\n📊 MATCHING SUMMARY")
print(f"Total rows: {total_rows}")
print(f"Rows with 2024 rank assigned: {matched_rows}")
print(f"Rows without 2024 rank: {unmatched_rows}")

if unmatched_rows == 0:
    print("✅ ALL rows have been successfully assigned a 2024 rank.")
else:
    print("⚠️ NOT all rows were assigned a 2024 rank.")
