import pandas as pd

df = pd.read_csv("scopus_finlit_paired.csv")[["EID","Authors","Affiliations"]].dropna()

df["n_auth"] = df["Authors"].astype(str).str.split(";").apply(len)
df["n_aff"]  = df["Affiliations"].astype(str).str.split(";").apply(len)

mismatch = df[df["n_auth"] != df["n_aff"]][["EID","n_auth","n_aff"]]

print("Rows with author/affiliation count mismatch:", len(mismatch))
mismatch.to_csv("author_affiliation_count_mismatches.csv", index=False)
