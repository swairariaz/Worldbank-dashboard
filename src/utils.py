"""
Utility functions for the Streamlit dashboard.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import streamlit as st

@st.cache_data
def load_all_data() -> Dict[str, pd.DataFrame]:
    """
    Load all processed data with caching.
    """
    try:
        # Load main data with features
        main_data = pd.read_csv('data/processed/features/main_data.csv')
        
        # Load latest snapshot
        latest_snapshot = pd.read_csv('data/processed/features/latest_snapshot.csv')
        
        # Load world aggregates
        world_aggregates = pd.read_csv('data/processed/features/world_aggregates.csv')
        
        return {
            'main_data': main_data,
            'latest_snapshot': latest_snapshot,
            'world_aggregates': world_aggregates
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

def format_number(number: float, precision: int = 0) -> str:
    """
    Format numbers with appropriate suffixes and precision.
    """
    if pd.isna(number):
        return "N/A"
    
    if abs(number) >= 1_000_000_000:
        return f"{number / 1_000_000_000:.{precision}f}B"
    elif abs(number) >= 1_000_000:
        return f"{number / 1_000_000:.{precision}f}M"
    elif abs(number) >= 1_000:
        return f"{number / 1_000:.{precision}f}K"
    else:
        return f"{number:.{precision}f}"

def get_change_icon(change: float) -> str:
    """
    Get appropriate icon for value changes.
    """
    if pd.isna(change):
        return ""
    elif change > 0:
        return "▲"
    elif change < 0:
        return "▼"
    else:
        return "─"

def get_change_color(change: float) -> str:
    """
    Get appropriate color for value changes.
    """
    if pd.isna(change):
        return "gray"
    elif change > 0:
        return "green"
    elif change < 0:
        return "red"
    else:
        return "gray"

def get_change_class(change: float) -> str:
    """
    Get appropriate CSS class for value changes.
    """
    if pd.isna(change):
        return ""
    elif change > 0:
        return "positive-change"
    elif change < 0:
        return "negative-change"
    else:
        return ""

def filter_data(df: pd.DataFrame, countries: List[str], years: List[int]) -> pd.DataFrame:
    """
    Filter data based on selected countries and years.
    """
    filtered_df = df.copy()
    
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    
    if years:
        filtered_df = filtered_df[filtered_df['year'].between(min(years), max(years))]
    
    return filtered_df

def get_available_countries(df: pd.DataFrame) -> List[str]:
    """
    Get sorted list of available countries.
    """
    return sorted(df['country'].unique())

def get_available_years(df: pd.DataFrame) -> List[int]:
    """
    Get sorted list of available years.
    """
    return sorted(df['year'].unique())

def calculate_kpis(df: pd.DataFrame, current_year: int, previous_year: int) -> Dict[str, Any]:
    """
    Calculate KPIs for the current year with changes from previous year.
    These represent aggregate values across all selected countries.
    """
    current_data = df[df['year'] == current_year]
    previous_data = df[df['year'] == previous_year]
    
    kpis = {}
    
    # Median GDP per capita (across selected countries)
    current_median_gdp = current_data['gdp_pc_usd'].median()
    previous_median_gdp = previous_data['gdp_pc_usd'].median()
    kpis['median_gdp'] = {
        'value': current_median_gdp,
        'change': ((current_median_gdp - previous_median_gdp) / previous_median_gdp * 100) if previous_median_gdp and previous_median_gdp != 0 else 0,
        'formatted_value': f"${current_median_gdp:,.0f}",
        'formatted_change': f"{((current_median_gdp - previous_median_gdp) / previous_median_gdp * 100):.1f}%" if previous_median_gdp and previous_median_gdp != 0 else "N/A"
    }
    
    # Median Life Expectancy (across selected countries)
    current_median_life = current_data['life_expectancy_years'].median()
    previous_median_life = previous_data['life_expectancy_years'].median()
    kpis['median_life_expectancy'] = {
        'value': current_median_life,
        'change': current_median_life - previous_median_life if previous_median_life else 0,
        'formatted_value': f"{current_median_life:.1f} years",
        'formatted_change': f"{current_median_life - previous_median_life:+.1f} years" if previous_median_life else "N/A"
    }
    
    # Total Population (sum of selected countries)
    current_total_pop = current_data['population_total'].sum()
    previous_total_pop = previous_data['population_total'].sum()
    kpis['total_population'] = {
        'value': current_total_pop,
        'change': ((current_total_pop - previous_total_pop) / previous_total_pop * 100) if previous_total_pop and previous_total_pop != 0 else 0,
        'formatted_value': f"{format_number(current_total_pop)}",
        'formatted_change': f"{((current_total_pop - previous_total_pop) / previous_total_pop * 100):.1f}%" if previous_total_pop and previous_total_pop != 0 else "N/A"
    }
    
    # Mean Income Growth (average across selected countries)
    current_mean_income = current_data['ann_income_pc_growth_pct'].mean()
    previous_mean_income = previous_data['ann_income_pc_growth_pct'].mean()
    kpis['mean_income_growth'] = {
        'value': current_mean_income,
        'change': current_mean_income - previous_mean_income if previous_mean_income else 0,
        'formatted_value': f"{current_mean_income:.1f}%",
        'formatted_change': f"{current_mean_income - previous_mean_income:+.1f}%" if previous_mean_income else "N/A"
    }
    
    return kpis

def format_dataframe_numbers(df, columns):
    """
    Format numbers in a DataFrame for better display.
    """
    df_formatted = df.copy()
    
    for col in columns:
        if col in df_formatted.columns:
            if col == 'gdp_pc_usd':
                df_formatted[col] = df_formatted[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
            elif col == 'population_total':
                df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
            elif col in ['life_expectancy_years', 'ann_income_pc_growth_pct']:
                df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
    
    return df_formatted