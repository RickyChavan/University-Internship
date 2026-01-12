import pandas as pd

# 1. Load your paired CSV file
df = pd.read_csv("scopus_finlit_paired.csv")

# 2. Extract the country
# We split by comma and take the last part (-1)
# .str.strip() removes any accidental leading/trailing spaces
df['country'] = df['Affiliations'].str.split(',').str[-1].str.strip()

# 3. Save the updated file
df.to_csv("scopus_finlit_with_country.csv", index=False)

# Optional: Print the first few rows to verify
print(df[['Affiliations', 'country']].head())
