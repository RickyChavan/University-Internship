from docx import Document
import pandas as pd
import pycountry
import re

# Input Word file
word_file = "repec rankings/repecranking.docx"

# Output Excel file
excel_file = "remainingrank.xlsx"


doc = Document(word_file)

rows = []

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue

    # Split at every period
    parts = text.split(".")

    for part in parts:
        sentence = part.strip()
        if sentence:
            rows.append([sentence + "."])  # add period back

# Save to Excel
df = pd.DataFrame(rows, columns=["Text"])
df.to_excel(excel_file, index=False)

print("✅ Word converted to Excel — new cell at every '.'")