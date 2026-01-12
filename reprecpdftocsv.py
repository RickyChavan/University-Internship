import pdfplumber
import pandas as pd
import re

pdf_path = "/Users/hrishikeshchavan/Desktop/ADREA FAZIO STAGE/repec rankings/croped.pdf"
output_csv = "repecrankings.csv"

data = []
import logging
# This hides the internal PDF parsing warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
            
        # Regex to find: Rank (number), then Institution name (next line/text)
        # RePEc pattern usually has Rank on its own line followed by Institution
        lines = text.split('\n')
        for i, line in enumerate(lines):
            match = re.match(r'^(\d+)\s*$', line.strip())
            if match and i + 1 < len(lines):
                rank = match.group(1)
                institution = lines[i+1].strip()
                data.append({"Rank": rank, "Institution": institution})
            
            # Catch sub-units often marked with "---" (no numeric rank)
            elif "---" in line and i + 1 < len(lines):
                institution = lines[i+1].strip()
                data.append({"Rank": "NA", "Institution": institution})

# Create DataFrame and save
df = pd.DataFrame(data)
# Clean up potential duplicates or headers captured by mistake
df = df[~df['Institution'].str.contains('Rank Institution', na=False)]
df.to_csv(output_csv, index=False)

print(f"CSV created: {output_csv}")
