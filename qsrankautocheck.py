import pandas as pd
from rapidfuzz import fuzz
import re

# Load files
final_file = "scopus_finlit_qs2024_repec_author_position.csv"
qs_file = "extracted_qs_rankings2024.csv"

final_df = pd.read_csv(final_file, keep_default_na=True)
qs_df = pd.read_csv(qs_file, keep_default_na=True)

# Normalize QS fields
qs_df["Institution Name"] = qs_df["Institution Name"].fillna("").str.lower().str.strip()
qs_df["Country"] = qs_df["Country"].fillna("").str.lower().str.strip()

qs_records = qs_df[["Institution Name", "Country"]].to_dict("records")

def exact_university_country_match(affiliation):
    if pd.isna(affiliation):
        return False
    
    aff = affiliation.lower()
    
    for rec in qs_records:
        uni = rec["Institution Name"]
        country = rec["Country"]
        
        if uni and country:
            # Exact phrase match for university
            uni_pattern = r"\b" + re.escape(uni) + r"\b"
            uni_match = re.search(uni_pattern, aff)
            
            # Country exact word match
            country_pattern = r"\b" + re.escape(country) + r"\b"
            country_match = re.search(country_pattern, aff)
            
            if uni_match and country_match:
                return True
    
    return False

# Apply match
final_df["QS_Exact_Match"] = final_df["Affiliations"].apply(exact_university_country_match)

# Save output
final_df.to_csv("final_with_qs_match.csv", index=False, na_rep="NA")

print("Done. Output saved as final_with_qs_match.csv")
