# Welfairies

This is a pipeline that takes as input a CSV of welfare notes and formats it as a printable PDF of A6 pages.

Submissions for the same person are automatically aggregated using fuzzy name matching, and pages are reordered for booklet printing (stack-of-pancakes order).

## Usage

Load the form response CSV to the `data` folder. Then update `parameters.py` to set the column names, term name, and Welsh phrase. To generate the welfairy PDF, run:
```
python3 generate.py data/form_responses.csv output/welfairies.pdf
```

You can also override the term name and Welsh phrase at the command line:
```
python3 generate.py data/form_responses.csv output/welfairies.pdf TT26 "Pwy ni chwardd pan fo hardd haf?"
```
