import pandas as pd
import requests
import time
import re
from rapidfuzz import fuzz

# =========================
# CONFIG
# =========================
API_KEY = "0gNGJzrC3W8SseitbXSQ5n"
INPUT_CSV = "output_with_qs_match.csv"
OUTPUT_CSV = "authors_with_orcid.csv"
MAILTO = "your_email@example.com"

OPENALEX_WORKS = "https://api.openalex.org/works"
DELAY = 0.4

TITLE_THRESHOLD = 85
NAME_THRESHOLD = 80
AFFIL_THRESHOLD = 80

# =========================
# SESSION
# =========================
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
})

retries = Retry(
    total=5,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

# =========================
# HELPERS
# =========================
def norm(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z ]", "", text)
    return text.strip()

def search_works(title):
    r = session.get(
        OPENALEX_WORKS,
        params={
            "search": title,
            "per-page": 5
        },
        timeout=30
    )
    if r.status_code == 200:
        return r.json()["results"]
    return []

# =========================
# MAIN
# =========================
df = pd.read_csv(INPUT_CSV)
results = []

for i, row in df.iterrows():
    title = row["Title"]
    affil = norm(row["Affiliations"])
    country = row["country"].upper()
    author_csv = norm(row["Authors"])

    print(f"[{i+1}/{len(df)}] {title[:70]}")

    works = search_works(title)
    time.sleep(DELAY)

    for work in works:
        title_score = fuzz.token_sort_ratio(norm(title), norm(work.get("title", "")))
        if title_score < TITLE_THRESHOLD:
            continue

        for auth in work.get("authorships", []):
            author = auth.get("author", {})
            author_name = norm(author.get("display_name", ""))

            name_score = fuzz.token_sort_ratio(author_csv, author_name)
            if name_score < NAME_THRESHOLD:
                continue

            for inst in auth.get("institutions", []):
                inst_name = norm(inst.get("display_name", ""))
                inst_country = inst.get("country_code")

                affil_score = fuzz.token_sort_ratio(affil, inst_name)

                if affil_score >= AFFIL_THRESHOLD and inst_country == country:
                    results.append({
                        "csv_title": title,
                        "csv_author": row["author"],
                        "matched_author": author.get("display_name"),
                        "institution": inst.get("display_name"),
                        "country": inst_country,
                        "orcid_url": author.get("orcid"),
                        "title_score": title_score,
                        "name_score": name_score,
                        "affil_score": affil_score
                    })

# =========================
# SAVE
# =========================
out = pd.DataFrame(results)
out.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved {len(out)} ORCID matches → {OUTPUT_CSV}")