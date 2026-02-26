# Data Dictionary

## Dataset Overview
- **Entities (REITs):** 409
- **Observations (entity-months):** 47,529
- **Date range:** 1986-12-31 to 2024-12-31
- **Panel structure:** Long format (one row per REIT-month)

## Property Type Codes (ptype)

| Code | Property Type |
|---|---|
| 1 | Diversified |
| 2 | Lodging/Resorts |
| 3 | Self-Storage |
| 4 | Retail |
| 5 | Office |
| 8 | Residential |
| 9 | Industrial |
| 10 | Healthcare |

## Variables

| Variable | Description | Type | Source | Units/Notes |
|---|---|---|---|---|
| it permno | CRSP permanent security identifier | numeric | REIT Master Panel |  |
| ticker | Stock ticker symbol | string | REIT Master Panel |  |
| comnam | Company name | string | REIT Master Panel |  |
| rtype | REIT type code (2 = equity REIT) | numeric | REIT Master Panel |  |
| ptype | Property type code (see legend below) | numeric | REIT Master Panel |  |
| psub | Property subtype code | numeric | REIT Master Panel |  |
| date | Observation date (month-end) | date | REIT Master Panel | datetime |
| caldt | Calendar date | date | REIT Master Panel | datetime |
| ym | Year-month label (YYYYmMM) | string | REIT Master Panel | YYYYmMM |
| usdret | Monthly total return with dividends (decimal, e.g. 0.01 = 1%) | numeric | REIT Master Panel | decimal (e.g. 0.01 = 1%) |
| usdprc | Close price (USD) | numeric | REIT Master Panel | USD |
| market_equity | Market capitalization (millions USD) | numeric | REIT Master Panel | millions USD |
| assets | Total assets | numeric | REIT Master Panel | USD (millions) |
| sales | Sales / revenue | numeric | REIT Master Panel | USD (millions) |
| net_income | Net income | numeric | REIT Master Panel | millions USD |
| book_equity | Book equity | numeric | REIT Master Panel | USD (millions) |
| debt_at | Debt-to-assets ratio | numeric | REIT Master Panel | ratio/decimal |
| cash_at | Cash-to-assets ratio | numeric | REIT Master Panel | ratio/decimal |
| ocf_at | Operating cash flow to assets | numeric | REIT Master Panel | ratio/decimal |
| roe | Return on equity | numeric | REIT Master Panel | ratio/decimal |
| btm | Book-to-market ratio | numeric | REIT Master Panel | ratio/decimal |
| beta | Market beta | numeric | REIT Master Panel | ratio/decimal |
| FEDFUNDS | Federal funds effective rate (percent) | numeric | FRED | percent |
| MORTGAGE30US | 30-year fixed mortgage rate (percent) | numeric | FRED | percent |
| CPIAUCSL | Consumer Price Index for Urban Consumers (index) | numeric | FRED | index |
| UNRATE | Unemployment rate (percent) | numeric | FRED | percent |
| cpi_inflation_yoy | CPI year-over-year inflation rate (percent) | numeric | FRED | percent |
| FEDFUNDS_lag1 | Federal funds rate, 1-month lag (percent) | numeric | FRED | percent |
| FEDFUNDS_lag3 | Federal funds rate, 3-month lag (percent) | numeric | FRED | percent |

## Cleaning Decisions

1. **Missing critical keys:** Removed rows missing `ticker`, `date`, or `usdret`.
2. **Duplicates:** Dropped duplicate `ticker-date` observations (kept first occurrence).
3. **Outliers:** Filtered extreme returns (usdret > 5.0 or < -1.0), representing > 500% gains or < -100% losses.
4. **Date alignment:** Normalized all dates to month-end for consistent panel structure.
5. **FRED merge:** Left join on month-end date preserves all REIT observations.

## Data Sources

- **REIT Master Panel:** Course-provided dataset (CRSP + Compustat + Ziman Real Estate)
- **FRED Economic Data:** Federal Reserve Bank of St. Louis (via API/demo)

## Notes

- Missing values reflect incomplete financial reporting or data unavailability for certain REITs/periods.
- FRED variables have ~40% missing before 2005 due to panel starting in 1986 but FRED coverage starting 2004-2005.
- Property type and subtype codes follow Ziman Center conventions.