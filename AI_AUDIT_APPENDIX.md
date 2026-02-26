# AI Audit Appendix

## Which AI tools you used
- Claude Sonnet 4.5

## Specific prompts or requests you made
- "Can you use these two files (I inserted the "REIT sample 2000-2024" and "REIT data dictionary") to create fetch scripts, for example, code/fetch_reit_data.py and code/fetch_fred_data.py. Then, create a merge script, code/merge_final_panel.py.

- Can you include a summary statistics file, which includes the before and after row counts. 

## What the AI produced
- Produced a file called "fetch_fred_data.py 3" and the script in it creates economic indicators from FRED for the analysis period 2004-2024.
- Produced a file called "fetch_reit_data.py 2" and the script in it loads the REIT Master Panel dataset (primary dataset), performs data quality checks, handles missing values, and saves the cleaned data to data/processed/.
- Produced a file called "merge_final_panel.py 2" and the script inside:
  1. Loads cleaned REIT and FRED data from data/processed/
  2. Aligns temporal structures (monthly format)
  3. Merges on date with appropriate join logic
  4. Validates merge integrity (no unexpected row loss)
  5. Saves analysis-ready panel to data/final/

- Produced a file called "summary_statistics_report.md" under data/results. It wrote out how many rows there were before the cleaning (48019). Then it wrote the row count after cleaning (47529). 

Then it created 7 tables.
- Table 1: it permno, rtype, ptype, psub
- Table 2: date, usdret, usdprc, market_equity
- Table 3: assets, sales, net_income, book_equity
- Table 4: debt_at, cash_at, ocf_at, roe
- Table 5: btm, beta, FEDFUNDS, MORTGAGE30US
- Table 6: CPIAUCSL, UNRATE, cpi_inflation_yoy, FEDFUNDS_lag1
- Table 7: FEDFUNDS_lag3

- I don't remember asking the AI to do these next two steps, but it must've just went through the assignment steps and it did them for me. It created the Final Dataset and called the file "reit_fred_analysis.csv". I can't even see what it has inside the file because the file is so large that it keeps freezing my laptop.
- It also created a Final Data Dictionary and called the file "data_dictionary.md". This file includes: 
   1. Dataset overview: 409 entities, 47,529 observations, 1986-2024 date range, long format
   2. Variable definitions table: All 27 variables with description, type, source, and units
   3. Cleaning decisions summary: 5 documented decisions (missing keys, duplicates, outliers, date alignment, FRED merge)