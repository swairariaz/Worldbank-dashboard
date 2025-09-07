import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

def compute_ranks(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Compute GDP and population ranks for each country in a specific year.
    
    Args:
        df: Cleaned DataFrame
        year: Year to compute ranks for
        
    Returns:
        DataFrame with rank columns added
    """
    df_ranked = df.copy()
    
    # Filter data for the specific year
    year_data = df_ranked[df_ranked['year'] == year].copy()
    
    # Compute ranks
    year_data['gdp_pc_rank'] = year_data['gdp_pc_usd'].rank(ascending=False, method='min')
    year_data['population_rank'] = year_data['population_total'].rank(ascending=False, method='min')
    
    # Merge ranks back to the main dataframe
    rank_cols = ['country', 'iso_code', 'gdp_pc_rank', 'population_rank']
    df_ranked = df_ranked.merge(
        year_data[rank_cols], 
        on=['country', 'iso_code'], 
        how='left',
        suffixes=('', '_rank')
    )
    
    return df_ranked

def compute_rolling_averages(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """
    Compute rolling averages for specified columns.
    
    Args:
        df: Cleaned DataFrame
        window: Rolling window size
        
    Returns:
        DataFrame with rolling average columns added
    """
    df_rolling = df.copy()
    
    # Sort by country and year
    df_rolling = df_rolling.sort_values(['country', 'year'])
    
    # Compute rolling averages for each country
    rolling_cols = ['ann_income_pc_growth_pct']
    
    for col in rolling_cols:
        if col in df_rolling.columns:
            df_rolling[f'{col}_rolling_{window}yr'] = df_rolling.groupby('country')[col].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )
    
    return df_rolling

def create_latest_year_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a snapshot of the latest available year for each country.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with latest year data for each country
    """
    # Get the latest year for each country
    latest_years = df.groupby('country')['year'].max().reset_index()
    
    # Merge to get the latest data for each country
    latest_snapshot = pd.merge(
        latest_years, 
        df, 
        on=['country', 'year'], 
        how='left'
    )
    
    return latest_snapshot

def compute_world_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute world aggregates (population-weighted averages).
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with world aggregate metrics
    """
    world_agg = df.copy()
    
    # Group by year and compute weighted averages
    world_metrics = world_agg.groupby('year').apply(
        lambda x: pd.Series({
            'world_gdp_pc_weighted': np.average(x['gdp_pc_usd'], weights=x['population_total']),
            'world_life_expectancy_weighted': np.average(x['life_expectancy_years'], weights=x['population_total']),
            'world_income_growth_weighted': np.average(x['ann_income_pc_growth_pct'], weights=x['population_total']),
            'world_population_total': x['population_total'].sum()
        })
    ).reset_index()
    
    return world_metrics

def calculate_year_over_year_changes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate year-over-year changes for key metrics.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with YoY change columns
    """
    df_yoy = df.copy()
    
    # Sort by country and year
    df_yoy = df_yoy.sort_values(['country', 'year'])
    
    # Calculate YoY changes
    metrics = ['gdp_pc_usd', 'life_expectancy_years', 'population_total']
    
    for metric in metrics:
        if metric in df_yoy.columns:
            df_yoy[f'{metric}_yoy_pct'] = df_yoy.groupby('country')[metric].pct_change() * 100
    
    return df_yoy

def engineer_features(df: pd.DataFrame, reference_year: int = 2023) -> Dict[str, pd.DataFrame]:
    """
    Main function to engineer all features.
    
    Args:
        df: Cleaned DataFrame
        reference_year: Year to use for ranking calculations
        
    Returns:
        Dictionary with various feature DataFrames
    """
    logger.info("Engineering features...")
    
    # Compute ranks for the reference year
    df_with_ranks = compute_ranks(df, reference_year)
    
    # Compute rolling averages
    df_with_rolling = compute_rolling_averages(df_with_ranks)
    
    # Calculate YoY changes
    df_with_yoy = calculate_year_over_year_changes(df_with_rolling)
    
    # Create latest year snapshot
    latest_snapshot = create_latest_year_snapshot(df_with_yoy)
    
    # Compute world aggregates
    world_aggregates = compute_world_aggregates(df_with_yoy)
    
    # Create a dictionary of all feature DataFrames
    features = {
        'main_data': df_with_yoy,
        'latest_snapshot': latest_snapshot,
        'world_aggregates': world_aggregates
    }
    
    logger.info("Feature engineering completed!")
    return features

def save_features(features: Dict[str, pd.DataFrame], output_dir: str) -> None:
    """
    Save all feature DataFrames to CSV files.
    
    Args:
        features: Dictionary of feature DataFrames
        output_dir: Directory to save files
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for name, df in features.items():
        file_path = os.path.join(output_dir, f'{name}.csv')
        df.to_csv(file_path, index=False)
        logger.info(f"Saved {name} to {file_path}")

# Test function
if __name__ == "__main__":
    # Test the feature engineering
    try:
        from data_loader import load_and_transform_data
        
        print("Loading data...")
        df, mapping = load_and_transform_data('../data/path.csv', handle_missing=True)
        
        print("Engineering features...")
        features = engineer_features(df, reference_year=2023)
        
        print("✅ Feature engineering successful!")
        
        # Show main data info
        main_data = features['main_data']
        print(f"\nMain data shape: {main_data.shape}")
        print(f"New columns: {[col for col in main_data.columns if col not in df.columns]}")
        
        # Show latest snapshot
        latest = features['latest_snapshot']
        print(f"\nLatest snapshot shape: {latest.shape}")
        print(f"Latest year: {latest['year'].max()}")
        
        # Show world aggregates
        world = features['world_aggregates']
        print(f"\nWorld aggregates shape: {world.shape}")
        print("World aggregates sample:")
        print(world.head())
        
        # Save features
        save_features(features, '../data/processed/features')
        
        # Show sample of engineered data
        print("\nSample of engineered data (first 3 rows):")
        print(main_data.head(3)[['country', 'year', 'gdp_pc_rank', 'population_rank', 'ann_income_pc_growth_pct_rolling_3yr']])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()