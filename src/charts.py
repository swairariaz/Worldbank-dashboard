"""
Chart creation functions using Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional

def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, color_col: str, 
                     title: str, y_axis_title: str) -> go.Figure:
    """
    Create a line chart for time series data.
    """
    fig = px.line(
        df, 
        x=x_col, 
        y=y_col, 
        color=color_col,
        title=title,
        labels={x_col: 'Year', y_col: y_axis_title, color_col: 'Country'},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None
        ),
        height=500,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='lightgray',
        showline=True, 
        linewidth=1, 
        linecolor='black',
        tickmode='linear',
        dtick=1
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='lightgray',
        showline=True, 
        linewidth=1, 
        linecolor='black'
    )
    
    # Add a subtle annotation with data source
    fig.add_annotation(
        x=0.02, y=-0.15,
        xref="paper", yref="paper",
        text="Source: World Bank Development Indicators",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    
    return fig

def create_gdp_chart(df: pd.DataFrame, selected_countries: List[str]) -> go.Figure:
    """
    Create GDP per capita line chart.
    """
    if not selected_countries:
        return go.Figure()
    
    filtered_df = df[df['country'].isin(selected_countries)]
    
    fig = create_line_chart(
        filtered_df,
        x_col='year',
        y_col='gdp_pc_usd',
        color_col='country',
        title='GDP per Capita Over Time',
        y_axis_title='GDP per Capita (Current US$)'
    )
    
    # Format y-axis with dollar signs and commas
    fig.update_layout(yaxis_tickprefix='$', yaxis_tickformat=',.0f')
    
    return fig

def create_life_expectancy_chart(df: pd.DataFrame, selected_countries: List[str]) -> go.Figure:
    """
    Create life expectancy line chart.
    """
    if not selected_countries:
        return go.Figure()
    
    filtered_df = df[df['country'].isin(selected_countries)]
    
    fig = create_line_chart(
        filtered_df,
        x_col='year',
        y_col='life_expectancy_years',
        color_col='country',
        title='Life Expectancy Over Time',
        y_axis_title='Life Expectancy (Years)'
    )
    
    return fig

def create_metric_card(label: str, value: str, change: str, change_icon: str, change_class: str):
    """
    Create a custom metric card with HTML/CSS.
    """
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-change {change_class}">
            {change_icon} {change}
        </div>
    </div>
    """

def create_gdp_bar_chart(latest_snapshot: pd.DataFrame, selected_countries: List[str]) -> go.Figure:
    """
    Create a horizontal bar chart for GDP per capita ranking.
    """
    # Create a copy to avoid modifying the original dataframe
    df = latest_snapshot.copy()
    
    # Calculate GDP rank if it doesn't exist
    if 'gdp_rank' not in df.columns:
        df['gdp_rank'] = df['gdp_pc_usd'].rank(ascending=False, method='min').astype(int)
    
    # Filter data for selected countries and sort by GDP rank
    filtered_df = df[df['country'].isin(selected_countries)]
    filtered_df = filtered_df.sort_values('gdp_rank')
    
    # Format GDP values for display
    filtered_df['gdp_formatted'] = filtered_df['gdp_pc_usd'].apply(
        lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A"
    )
    
    fig = px.bar(
        filtered_df,
        y='country',
        x='gdp_pc_usd',
        orientation='h',
        title='GDP per Capita Ranking',
        labels={'gdp_pc_usd': 'GDP per Capita (Current US$)', 'country': 'Country'},
        color='gdp_pc_usd',
        color_continuous_scale='Viridis'
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        height=max(400, len(selected_countries) * 50),  # Increased height for better spacing
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=120, r=50, t=80, b=50),  # Increased left margin for country names
        title_x=0.5,
        title_font_size=16,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    # Format x-axis with dollar signs
    fig.update_xaxes(
        tickprefix='$', 
        tickformat=',.0f',
        title='GDP per Capita (Current US$)',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    fig.update_yaxes(
        title='Country',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)  # Smaller font for country names
    )
    
    # Add value annotations with proper positioning
    for i, row in enumerate(filtered_df.itertuples()):
        fig.add_annotation(
            x=row.gdp_pc_usd,
            y=row.country,
            text=f"${row.gdp_pc_usd:,.0f}",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=10, color='black')
        )
    
    return fig

def create_population_bar_chart(latest_snapshot: pd.DataFrame, selected_countries: List[str]) -> go.Figure:
    """
    Create a horizontal bar chart for population ranking.
    """
    # Create a copy to avoid modifying the original dataframe
    df = latest_snapshot.copy()
    
    # Calculate population rank if it doesn't exist
    if 'population_rank' not in df.columns:
        df['population_rank'] = df['population_total'].rank(ascending=False, method='min').astype(int)
    
    # Filter data for selected countries and sort by population rank
    filtered_df = df[df['country'].isin(selected_countries)]
    filtered_df = filtered_df.sort_values('population_rank')
    
    # Format population values for display
    from src.utils import format_number
    filtered_df['population_formatted'] = filtered_df['population_total'].apply(
        lambda x: format_number(x, 1) if pd.notna(x) else "N/A"
    )
    
    fig = px.bar(
        filtered_df,
        y='country',
        x='population_total',
        orientation='h',
        title='Population Ranking',
        labels={'population_total': 'Population', 'country': 'Country'},
        color='population_total',
        color_continuous_scale='Plasma'
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        height=max(400, len(selected_countries) * 50),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=120, r=50, t=80, b=50),
        title_x=0.5,
        title_font_size=16,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    # Format x-axis with vertical orientation
    fig.update_xaxes(
        tickformat=',.0f',
        title='Population',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickangle=-90,  # Rotate x-axis labels vertically
        tickfont=dict(size=10)  # Smaller font for x-axis labels
    )
    
    fig.update_yaxes(
        title='Country',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    )
    
    # Add value annotations with proper positioning
    for i, row in enumerate(filtered_df.itertuples()):
        fig.add_annotation(
            x=row.population_total,
            y=row.country,
            text=format_number(row.population_total, 1),
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=10, color='black')
        )
    
    return fig

def create_bubble_chart(df: pd.DataFrame, selected_year: int, selected_countries: List[str]) -> go.Figure:
    """
    Create a bubble scatter plot for GDP vs Life Expectancy.
    """
    # Filter data for selected year and countries
    filtered_df = df[(df['year'] == selected_year) & (df['country'].isin(selected_countries))]
    
    # Remove rows with missing values
    filtered_df = filtered_df.dropna(subset=['gdp_pc_usd', 'life_expectancy_years', 'population_total', 'ann_income_pc_growth_pct'])
    
    # Format population for hover text
    from src.utils import format_number
    filtered_df['population_formatted'] = filtered_df['population_total'].apply(
        lambda x: format_number(x, 1) if pd.notna(x) else "N/A"
    )
    
    fig = px.scatter(
        filtered_df,
        x='gdp_pc_usd',
        y='life_expectancy_years',
        size='population_total',
        color='ann_income_pc_growth_pct',
        hover_name='country',
        hover_data={
            'gdp_pc_usd': ':.0f',
            'life_expectancy_years': ':.1f',
            'population_total': False,
            'ann_income_pc_growth_pct': ':.1f',
            'population_formatted': True
        },
        title='',
        labels={
            'gdp_pc_usd': 'GDP per Capita (Current US$)',
            'life_expectancy_years': 'Life Expectancy (Years)',
            'population_formatted': 'Population',
            'ann_income_pc_growth_pct': 'Income Growth (%)'
        },
        color_continuous_scale='RdYlGn',
        size_max=50
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        height=500,
        margin=dict(l=50, r=50, t=30, b=50),
        title_x=0.5,
        title_font_size=16,
        coloraxis_colorbar=dict(
            title="Income Growth (%)",
            thickness=15,
            len=0.75,
            yanchor="middle",
            y=0.5
        )
    )
    
    # Format x-axis with dollar signs
    fig.update_xaxes(
        tickprefix='$', 
        tickformat=',.0f',
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black',
        title='GDP per Capita (Current US$)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black',
        title='Life Expectancy (Years)'
    )
    
    # Improve hover template
    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>GDP: $%{x:,.0f}<br>Life Expectancy: %{y:.1f} years<br>Population: %{customdata[0]}<br>Income Growth: %{marker.color:.1f}%<extra></extra>',
        customdata=filtered_df['population_formatted'].values
    )
    
    return fig

def create_correlation_heatmap(df: pd.DataFrame, selected_countries: List[str]) -> go.Figure:
    """
    Create a correlation heatmap across indicators.
    """
    # Filter data for selected countries
    filtered_df = df[df['country'].isin(selected_countries)]
    
    # Select only numeric columns for correlation
    numeric_cols = ['gdp_pc_usd', 'life_expectancy_years', 'population_total', 'ann_income_pc_growth_pct']
    numeric_df = filtered_df[numeric_cols].dropna()
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Create custom labels with better formatting
    labels = {
        'gdp_pc_usd': 'GDP per Capita',
        'life_expectancy_years': 'Life Expectancy',
        'population_total': 'Population',
        'ann_income_pc_growth_pct': 'Income Growth'
    }
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title='',
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1
    )
    
    # Update layout for better appearance with more space for labels
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, family='Arial'),
        height=550,  # Increased height to accommodate the title
        width=600,
        margin=dict(l=150, r=50, t=30, b=180),  # Increased bottom margin for the title
        title_x=0.5,
        title_font_size=16,
        coloraxis_colorbar=dict(
            title="Correlation",
            thickness=15,
            len=0.6,
            yanchor="middle",
            y=0.5
        )
    )
    
    # Update x and y axis labels with better formatting
    fig.update_xaxes(
        tickvals=list(range(len(numeric_cols))),
        ticktext=[labels[col] for col in numeric_cols],
        tickangle=90,  # Set to 90 for vertical orientation
        tickfont=dict(size=12),
        tickmode='array',
        title_text=''
    )
    
    fig.update_yaxes(
        tickvals=list(range(len(numeric_cols))),
        ticktext=[labels[col] for col in numeric_cols],
        tickfont=dict(size=12),
        tickmode='array',
        title_text=''
    )
    
    # Improve the text display on the heatmap
    fig.update_traces(
        texttemplate='%{text:.2f}',
        textfont=dict(size=12, color='black')
    )
    
    # Add titles manually to have more control over positioning
    # Move the x-axis title further down
    fig.add_annotation(
        x=0.5, y=-0.35,  # Adjusted y position to be lower
        xref="paper", yref="paper",
        text="Indicators",
        showarrow=False,
        font=dict(size=14),
        yanchor="top"
    )
    
    fig.add_annotation(
        x=-0.1, y=0.5,
        xref="paper", yref="paper",
        text="Indicators",
        showarrow=False,
        textangle=-90,
        font=dict(size=14)
    )
    
    return fig