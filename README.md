# Welfairies

This is a pipeline that takes as input a csv with notes for people and formats it as a pdf of A6 pages.

## Usage

Load the form response csv to the data folder. Then update `parameters.py` to match the form questions. To generate the welfairy pdf, call:
```
python3 -m generate data/form_responses.csv output/welfairies.pdf
```