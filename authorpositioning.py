import pandas as pd

input_file = "scopus_finlit_qs2024_repec.csv"
output_file = "scopus_finlit_qs2024_repec_author_position.csv"

# Read CSV without dropping NA
df = pd.read_csv(input_file, keep_default_na=True)

# Assign author position per Title WITHOUT removing rows
df["Author_Position"] = df.groupby("Title", dropna=False).cumcount() + 1

# Save while preserving NA formatting
df.to_csv(output_file, index=False, na_rep="NA")

print("Done. NA values preserved. Output saved to:", output_file)