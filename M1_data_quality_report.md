# M1 Data Quality Report

## Data Sources
- REIT Master Panel (course-provided).
- FRED macroeconomic series: Fed funds rate, mortgage rate, CPI, unemployment.

## Cleaning Decisions
- Dropped rows missing critical keys (ticker, date, usdret).
- Removed duplicate ticker-date observations.
- Filtered extreme return outliers (usdret > 5.0 or < -1.0).
- Converted dates to month-end for consistent panel alignment.

## Row Counts
| Dataset | Rows |
|---|---|
| REIT raw | 48019 |
| REIT cleaned | 47529 |
| FRED cleaned | 240 |
| Final panel | 47529 |

## Merge Strategy
- Left join REIT panel to monthly FRED series on date (month-end).
- Preserves all REIT observations; macro values are matched by month.

## Final Dataset Summary
- Observations: 47529
- Unique REITs: 409
- Date range: 1986-12-31 to 2024-12-31

## Reproducibility Checklist
- Scripts use paths via config_paths.py.
- Each fetch script prints row counts and summary stats.
- Merge script validates dimensions.

## Ethical Considerations
- Missing values and outlier filtering can drop stressed or thinly traded REITs; review for bias.
- Macro data alignment assumes monthly timing; sensitivity to lags should be tested.