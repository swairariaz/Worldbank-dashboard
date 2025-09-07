"""
Forecasting functions for the Streamlit dashboard.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
warnings.filterwarnings('ignore')

def prepare_forecast_data(main_data, country, indicator, min_data_points=5):
    """
    Prepare data for forecasting by selecting a country and an indicator,
    and returning a clean time series with no missing values.
    """
    # Filter data for the selected country and indicator
    country_data = main_data[main_data['country'] == country]
    
    if country_data.empty:
        return None
    
    # Create a time series for the selected indicator
    ts_data = country_data[['year', indicator]].dropna()
    
    # Check if we have enough data points
    if len(ts_data) < min_data_points:
        return None
    
    # Set year as index and sort
    ts_data = ts_data.set_index('year').sort_index()
    
    return ts_data

def linear_regression_forecast(ts_data, forecast_years=5):
    """
    Perform linear regression forecast.
    """
    # Prepare data for regression
    X = np.array(ts_data.index.values).reshape(-1, 1)
    y = ts_data.values
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future years for prediction
    last_year = ts_data.index.max()
    future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
    
    # Predict future values
    future_predictions = model.predict(future_years)
    
    # Create result DataFrame
    historical = pd.DataFrame({
        'year': ts_data.index,
        'value': ts_data.values.flatten(),
        'type': 'Historical'
    })
    
    forecast = pd.DataFrame({
        'year': future_years.flatten(),
        'value': future_predictions.flatten(),
        'type': 'Forecast'
    })
    
    return pd.concat([historical, forecast], ignore_index=True)

def exponential_smoothing_forecast(ts_data, forecast_years=5):
    """
    Perform exponential smoothing forecast (Holt-Winters).
    """
    try:
        # Fit exponential smoothing model
        model = ExponentialSmoothing(
            ts_data, 
            trend='add', 
            seasonal=None, 
            initialization_method='estimated'
        )
        fitted_model = model.fit()
        
        # Generate forecast
        forecast = fitted_model.forecast(forecast_years)
        
        # Create result DataFrame
        historical = pd.DataFrame({
            'year': ts_data.index,
            'value': ts_data.values.flatten(),
            'type': 'Historical'
        })
        
        forecast_df = pd.DataFrame({
            'year': range(ts_data.index.max() + 1, ts_data.index.max() + forecast_years + 1),
            'value': forecast.values,
            'type': 'Forecast'
        })
        
        return pd.concat([historical, forecast_df], ignore_index=True)
    except:
        # Fall back to linear regression if exponential smoothing fails
        return linear_regression_forecast(ts_data, forecast_years)

def create_forecast_chart(forecast_data, country, indicator):
    """
    Create a forecast chart with historical data and predictions.
    """
    import plotly.express as px
    import plotly.graph_objects as go
    
    # Separate historical and forecast data
    historical = forecast_data[forecast_data['type'] == 'Historical']
    forecast = forecast_data[forecast_data['type'] == 'Forecast']
    
    # Create the figure
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=historical['year'],
        y=historical['value'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # Add forecast data
    fig.add_trace(go.Scatter(
        x=forecast['year'],
        y=forecast['value'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=6)
    ))
    
    # Add confidence interval (simplified)
    if len(forecast) > 0:
        last_historical_value = historical['value'].iloc[-1]
        forecast_std = historical['value'].std()
        
        fig.add_trace(go.Scatter(
            x=forecast['year'],
            y=forecast['value'] + forecast_std,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast['year'],
            y=forecast['value'] - forecast_std,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 127, 14, 0.2)',
            name='Confidence Interval',
            hoverinfo='skip'
        ))
    
    # Update layout
    indicator_titles = {
        'gdp_pc_usd': 'GDP per Capita (Current US$)',
        'life_expectancy_years': 'Life Expectancy (Years)',
        'population_total': 'Population',
        'ann_income_pc_growth_pct': 'Income Growth (%)'
    }
    
    fig.update_layout(
        title=f'{indicator_titles.get(indicator, indicator)} Forecast for {country}',
        xaxis_title='Year',
        yaxis_title=indicator_titles.get(indicator, indicator),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='lightgray',
        showline=True, 
        linewidth=1, 
        linecolor='black'
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='lightgray',
        showline=True, 
        linewidth=1, 
        linecolor='black'
    )
    
    return fig