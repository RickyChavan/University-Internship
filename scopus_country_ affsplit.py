import pandas as pd

# Load the data
input_file = "scopus_finlit_with_country.csv"
output_file = "scopus_finlit_with_aff_split.csv"

df = pd.read_csv(input_file)

# Safely split the Affiliations column on commas
aff_split = df["Affiliations"].fillna("").str.split(",", expand=True)

# First part: Affiliations (e.g., department or main unit)
df["Affiliations"] = aff_split[0].str.strip().replace("", pd.NA)

# Second part: Institution (e.g., university, college) if it exists
if aff_split.shape[1] > 1:
    df["Institution"] = aff_split[1].str.strip().replace("", pd.NA)
else:
    df["Institution"] = pd.NA

# Remaining parts combined into a single "other" column
if aff_split.shape[1] > 2:
    df["Affiliation_other"] = (
        aff_split.loc[:, 2:]
        .apply(lambda row: ", ".join(row.dropna().astype(str).str.strip()), axis=1)
        .replace("", pd.NA)
    )
else:
    df["Affiliation_other"] = pd.NA

# Save to a new CSV
df.to_csv(output_file, index=False)

print("Done. New file saved as:", output_file)
