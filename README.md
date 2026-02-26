[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22872623&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
- **data/OpenData_rows** (1).csv - OpenData
- **data/raw/** — Original data (read-only)
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.

## Team
- Thang Pau and Claude Sonnet 4.5 making the comeback

## Research Question
How do REIT sector returns respond to Federal Reserve interest rate changes, and which property types are most sensitive?

## Datasets
- **REIT Master Panel** (course data): `data/raw/REIT_sample_2000_2024_All_Variables.csv`
  - 47,529 monthly observations from 409 REITs (1986-2024)
  - Includes returns, market equity, property types, financial ratios
- **FRED macroeconomic series**: Fed Funds Rate, 30-Year Mortgage Rate, CPI, Unemployment Rate
  - Fetched via API with 1-month and 3-month lags
  - Monthly frequency (2005-2024)

## Preliminary Hypotheses
- H1: 

## How to Run the Pipeline
1. Place raw REIT data in data/raw/REIT_sample_2000_2024_All_Variables.csv
2. Run `python code/fetch_reit_data.py`
3. Run `python code/fetch_fred_data.py`
4. Run `python code/merge_final_panel.py`

## Outputs
- Cleaned REIT data: data/processed/reit_data_clean.csv
- Cleaned FRED data: data/processed/fred_data_clean.csv
- Final panel: data/final/reit_fred_analysis_panel.csv
- Summary stats: data/final/summary_statistics.csv
- Summary report: results/reports/summary_statistics_report.md
