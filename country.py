import pandas as pd

# Load file
df = pd.read_csv("scopus_finlit_paired.csv")

# 1. Extract full name (first two comma-separated parts)
df["full_names"] = (
    df["Affiliations"]
    .str.split(",", n=2)
    .str[:2]
    .str.join(", ")
    .str.strip()
)

# 2. Remove first two parts from Affiliations
df["Affiliations_cleaned"] = (
    df["Affiliations"]
    .str.split(",", n=2)
    .str[-1]
    .str.strip()
)

# 3. Extract country
df["country"] = (
    df["Affiliations_cleaned"]
    .str.split(",")
    .str[-1]
    .str.strip()
)

# 4. Drop original Affiliations column
df = df.drop(columns=["Affiliations"])

# Save
df.to_csv("scopus_finlit_with_country.csv", index=False)

# Verify
print(df.head())
