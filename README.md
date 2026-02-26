[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22872623&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/OpenData_rows (1).csv - OpenData
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.

Option A: REIT Returns & Interest Rate Sensitivity (Default Track -- Pre-
Approved)
Research Question: How do REIT sector returns respond to Federal Reserve interest rate changes, and which
property types are most sensitive?
Datasets:
Dataset Source What It Provides
REIT Master Panel Course data (Data/) Monthly returns, market cap, sector for 500+ REITs (2004-
2024)
REIT Factor Library Course data (Data/) SIZE, VALUE, MOM, QLTY, LOWVOL, REV factor premiums
FRED Economic
Data
pandas-datareader
API
Fed Funds Rate, 30-Year Mortgage Rate, CPI,
Unemployment
Key Variables:
Outcome: Monthly REIT return (%)
Driver: Federal funds rate (lagged 1-2 months)
Controls: Market cap, momentum factor, quality factor
Groups: Property sector (Retail, Office, Industrial, Residential, Healthcare)
Why It's Interesting: REITs are ~60% debt-financed, so they're directly exposed to rate changes -- but the
effect varies dramatically by sector. Retail and Office REITs took a beating in 2022-2023 while Industrial
(warehouses, logistics) barely flinched. Your analysis quantifies this.
What Your Models Might Show:
Fixed effects regression: A 1 percentage point rate hike predicts a ~2.5% decline in REIT returns
Difference-in-differences: Rate-sensitive sectors (Retail/Office) underperformed resilient sectors
(Industrial) by ~3.5 pp after the 2022 hike cycle
VIF confirms low multicollinearity among controls
