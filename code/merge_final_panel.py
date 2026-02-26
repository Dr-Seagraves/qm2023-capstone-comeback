"""
Merge Processed Datasets into Final Analysis Panel
===================================================

This script:
  1. Loads cleaned REIT and FRED data from data/processed/
  2. Aligns temporal structures (monthly format)
  3. Merges on date with appropriate join logic
  4. Validates merge integrity (no unexpected row loss)
  5. Saves analysis-ready panel to data/final/

Output:
    - data/final/reit_fred_analysis_panel.csv

Panel structure: Long format (one row per REIT-month observation)
  Columns: date, ticker, return, market_cap, sector, fed_funds_rate, mortgage_rate, cpi, unemployment, ...

Author: Capstone Team
Date: 2026-02-26
"""

import pandas as pd
import numpy as np
from pathlib import Path
from config_paths import PROCESSED_DATA_DIR, FINAL_DATA_DIR

# ==============================================================================
# LOAD PROCESSED DATA
# ==============================================================================

def load_processed_data():
    """
    Load cleaned datasets from data/processed/.
    
    Returns:
        tuple: (reit_df, fred_df) or (None, None) if loading fails
    """
    print("\n" + "="*70)
    print("STEP 1: Loading Processed Datasets")
    print("="*70)
    
    # Load REIT data
    reit_file = PROCESSED_DATA_DIR / 'reit_data_clean.csv'
    if not reit_file.exists():
        print(f"⚠️  REIT data not found: {reit_file}")
        reit_df = None
    else:
        reit_df = pd.read_csv(reit_file)
        reit_df['date'] = pd.to_datetime(reit_df['date'])
        print(f"✓ REIT data: {len(reit_df)} rows, {len(reit_df.columns)} columns")
        print(f"   Date range: {reit_df['date'].min().date()} to {reit_df['date'].max().date()}")
        print(f"   Unique REITs: {reit_df['ticker'].nunique()}")
    
    # Load FRED data
    fred_file = PROCESSED_DATA_DIR / 'fred_data_clean.csv'
    if not fred_file.exists():
        print(f"⚠️  FRED data not found: {fred_file}")
        fred_df = None
    else:
        fred_df = pd.read_csv(fred_file)
        fred_df['date'] = pd.to_datetime(fred_df['date'])
        print(f"✓ FRED data: {len(fred_df)} rows, {len(fred_df.columns)} columns")
        print(f"   Date range: {fred_df['date'].min().date()} to {fred_df['date'].max().date()}")
    
    return reit_df, fred_df


def align_temporal_structure(reit_df, fred_df):
    """
    Ensure both datasets use consistent monthly frequency.
    
    Parameters:
        reit_df (pd.DataFrame): REIT data
        fred_df (pd.DataFrame): FRED data
        
    Returns:
        tuple: (reit_aligned, fred_aligned) - both in month-end format
    """
    print("\n" + "="*70)
    print("STEP 2: Align Temporal Structure (Month-End)")
    print("="*70)
    
    # REIT: assume monthly, normalize to month-end
    if reit_df is not None:
        reit_df['date'] = reit_df['date'].dt.to_period('M').dt.to_timestamp('M')
        print(f"✓ REIT data aligned to month-end")
    
    # FRED: already monthly, normalize to month-end
    if fred_df is not None:
        fred_df['date'] = fred_df['date'].dt.to_period('M').dt.to_timestamp('M')
        print(f"✓ FRED data aligned to month-end")
    
    return reit_df, fred_df


def merge_datasets(reit_df, fred_df):
    """
    Merge REIT and FRED data on date (many-to-one join).
    
    Each REIT has one return per month, but one FRED observation per month.
    Thus: left join REIT data with FRED data on date.
    
    Parameters:
        reit_df (pd.DataFrame): REIT returns data
        fred_df (pd.DataFrame): FRED macroeconomic data
        
    Returns:
        pd.DataFrame: Merged panel
    """
    print("\n" + "="*70)
    print("STEP 3: Merge Datasets")
    print("="*70)
    
    if reit_df is None or fred_df is None:
        print("⚠️  Cannot merge: missing data")
        return None
    
    initial_reit_rows = len(reit_df)
    
    # Merge on date (left join keeps all REIT observations)
    panel = pd.merge(
        reit_df,
        fred_df,
        on='date',
        how='left'
    )
    
    print(f"\n📊 Merge Summary:")
    print(f"   REIT observations (before): {initial_reit_rows}")
    print(f"   FRED observations: {len(fred_df)}")
    print(f"   Panel observations (after): {len(panel)}")
    
    # Check for data loss
    rows_lost = initial_reit_rows - len(panel)
    if rows_lost > 0:
        print(f"   ⚠️  Rows lost: {rows_lost}")
    else:
        print(f"   ✓ No data loss")
    
    return panel


def validate_merge_integrity(panel):
    """
    Validate merged panel for structural issues.
    
    Parameters:
        panel (pd.DataFrame): Merged panel
    """
    print("\n" + "="*70)
    print("STEP 4: Merge Integrity Validation")
    print("="*70)
    
    # Check no unexpected structure
    print(f"\n✓ Panel dimensions: {panel.shape[0]} rows × {panel.shape[1]} columns")
    
    # Check for missing values (expected for FRED lags)
    print(f"\n📋 Missing Values by Column:")
    missing = panel.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) > 0:
        for col, count in missing.items():
            pct = (count / len(panel)) * 100
            print(f"   • {col}: {count} ({pct:.1f}%)")
    else:
        print("   None")
    
    # Check time coverage
    date_min = panel['date'].min()
    date_max = panel['date'].max()
    print(f"\n📅 Date Coverage:")
    print(f"   Earliest: {date_min.date()}")
    print(f"   Latest:   {date_max.date()}")
    
    # Check entity coverage
    if 'ticker' in panel.columns:
        n_tickers = panel['ticker'].nunique()
        n_months = panel['date'].nunique()
        expected_obs = n_tickers * n_months
        actual_obs = len(panel)
        print(f"\n🏢 Entity Coverage:")
        print(f"   Unique REITs: {n_tickers}")
        print(f"   Months: {n_months}")
        print(f"   Expected observations (balanced): {expected_obs}")
        print(f"   Actual observations: {actual_obs}")
        print(f"   Imbalance: {expected_obs - actual_obs} obs")


def save_final_panel(panel, output_path):
    """
    Save final analysis-ready panel to CSV.
    
    Parameters:
        panel (pd.DataFrame): Final merged panel
        output_path (Path): Path to output file
    """
    print("\n" + "="*70)
    print("STEP 5: Saving Final Analysis Panel")
    print("="*70)
    
    # Sort by ticker and date for readability
    panel = panel.sort_values(['ticker', 'date']).reset_index(drop=True)
    
    panel.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    
    print(f"\n✓ Saved final panel: {output_path}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Rows: {len(panel)} (entity-months)")
    print(f"  Columns: {len(panel.columns)}")
    
    return panel


def create_data_summary(panel, output_path):
    """
    Create summary of key variables in final panel.
    
    Parameters:
        panel (pd.DataFrame): Final merged panel
        output_path (Path): Path to summary file
    """
    print("\n" + "="*70)
    print("STEP 6: Create Summary Statistics")
    print("="*70)
    
    summary_stats = panel.describe()
    summary_stats.to_csv(output_path)
    
    print(f"✓ Saved summary statistics to: {output_path}")


def main():
    """
    Execute full merge pipeline.
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "MERGE INTO FINAL ANALYSIS PANEL" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    
    # Load data
    reit_df, fred_df = load_processed_data()
    
    if reit_df is not None and fred_df is not None:
        # Align temporal structures
        reit_df, fred_df = align_temporal_structure(reit_df, fred_df)
        
        # Merge
        panel = merge_datasets(reit_df, fred_df)
        
        if panel is not None:
            # Validate
            validate_merge_integrity(panel)
            
            # Save final panel
            output_file = FINAL_DATA_DIR / 'reit_fred_analysis_panel.csv'
            panel = save_final_panel(panel, output_file)
            
            # Save summary statistics
            summary_file = FINAL_DATA_DIR / 'summary_statistics.csv'
            create_data_summary(panel, summary_file)
            
            print("\n" + "="*70)
            print("✅ MERGE PIPELINE COMPLETE!")
            print("="*70 + "\n")
    else:
        print("\n⚠️  Pipeline failed: missing source data.\n")


if __name__ == "__main__":
    main()
