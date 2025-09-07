import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
import pycountry
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def standardize_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize country codes to ISO3 format using pycountry.
    
    Args:
        df: DataFrame with country names and codes
        
    Returns:
        DataFrame with standardized ISO3 codes
    """
    df_clean = df.copy()
    
    # Create a mapping for special cases
    special_mapping = {
        'European Union': 'EUU',  # EUU is the World Bank code for European Union
        'Korea, Rep.': 'KOR',
    }
    
    def get_iso3_code(country_name: str, current_code: str) -> str:
        # First check special cases
        if country_name in special_mapping:
            return special_mapping[country_name]
        
        # Try to find by current code first
        if current_code and len(current_code) == 3:
            try:
                country = pycountry.countries.get(alpha_3=current_code)
                if country:
                    return current_code
            except:
                pass
        
        # Try to find by name
        try:
            country = pycountry.countries.get(name=country_name)
            if country:
                return country.alpha_3
        except:
            pass
        
        # Try fuzzy matching by name
        try:
            country = pycountry.countries.search_fuzzy(country_name)
            if country:
                return country[0].alpha_3
        except:
            pass
        
        # If all else fails, return the original code
        return current_code if current_code and len(current_code) == 3 else None
    
    # Apply the standardization
    df_clean['iso_code'] = df_clean.apply(
        lambda row: get_iso3_code(row['country'], row['iso_code']), 
        axis=1
    )
    
    # Log any countries that couldn't be standardized
    invalid_countries = df_clean[df_clean['iso_code'].isna()]['country'].unique()
    if len(invalid_countries) > 0:
        logger.warning(f"Could not standardize codes for: {invalid_countries}")
    
    return df_clean

def handle_missing_data(df: pd.DataFrame, strategy: str = 'forward_fill') -> pd.DataFrame:
    """
    Handle missing data with specified strategy.
    
    Args:
        df: DataFrame with potential missing values
        strategy: 'forward_fill', 'interpolate', or 'leave_gaps'
        
    Returns:
        DataFrame with handled missing values
    """
    df_clean = df.copy()
    
    # Sort by country and year for proper handling
    df_clean = df_clean.sort_values(['country', 'year'])
    
    # Define which columns to handle with which strategy
    time_series_columns = ['ann_income_pc_growth_pct', 'gdp_pc_usd', 'life_expectancy_years']
    demographic_columns = ['population_total']
    
    # Group by country and apply missing data handling
    grouped = df_clean.groupby('country')
    
    if strategy == 'forward_fill':
        # For time series data, forward fill within each country
        for col in time_series_columns:
            df_clean[col] = grouped[col].transform(lambda x: x.ffill().bfill())
        
        # For demographic data, use interpolation
        for col in demographic_columns:
            df_clean[col] = grouped[col].transform(lambda x: x.interpolate())
    
    elif strategy == 'interpolate':
        # Use linear interpolation for all numeric columns
        for col in time_series_columns + demographic_columns:
            df_clean[col] = grouped[col].transform(lambda x: x.interpolate(limit_direction='both'))
    
    # For 'leave_gaps', we do nothing - leave missing values as is
    
    return df_clean

def validate_data(df: pd.DataFrame) -> Tuple[bool, pd.DataFrame]:
    """
    Validate the cleaned data for common issues.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        Tuple of (is_valid, validation_report)
    """
    validation_checks = []
    
    # Check for missing ISO codes
    missing_iso = df['iso_code'].isna().sum()
    validation_checks.append({
        'check': 'Missing ISO codes',
        'count': missing_iso,
        'status': 'PASS' if missing_iso == 0 else 'WARNING'
    })
    
    # Check for negative population
    negative_pop = (df['population_total'] < 0).sum()
    validation_checks.append({
        'check': 'Negative population values',
        'count': negative_pop,
        'status': 'PASS' if negative_pop == 0 else 'ERROR'
    })
    
    # Check for unrealistic life expectancy
    unrealistic_life = ((df['life_expectancy_years'] < 20) | (df['life_expectancy_years'] > 100)).sum()
    validation_checks.append({
        'check': 'Unrealistic life expectancy values',
        'count': unrealistic_life,
        'status': 'PASS' if unrealistic_life == 0 else 'ERROR'
    })
    
    # Check for missing values after handling
    missing_after = df.isnull().sum().sum()
    validation_checks.append({
        'check': 'Total missing values after handling',
        'count': missing_after,
        'status': 'PASS' if missing_after == 0 else 'WARNING'
    })
    
    # Create validation report
    validation_report = pd.DataFrame(validation_checks)
    is_valid = all(check['status'] in ['PASS', 'WARNING'] for check in validation_checks)
    
    return is_valid, validation_report

def load_and_transform_data(file_path: str, handle_missing: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    Load and transform World Bank data from wide to long format.
    
    Args:
        file_path: Path to the CSV file
        handle_missing: Whether to handle missing data
        
    Returns:
        Tuple of (transformed DataFrame, indicator mapping dictionary)
    """
    # Load the raw data
    df = pd.read_csv(file_path)
    
    # Remove any empty rows and columns
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Remove footer rows (non-data rows at the end)
    df = df[df['Country Name'].notna() & (df['Country Name'] != '')]
    
    # Identify year columns (those containing 'YR' or digits)
    year_columns = [col for col in df.columns if any(x in col for x in ['YR', '19', '20'])]
    
    # Melt the dataframe to convert from wide to long format
    id_vars = ['Country Name', 'Country Code', 'Series Name', 'Series Code']
    id_vars = [col for col in id_vars if col in df.columns]
    
    df_long = df.melt(
        id_vars=id_vars,
        value_vars=year_columns,
        var_name='year_str',
        value_name='value'
    )
    
    # Extract year from the year string (e.g., "2015 [YR2015]" -> 2015)
    df_long['year'] = df_long['year_str'].str.extract(r'(\d{4})').astype(int)
    
    # Drop the original year string column
    df_long = df_long.drop(columns=['year_str'])
    
    # Create indicator mapping
    indicator_mapping = {
        'NY.ADJ.NNTY.PC.KD.ZG': 'ann_income_pc_growth_pct',
        'SP.POP.TOTL': 'population_total', 
        'SP.DYN.LE00.IN': 'life_expectancy_years',
        'NY.GDP.PCAP.CD': 'gdp_pc_usd'
    }
    
    # Filter only the indicators we care about
    df_long = df_long[df_long['Series Code'].isin(indicator_mapping.keys())]
    
    # Pivot to get each indicator as a separate column
    df_pivoted = df_long.pivot_table(
        index=['Country Name', 'Country Code', 'year'],
        columns='Series Code',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    # Rename columns using the mapping
    df_pivoted = df_pivoted.rename(columns=indicator_mapping)
    
    # Clean up the column names and handle missing values
    df_clean = df_pivoted.copy()
    
    # Standardize column names
    df_clean = df_clean.rename(columns={
        'Country Name': 'country',
        'Country Code': 'iso_code'
    })
    
    # Convert data types
    numeric_columns = ['ann_income_pc_growth_pct', 'population_total', 
                      'life_expectancy_years', 'gdp_pc_usd']
    
    for col in numeric_columns:
        if col in df_clean.columns:
            # Convert to numeric, handling non-numeric values and '..' as NaN
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Standardize country codes
    df_clean = standardize_country_codes(df_clean)
    
    # Handle missing data if requested
    if handle_missing:
        df_clean = handle_missing_data(df_clean, strategy='forward_fill')
    
    # Drop rows where all indicator values are missing
    df_clean = df_clean.dropna(subset=numeric_columns, how='all')
    
    # Sort the data
    df_clean = df_clean.sort_values(['country', 'year'])
    
    # Reset index
    df_clean = df_clean.reset_index(drop=True)
    
    return df_clean, indicator_mapping

def get_missing_data_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate missing data statistics by column.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with missing data statistics
    """
    missing_stats = pd.DataFrame({
        'total_values': df.count(),
        'missing_values': df.isnull().sum(),
        'missing_pct': (df.isnull().sum() / len(df)) * 100
    })
    
    return missing_stats

def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save cleaned data to CSV file.
    
    Args:
        df: Cleaned DataFrame
        output_path: Path to save the cleaned CSV
    """
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved to {output_path}")

# Test function
if __name__ == "__main__":
    # Test the data loading
    try:
        print("Loading and transforming data...")
        df, mapping = load_and_transform_data('data/path.csv' , handle_missing=True)
        
        print(f"Data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Countries: {df['country'].unique()}")
        print(f"ISO Codes: {df['iso_code'].unique()}")
        print(f"Years: {sorted(df['year'].unique())}")
        
        # Show missing data stats
        missing_stats = get_missing_data_stats(df)
        print("\nMissing data statistics after cleaning:")
        print(missing_stats)
        
        # Validate data
        is_valid, validation_report = validate_data(df)
        print(f"\nData validation: {'PASS' if is_valid else 'FAIL'}")
        print("Validation report:")
        print(validation_report)
        
        # Save cleaned data
        save_cleaned_data(df, '../data/processed/worldbank_indicators_cleaned.csv')
        
        # Show first few rows
        print("\nFirst 5 rows of cleaned data:")
        print(df.head())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()