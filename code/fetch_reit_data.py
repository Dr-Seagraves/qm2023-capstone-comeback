"""
Fetch and Clean REIT Master Panel Data
========================================

This script loads the REIT Master Panel dataset (primary dataset),
performs data quality checks, handles missing values, and saves
the cleaned data to data/processed/.

Output:
    - data/processed/reit_data_clean.csv

Author: Capstone Team
Date: 2026-02-26
"""

import pandas as pd
import numpy as np
from pathlib import Path
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Expected columns in raw REIT data (from REIT_sample_2000_2024_All_Variables.csv)
EXPECTED_COLUMNS = [
    'ticker', 'date', 'usdret', 'market_equity', 'ptype',
    'assets', 'sales', 'net_income', 'book_equity', 'debt_at'
]

# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def load_reit_data(file_path):
    """
    Load REIT Master Panel data from CSV.
    
    Parameters:
        file_path (Path): Path to raw REIT data file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    print("\n" + "="*70)
    print("STEP 1: Loading REIT Master Panel Data")
    print("="*70)
    
    if not file_path.exists():
        print(f"⚠️  WARNING: File not found at {file_path}")
        print("   Please ensure raw REIT data is in data/raw/")
        return None
    
    df = pd.read_csv(file_path)
    print(f"✓ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"  Columns: {list(df.columns)}")
    
    return df


def clean_reit_data(df):
    """
    Perform data quality checks and cleaning.
    
    Parameters:
        df (pd.DataFrame): Raw REIT data
        
    Returns:
        pd.DataFrame: Cleaned data
    """
    print("\n" + "="*70)
    print("STEP 2: Data Cleaning & Quality Checks")
    print("="*70)
    
    initial_rows = len(df)
    
    # Check for required columns
    print("\n📋 Column Check:")
    for col in df.columns:
        print(f"   • {col}")
    
    # Handle missing values
    print("\n🔍 Missing Values (before cleaning):")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("   No missing values detected")
    
    # Remove rows with missing critical values
    critical_cols = ['ticker', 'date', 'usdret']
    df = df.dropna(subset=critical_cols)
    
    print(f"\n✓ Rows removed for missing critical data: {initial_rows - len(df)}")
    
    # Ensure date is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        invalid_dates = df['date'].isnull().sum()
        if invalid_dates > 0:
            print(f"⚠️  Removed {invalid_dates} rows with invalid dates")
            df = df.dropna(subset=['date'])
    
    # Handle numeric columns
    numeric_cols = ['usdret', 'market_equity', 'assets', 'sales', 'net_income', 'book_equity', 'debt_at']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove outliers (return > 500% or < -100%)
    if 'usdret' in df.columns:
        # Note: returns are in decimal form (0.10 = 10%), outliers are those > 5.00 (500%) or < -1.00 (-100%)
        outliers = len(df[(df['usdret'] > 5.0) | (df['usdret'] < -1.0)])
        if outliers > 0:
            print(f"⚠️  Found {outliers} extreme return values (>500% or <-100%)")
            df = df[(df['usdret'] <= 5.0) & (df['usdret'] >= -1.0)]
    
    # Ensure ticker is string
    if 'ticker' in df.columns:
        df['ticker'] = df['ticker'].astype(str).str.upper()
    
    # Remove duplicates
    duplicates = len(df[df.duplicated(subset=['ticker', 'date'], keep='first')])
    if duplicates > 0:
        print(f"⚠️  Removed {duplicates} duplicate ticker-date observations")
        df = df.drop_duplicates(subset=['ticker', 'date'], keep='first')
    
    final_rows = len(df)
    print(f"\n✓ Final sample size: {final_rows} rows")
    print(f"  Total rows removed: {initial_rows - final_rows}")
    
    return df


def summarize_data(df):
    """
    Print summary statistics for cleaned data.
    
    Parameters:
        df (pd.DataFrame): Cleaned REIT data
    """
    print("\n" + "="*70)
    print("STEP 3: Summary Statistics")
    print("="*70)
    
    if df is None or len(df) == 0:
        print("⚠️  No data to summarize")
        return
    
    print(f"\n📊 Panel Dimensions:")
    print(f"   • Time periods: {df['date'].min()} to {df['date'].max()}")
    print(f"   • Unique REITs: {df['ticker'].nunique()}")
    print(f"   • Total observations: {len(df)}")
    
    if 'ptype' in df.columns:
        print(f"\n🏢 Property Type Distribution:")
        print(df['ptype'].value_counts())
    
    if 'usdret' in df.columns:
        print(f"\n💰 Return Statistics (decimal, e.g. 0.10 = 10%):")
        print(df['usdret'].describe())
    
    if 'market_equity' in df.columns:
        print(f"\n💵 Market Equity Statistics (millions $):")
        print(df['market_equity'].describe())


def save_cleaned_data(df, output_path):
    """
    Save cleaned data to CSV.
    
    Parameters:
        df (pd.DataFrame): Cleaned data
        output_path (Path): Path to save file
    """
    print("\n" + "="*70)
    print("STEP 4: Saving Cleaned Data")
    print("="*70)
    
    df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Saved to: {output_path}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")


def main():
    """
    Execute full REIT data fetch and cleaning pipeline.
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "REIT DATA FETCH & CLEAN PIPELINE" + " "*21 + "║")
    print("╚" + "="*68 + "╝")
    
    # Define paths
    raw_file = RAW_DATA_DIR / 'REIT_sample_2000_2024_All_Variables.csv'
    output_file = PROCESSED_DATA_DIR / 'reit_data_clean.csv'
    
    # Execute pipeline
    df = load_reit_data(raw_file)
    
    if df is not None:
        df = clean_reit_data(df)
        summarize_data(df)
        save_cleaned_data(df, output_file)
        
        print("\n" + "="*70)
        print("✅ REIT data pipeline complete!")
        print("="*70 + "\n")
    else:
        print("\n⚠️  Pipeline failed. Please check raw data file.\n")


if __name__ == "__main__":
    main()
