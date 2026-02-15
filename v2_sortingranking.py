import pandas as pd

# =========================
# FILE PATHS
# =========================
QS_INPUT = "extracted_qs_rankings2024.csv"
QS_OUTPUT = "v2_qsranking_sorted.csv"

REPEC_INPUT = "repeccomplete.csv"
REPEC_OUTPUT = "v2_repec_ranking_sorted.csv"

# =========================
# 1️⃣ SORT QS FILE
# =========================
qs_df = pd.read_csv(QS_INPUT)
qs_df.columns = qs_df.columns.str.strip()

if "Institution Name" not in qs_df.columns:
    raise ValueError("Column 'Institution Name' not found in QS file")

qs_df = qs_df.sort_values(by="Institution Name", ascending=True)
qs_df.to_csv(QS_OUTPUT, index=False)

print("✅ QS ranking sorted and saved.")

# =========================
# 2️⃣ SORT REPEC FILE
# =========================
repec_df = pd.read_csv(REPEC_INPUT)
repec_df.columns = repec_df.columns.str.strip()

if "institution" not in repec_df.columns:
    raise ValueError("Column 'institution' not found in REPEC file")

repec_df = repec_df.sort_values(by="institution", ascending=True)
repec_df.to_csv(REPEC_OUTPUT, index=False)

print("✅ REPEC ranking sorted and saved.")
