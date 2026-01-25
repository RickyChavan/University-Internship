import pandas as pd
import pycountry
import re

# Load CSV
df = pd.read_csv("repecsplitcomplete.csv")

# Ranks to modify
target_ranks = ["Top 6%", "Top 7%", "Top 8%", "Top 9%", "Top 10%"]
mask = df["rank"].isin(target_ranks)

# Build full list of all countries
countries = sorted(
    {c.name for c in pycountry.countries},
    key=len,
    reverse=True  # longest first avoids partial match errors
)

country_pattern = "|".join(re.escape(c) for c in countries)

def split_after_country(text):
    if pd.isna(text):
        return text

    # Normalize non-breaking spaces
    text = text.replace("\xa0", " ").strip()

    # Insert split marker after country names
    text = re.sub(
        rf'\b({country_pattern})\b',
        r'\1|||SPLIT|||',
        text
    )

    # Split text into institutions
    parts = text.split("|||SPLIT|||")

    # Clean results
    cleaned = [p.strip() for p in parts if len(p.strip()) > 5]
    return cleaned


# Apply only to Top 6% → Top 10%
df.loc[mask, "institution"] = df.loc[mask, "institution"].apply(split_after_country)

# Explode into new rows
df_split = df[mask].explode("institution")
df_other = df[~mask]

# Clean whitespace
df_split["institution"] = df_split["institution"].str.strip()
df_split = df_split[df_split["institution"] != ""]

# Merge back without touching other rows
df_final = pd.concat([df_split, df_other]).sort_index()

# Save output
df_final.to_csv("repecsplitcomplete.csv", index=False)

print("✅ Done — rows split at every country name.")


df = pd.read_csv("repecsplitcomplete.csv", low_memory=False)
df.to_excel("repecsplitcomplete.xlsx", index=False, engine="openpyxl")