import pandas as pd

# 1. Load the Excel file, skipping the empty first row to find headers
input_file = "scopus_finlit.xlsx"
df = pd.read_excel(input_file, skiprows=1)

# Clean column names (remove quotes if they exist)
df.columns = [col.replace('"', '') for col in df.columns]

# 2. Select and keep the required columns
required_cols = ["EID", "Authors", "Affiliations", "Title", "Year"]
df = df[required_cols].dropna(subset=["Authors", "Affiliations"]).copy()

# 3. Process each row to pair authors and affiliations
expanded_data = []

for _, row in df.iterrows():
    # Split by semicolon and strip whitespace/quotes
    authors = [a.strip().strip('"') for a in str(row["Authors"]).split(";")]
    affiliations = [aff.strip().strip('"') for aff in str(row["Affiliations"]).split(";")]
    
    # Pair 1st author with 1st affiliation, 2nd with 2nd, etc.
    # zip stops at the end of the shorter list
    for auth, aff in zip(authors, affiliations):
        expanded_data.append({
            "EID": row["EID"],
            "Authors": auth,
            "Affiliations": aff,
            "Title": row["Title"],
            "Year": row["Year"]
        })

# 4. Create the new expanded DataFrame
df_expanded = pd.DataFrame(expanded_data)

# 5. Save the final result
output_file = "scopus_finlit_paired.csv"
df_expanded.to_csv(output_file, index=False)

print(f"Original records: {len(df)}")
print(f"Expanded author-affiliation pairs: {len(df_expanded)}")
