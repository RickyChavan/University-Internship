📊 Scopus_with_ranking_author_matrics
Author-Level Dataset with Institutional Rankings and Bibliometric Metrics

This repository contains the full pipeline and final dataset generated for constructing a validated, enriched, and structured author-level dataset from Scopus bibliographic metadata.

The final dataset:

Scopus_with_ranking_author_matrics.csv

🎯 Project Objective

The goal of this project was to transform raw bibliographic metadata into a structured, research-ready dataset by integrating:

✅ QS World University Rankings (2024)

✅ RePEc Institutional Rankings

✅ Author position (First / Middle / Last)

✅ OpenAlex bibliometric metrics (h-index, i10-index, total citations)

✅ ORCID identifiers (where available)

✅ Cleaned institutional mapping

✅ Country information

The dataset supports institutional performance analysis, bibliometric studies, and author-level research evaluation.

🏗 Pipeline Overview

The project is structured into five major stages:

1️⃣ Data Cleaning & Institutional Normalization

Institution names across Scopus, QS, and RePEc datasets were inconsistent.

Normalization logic applied:

Convert to lowercase

Remove punctuation

Remove department-level terms (faculty, department, school, etc.)

Standardize abbreviations

Strip whitespace

Remove duplicate spacing

This ensures institutional matching occurs at the core entity level.

2️⃣ QS & RePEc Ranking Assignment
QS Ranking Matching

Fuzzy string matching used

Threshold = 85

If similarity ≥ 85 → Assign rank

Else → Assign NA

Why 85?

High precision threshold

Minimizes false positives

Logically reduces false negatives when language is consistent

RePEc Integration

Cleaned institutional names

Left join on normalized names

NA preserved for unmatched institutions

3️⃣ Author–Affiliation Structural Correction (1:n)

Corrected a major structural issue:

An author may have multiple affiliations (1:n relationship).

Fix implemented:

Proper row splitting

Preserve affiliation mapping per author

Prevent duplicate or overwritten assignments

Maintain author-level granularity

This significantly improved dataset integrity.

4️⃣ OpenAlex API Integration

For each author, the following metrics were retrieved:

h-index

i10-index

Total citation count

OpenAlex Author ID

ORCID ID (if available)

API Logic:

Query OpenAlex /authors endpoint

Parse JSON

Extract:

summary_stats.h_index

summary_stats.i10_index

cited_by_count

Store metrics

Handle null values and log errors

Error handling:

try/except blocks

Logging failed requests

Preserving NA values for missing authors

5️⃣ Manual Validation & Quality Assurance

Dataset size: 29,300 rows

Manually checked: 27,300 rows

Validation focus:

False positive QS matches

Institution similarity errors

Abbreviation mismatches

Ranking misassignments

All detected false positives were corrected.

False Negative Control

Given fuzzy threshold = 85, false negatives should be minimal when language is consistent.

However:

Random sampling of NA rows was performed

Any detected false negatives were corrected

This ensures high confidence in ranking assignments.

📁 Final Dataset
Scopus_with_ranking_author_matrics.csv
Contains:

Author full name

Cleaned institution

QS Rank 2024

RePEc Rank

Country

Author position

h-index

i10-index

Total citations

ORCID ID (where available)

OpenAlex Author ID

The dataset is:

Structurally consistent

Ranking validated

Bibliometrically enriched

Reproducible via modular Python scripts

🔍 Repository Structure

The repository includes:

Data cleaning scripts

Ranking assignment scripts

API integration scripts

Sorting and restructuring modules

Logging files

Intermediate outputs

Final v2 pipeline files

All scripts are modular and reproducible.

⚠ Known Limitations

Not all authors have ORCID IDs

ORCID employment data is incomplete for many profiles

Fuzzy matching assumes consistent language usage

Approximately 2,000 rows remain unchecked manually

🚧 Remaining Work

The remaining major task is:

Academic Seniority / Designation Retrieval

Planned methodology:

Use ORCID ID to query ORCID Public API

Extract employment role title

Normalize job titles

Map to structured career categories

Use bibliometric fallback when ORCID missing

This will further enrich the dataset with career-stage classification.

🧠 Key Achievements

Deterministic institutional normalization framework

Controlled fuzzy matching (threshold = 85)

Large-scale manual validation (27,300 rows)

Structural correction of 1:n author–affiliation mapping

OpenAlex bibliometric integration

Fully modular and reproducible Python pipeline

📌 Reproducibility

All processing steps are:

Script-based

Modular

Logged

Traceable

The dataset can be regenerated from raw metadata using the provided pipeline.

👤 Author

Hrishikesh (Ricky) Chavan
Building an Author-Level Dataset from Bibliographic Metadata
