Hello all here I have created a repository that is followable by anyone, where we are trying to build

"Building an Author-Level Dataset from Bibliographic Metadata"

instruction file: Instructions.pdf
Source file: scopus_finlit.xlsx

There are 2 seperate folders that have webscraping data in pdfs of both rankings

I have created seperate python files for each step.

finlit.py : cleans and restructure the data according to the instructions
country.py : to extract and make a new country column
missmatch.py : to check any mismatch in the data and stire it in author_affiliation_count_mismatches.csv
reprecpdftocsv.py : to scape the data from pdf of rep rankings from the folder into repecrankings.csv (code failed)


scopus_finlit_with_country.csv is the final file for now; 

next I'll upgrade it with the rankings. 

The project is still in progress.
