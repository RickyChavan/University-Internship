import pandas as pd

input_file = "scopus_finlit_qs2024_repec_author_position.csv"
output_file = "scopus_finlit_qs2024_repec_author_position.xlsx"

# Load CSV (preserve NA)
df = pd.read_csv(input_file, keep_default_na=True)

# Desired column order
new_order = [
    "EID",
    "Authors",
    "Author_Position",
    "qs_rank_2024",
    "repec_rank",
    "Affiliations",
    "Year",
    "country",
    "Title"
]

# Reorder columns safely
df = df[new_order]

# Replace NaN with explicit "NA" so Excel shows it
df = df.fillna("NA")

# Save to Excel
df.to_excel(output_file, index=False)

print("Done. NA values preserved. File saved as:", output_file)