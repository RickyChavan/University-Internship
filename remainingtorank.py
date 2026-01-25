import pandas as pd

input_path = "scopus_finlit_with_qs2024.csv"
output_path = "scopus_finlit_without_qs_rank_2024.csv"

df = pd.read_csv(input_path)

# Rows where qs_rank_2024 is missing (NaN) or an empty/whitespace string
mask = df["qs_rank_2024"].isna() | (df["qs_rank_2024"].astype(str).str.strip() == "")

df_missing_qs = df.loc[mask].copy()
df_missing_qs.to_csv(output_path, index=False)

print("Saved:", output_path)
print("Original rows:", len(df))
print("Rows without qs_rank_2024:", len(df_missing_qs))
