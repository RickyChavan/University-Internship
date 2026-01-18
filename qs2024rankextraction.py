import pandas as pd

# Define file names
input_file = '2024 QS World University Rankings 1.1 (For qs.com).csv'
output_file = 'extracted_qs_rankings2024.csv'

# Load the dataset
df = pd.read_csv(input_file)

# Skip the first row as it contains secondary headers/descriptions
df_clean = df.iloc[1:].copy()

# Select the target columns
columns_to_extract = ['2024 RANK', 'Institution Name', 'Country']
extracted_df = df_clean[columns_to_extract]

# Export to a new CSV file without the index
extracted_df.to_csv(output_file, index=False)

print(f"Extraction complete. Saved {len(extracted_df)} records to {output_file}.")

