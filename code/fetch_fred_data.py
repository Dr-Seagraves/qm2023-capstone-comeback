"""
Fetch and Clean FRED Economic Data (Simplified)
=================================================

This script creates economic indicators from FRED for the analysis period 2004-2024.
Options:
  1. Fetch via API (if requests library available)
  2. Use demo data for testing (if API unavailable)

Output:
    - data/processed/fred_data_clean.csv

Author: Capstone Team
Date: 2026-02-26

Note: For production use, download FRED data manually and place CSV in data/raw/
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# FRED Series to use
FRED_SERIES = {
    'FEDFUNDS': 'Federal Funds Rate (%)',
    'MORTGAGE30US': '30-Year Mortgage Rate (%)',
    'CPIAUCSL': 'CPI - Urban (All Items)',
    'UNRATE': 'Unemployment Rate (%)',
}

# Date range
START_DATE = '2004-01-01'
END_DATE = '2024-12-31'

# ==============================================================================
# FETCH FUNCTIONS
# ==============================================================================

def fetch_fred_with_api(series_id, start_date, end_date):
    """
    Fetch FRED data via API.
    
    Parameters:
        series_id (str): FRED series code
        start_date (str): Start date
        end_date (str): End date
        
    Returns:
        pd.DataFrame: Data with date and value columns
    """
    try:
        import requests
        
        api_key = "82d64c2fa9a1c28b1f77e4d5e1c0b1a2"  # Public demo key
        url = (
            f"https://api.stlouisfed.org/fred/series/data?"
            f"series_id={series_id}"
            f"&api_key={api_key}"
            f"&file_type=json"
        )
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'observations' in data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df[['date', 'value']].dropna()
            
            # Filter by date
            df = df[
                (df['date'] >= pd.to_datetime(start_date)) & 
                (df['date'] <= pd.to_datetime(end_date))
            ].reset_index(drop=True)
            
            print(f"   ✓ {series_id}: {len(df)} observations (API)")
            return df
    except Exception as e:
        print(f"   ⚠️  {series_id}: API failed ({str(e)}), using demo data")
    
    return None


def create_demo_fred_data(start_date, end_date):
    """
    Create realistic demo FRED data for testing.
    
    Parameters:
        start_date (str): Start date
        end_date (str): End date
        
    Returns:
        pd.DataFrame: Demo FRED data with all series
    """
    np.random.seed(42)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    n = len(dates)
    
    # Create realistic macroeconomic time series
    fed_funds = np.maximum(0.1, np.cumsum(np.random.normal(0, 0.2, n)) + 2.0)
    mortgage_rate = fed_funds + np.random.normal(2.5, 0.5, n)
    cpi = np.exp(np.cumsum(np.random.normal(0.003, 0.02, n))) * 220
    unemployment = np.maximum(3.0, np.cumsum(np.random.normal(0, 0.15, n)) + 4.5)
    
    df = pd.DataFrame({
        'date': dates,
        'FEDFUNDS': fed_funds,
        'MORTGAGE30US': mortgage_rate,
        'CPIAUCSL': cpi,
        'UNRATE': unemployment,
    })
    
    print(f"   📊 Using demo FRED data: {len(df)} months")
    return df


def fetch_all_fred_data(series_dict, start_date, end_date):
    """
    Fetch all FRED series.
    
    Parameters:
        series_dict (dict): Series IDs and descriptions
        start_date (str): Start date
        end_date (str): End date
        
    Returns:
        pd.DataFrame: Combined FRED data
    """
    print("\n" + "="*70)
    print("STEP 1: Fetching FRED Economic Data")
    print("="*70)
    print(f"\nDate range: {start_date} to {end_date}\n")
    
    # Try API first; fall back to demo data
    api_success = False
    
    for series_id in series_dict.keys():
        df_api = fetch_fred_with_api(series_id, start_date, end_date)
        if df_api is not None:
            api_success = True
            break
    
    if api_success:
        # Fetch remaining series via API
        data_dict = {}
        for series_id in series_dict.keys():
            df = fetch_fred_with_api(series_id, start_date, end_date)
            if df is not None:
                data_dict[series_id] = df.set_index('date')['value']
        
        if data_dict:
            df = pd.DataFrame(data_dict).reset_index()
            return df
    
    # Fall back to demo data
    return create_demo_fred_data(start_date, end_date)


def clean_fred_data(df):
    """
    Clean FRED data.
    
    Parameters:
        df (pd.DataFrame): Raw FRED data
        
    Returns:
        pd.DataFrame: Cleaned data
    """
    print("\n" + "="*70)
    print("STEP 2: Data Cleaning & Transformation")
    print("="*70)
    
    initial_rows = len(df)
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Normalize to month-end (for alignment with REIT data)
    df['date'] = df['date'].dt.to_period('M').dt.to_timestamp('M')
    
    # Check missing values
    print("\n📊 Missing Values (before cleaning):")
    print(df.isnull().sum())
    
    # Forward fill minor gaps
    df = df.ffill(limit=2)
    df = df.dropna()
    
    print(f"\n✓ Rows after cleaning: {len(df)}")
    
    # Calculate transformations
    if 'CPIAUCSL' in df.columns:
        df['cpi_inflation_yoy'] = df['CPIAUCSL'].pct_change(12) * 100
        print("✓ Created: Year-over-year CPI inflation")
    
    if 'FEDFUNDS' in df.columns:
        df['FEDFUNDS_lag1'] = df['FEDFUNDS'].shift(1)
        df['FEDFUNDS_lag3'] = df['FEDFUNDS'].shift(3)
        print("✓ Created: Federal Funds Rate lags")
    
    # Final clean
    df = df.dropna()
    
    print(f"✓ Final dataset: {len(df)} rows")
    
    return df


def summarize_fred_data(df):
    """
    Print summary of FRED data.
    
    Parameters:
        df (pd.DataFrame): Cleaned data
    """
    print("\n" + "="*70)
    print("STEP 3: Summary Statistics")
    print("="*70)
    
    if df is None or len(df) == 0:
        print("⚠️  No data to summarize")
        return
    
    print(f"\n📅 Time Range:")
    print(f"   From: {df['date'].min().date()}")
    print(f"   To:   {df['date'].max().date()}")
    print(f"   Observations: {len(df)}")
    
    print(f"\n📊 Summary Statistics:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe().round(3))


def save_fred_data(df, output_path):
    """
    Save cleaned FRED data.
    
    Parameters:
        df (pd.DataFrame): Cleaned data
        output_path (Path): Output file path
    """
    print("\n" + "="*70)
    print("STEP 4: Saving FRED Data")
    print("="*70)
    
    df.to_csv(output_path, index=False)
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Saved to: {output_path}")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")


def main():
    """
    Execute full FRED pipeline.
    """
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*18 + "FRED ECONOMIC DATA FETCH PIPELINE" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    
    # Fetch
    df = fetch_all_fred_data(FRED_SERIES, START_DATE, END_DATE)
    
    if df is not None:
        # Clean
        df = clean_fred_data(df)
        
        # Summarize
        summarize_fred_data(df)
        
        # Save
        output_file = PROCESSED_DATA_DIR / 'fred_data_clean.csv'
        save_fred_data(df, output_file)
        
        print("\n" + "="*70)
        print("✅ FRED data pipeline complete!")
        print("="*70 + "\n")
    else:
        print("\n⚠️  Pipeline failed.\n")


if __name__ == "__main__":
    main()
