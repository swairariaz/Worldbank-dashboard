"""
World Bank Indicators Dashboard - Main Streamlit App
"""
import sys, os
sys.path.append(os.path.dirname(__file__))

import io
from datetime import datetime
import streamlit as st
import pandas as pd
from utils import load_all_data, get_available_countries, get_available_years, filter_data, calculate_kpis, get_change_icon, get_change_class
from styles import get_css_styles
from charts import create_gdp_chart, create_life_expectancy_chart, create_metric_card, create_gdp_bar_chart, create_population_bar_chart, create_bubble_chart, create_correlation_heatmap
from forecast import prepare_forecast_data, linear_regression_forecast, exponential_smoothing_forecast, create_forecast_chart

# Page configuration
st.set_page_config(
    page_title="World Bank Indicators Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS styles
st.markdown(get_css_styles(), unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Load data with caching
    data = load_all_data()
    
    if not data:
        st.error("Failed to load data. Please check the data files.")
        return
    
    # Extract dataframes
    main_data = data['main_data']
    latest_snapshot = data['latest_snapshot']
    world_aggregates = data['world_aggregates']
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">🌍 Dashboard Controls</div>
            <div class="sidebar-subtitle">Customize your analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Country selection
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-header">📍 Country Selection</div>', unsafe_allow_html=True)
        available_countries = get_available_countries(main_data)
        
        selected_countries = st.multiselect(
            "Select Countries",
            options=available_countries,
            default=available_countries[:5],
            help="Choose countries to analyze"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Year range selection with improved spacing
        st.markdown('<div class="filter-section" style="padding-bottom: 1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="filter-header">📅 Year Range</div>', unsafe_allow_html=True)
        available_years = get_available_years(main_data)
        min_year, max_year = min(available_years), max(available_years)
        
        selected_years = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(max_year - 5, max_year),
            help="Select the range of years to analyze"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info section
        st.markdown("""
        <div style="margin-top: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
            <p style="margin: 0; font-size: 0.85rem; color: #718096; line-height: 1.4;">
                <strong>💡 Tip:</strong> Select multiple countries to compare their development indicators over time.
                Data sourced from World Bank.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("""
    <div class="header">
        <h1 class="title">World Bank Indicators Dashboard</h1>
        <p class="subtitle">Explore global development indicators across countries and time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Page navigation
    st.markdown('<div class="navigation-select">', unsafe_allow_html=True)
    pages = {
        "Overview": overview_page,
        "Country Compare": country_compare_page,
        "Relationships": relationships_page,
        "Forecast": forecast_page,
        "Data & Download": data_page
    }
    
    selected_page = st.selectbox(
        "Navigate to", 
        list(pages.keys()),
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display selected page
    pages[selected_page](main_data, latest_snapshot, world_aggregates, selected_countries, selected_years)

def overview_page(main_data, latest_snapshot, world_aggregates, selected_countries, selected_years):
    """Overview page with KPIs and global trends."""
    st.markdown('<div class="section-header">📊 Overview</div>', unsafe_allow_html=True)
    
    # Filter data based on selections
    filtered_data = filter_data(main_data, selected_countries, selected_years)
    
    # Calculate KPIs
    current_year = max(selected_years)
    previous_year = current_year - 1 if current_year > min(selected_years) else current_year
    
    kpis = calculate_kpis(filtered_data, current_year, previous_year)
    
    # KPI Cards
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 1.5rem; color: #718096; font-size: 0.95rem;">
        These metrics represent aggregate values across all selected countries for the most recent year in your selection.
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Median GDP per capita
        kpi = kpis['median_gdp']
        change_icon = get_change_icon(kpi['change'])
        change_class = get_change_class(kpi['change'])
        st.markdown(create_metric_card(
            "Median GDP per Capita", 
            kpi['formatted_value'], 
            kpi['formatted_change'], 
            change_icon, 
            change_class
        ), unsafe_allow_html=True)
    
    with col2:
        # Median Life Expectancy
        kpi = kpis['median_life_expectancy']
        change_icon = get_change_icon(kpi['change'])
        change_class = get_change_class(kpi['change'])
        st.markdown(create_metric_card(
            "Median Life Expectancy", 
            kpi['formatted_value'], 
            kpi['formatted_change'], 
            change_icon, 
            change_class
        ), unsafe_allow_html=True)
    
    with col3:
        # Total Population
        kpi = kpis['total_population']
        change_icon = get_change_icon(kpi['change'])
        change_class = get_change_class(kpi['change'])
        st.markdown(create_metric_card(
            "Total Population", 
            kpi['formatted_value'], 
            kpi['formatted_change'], 
            change_icon, 
            change_class
        ), unsafe_allow_html=True)
    
    with col4:
        # Mean Income Growth
        kpi = kpis['mean_income_growth']
        change_icon = get_change_icon(kpi['change'])
        change_class = get_change_class(kpi['change'])
        st.markdown(create_metric_card(
            "Avg Income Growth", 
            kpi['formatted_value'], 
            kpi['formatted_change'], 
            change_icon, 
            change_class
        ), unsafe_allow_html=True)
    
    # Charts
    st.markdown('<div class="section-header">Global Trends</div>', unsafe_allow_html=True)
    
    # GDP Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">GDP per Capita Over Time</div>', unsafe_allow_html=True)
    gdp_chart = create_gdp_chart(filtered_data, selected_countries)
    st.plotly_chart(gdp_chart, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Life Expectancy Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Life Expectancy Over Time</div>', unsafe_allow_html=True)
    life_chart = create_life_expectancy_chart(filtered_data, selected_countries)
    st.plotly_chart(life_chart, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data summary (without sample data)
    with st.expander("📋 Data Summary & Statistics", expanded=False):
        st.write(f"**Showing data for {len(selected_countries)} countries from {selected_years[0]} to {selected_years[1]}**")
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        # Get only numeric columns for summary
        numeric_cols = ['gdp_pc_usd', 'life_expectancy_years', 'population_total', 'ann_income_pc_growth_pct']
        summary = filtered_data[numeric_cols].describe().round(2)
        
        st.dataframe(summary, width='stretch')

def country_compare_page(main_data, latest_snapshot, world_aggregates, selected_countries, selected_years):
    """Country comparison page."""
    st.markdown('<div class="section-header">🇺🇳 Country Comparison</div>', unsafe_allow_html=True)
    
    if not selected_countries:
        st.warning("Please select at least one country from the sidebar to compare.")
        return
    
    # Create two columns for the charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">GDP per Capita Ranking</div>', unsafe_allow_html=True)
        gdp_chart = create_gdp_bar_chart(latest_snapshot, selected_countries)
        st.plotly_chart(gdp_chart, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Population Ranking</div>', unsafe_allow_html=True)
        pop_chart = create_population_bar_chart(latest_snapshot, selected_countries)
        st.plotly_chart(pop_chart, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparison table
    st.markdown('<div class="section-header">Country Comparison Table</div>', unsafe_allow_html=True)

    # Create a copy to avoid modifying the original dataframe
    comparison_data = latest_snapshot[latest_snapshot['country'].isin(selected_countries)].copy()

    # Calculate ranks if they don't exist
    if 'gdp_rank' not in comparison_data.columns:
        comparison_data['gdp_rank'] = comparison_data['gdp_pc_usd'].rank(ascending=False, method='min').astype(int)
    if 'population_rank' not in comparison_data.columns:
        comparison_data['population_rank'] = comparison_data['population_total'].rank(ascending=False, method='min').astype(int)

    # Prepare table data
    table_data = comparison_data[['country', 'gdp_pc_usd', 'gdp_rank', 'life_expectancy_years', 
                                'population_total', 'population_rank', 'ann_income_pc_growth_pct']].copy()

    # Format numbers for display
    table_data['gdp_pc_usd'] = table_data['gdp_pc_usd'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
    table_data['population_total'] = table_data['population_total'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    table_data['ann_income_pc_growth_pct'] = table_data['ann_income_pc_growth_pct'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    table_data['life_expectancy_years'] = table_data['life_expectancy_years'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")

    # Rename columns for display
    table_data = table_data.rename(columns={
        'country': 'Country',
        'gdp_pc_usd': 'GDP per Capita',
        'gdp_rank': 'GDP Rank',
        'life_expectancy_years': 'Life Expectancy',
        'population_total': 'Population',
        'population_rank': 'Population Rank',
        'ann_income_pc_growth_pct': 'Income Growth'
    })

    # Display the table
    st.dataframe(
        table_data,
        width='stretch',
        hide_index=True,
        column_config={
            "Country": st.column_config.TextColumn(width="medium"),
            "GDP per Capita": st.column_config.TextColumn(width="small"),
            "GDP Rank": st.column_config.NumberColumn(width="small"),
            "Life Expectancy": st.column_config.TextColumn(width="small"),
            "Population": st.column_config.TextColumn(width="medium"),
            "Population Rank": st.column_config.NumberColumn(width="small"),
            "Income Growth": st.column_config.TextColumn(width="small")
        }
    )

def relationships_page(main_data, latest_snapshot, world_aggregates, selected_countries, selected_years):
    """Relationships and correlations page."""
    # Add inline CSS for the relationships page
    st.markdown("""
    <style>
    .relationships-filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .relationships-filter-header {
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #2d3748;
        font-size: 1rem;
    }
    
    .chart-subtitle {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .insight-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    .insight-content {
        font-size: 0.95rem;
        color: #4a5568;
        line-height: 1.6;
    }
    
    .insight-content ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .insight-content li {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🔗 Relationships & Correlations</div>', unsafe_allow_html=True)
    
    if not selected_countries:
        st.warning("Please select at least one country from the sidebar to analyze relationships.")
        return
    
    # Year selection for bubble chart with improved styling
    st.markdown('<div class="relationships-filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="relationships-filter-header">📅 Select Year for Analysis</div>', unsafe_allow_html=True)
    
    available_years = sorted(main_data['year'].unique())
    selected_year = st.select_slider(
        "Select Year for Visualization",
        options=available_years,
        value=max(available_years),
        help="Select the year to display in the visualizations"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create two columns for the charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bubble chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">GDP vs Life Expectancy (Bubble Chart)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Bubble size represents population, color represents income growth</div>', unsafe_allow_html=True)
        bubble_chart = create_bubble_chart(main_data, selected_year, selected_countries)
        st.plotly_chart(bubble_chart, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Correlation heatmap
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Indicator Correlations</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Relationship strength between metrics</div>', unsafe_allow_html=True)
        heatmap = create_correlation_heatmap(main_data, selected_countries)
        st.plotly_chart(heatmap, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights section
    st.markdown('<div class="section-header">📊 Data Insights</div>', unsafe_allow_html=True)
    
    # Calculate some basic insights
    filtered_data = main_data[(main_data['country'].isin(selected_countries)) & (main_data['year'] == selected_year)]
    
    if not filtered_data.empty:
        # Calculate correlations
        gdp_life_corr = filtered_data['gdp_pc_usd'].corr(filtered_data['life_expectancy_years'])
        income_gdp_corr = filtered_data['ann_income_pc_growth_pct'].corr(filtered_data['gdp_pc_usd'])
        pop_gdp_corr = filtered_data['population_total'].corr(filtered_data['gdp_pc_usd'])
        
        # Display insights in a grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">GDP vs Life Expectancy</div>
                <div class="metric-value">{gdp_life_corr:.2f}</div>
                <div class="metric-change">{'Strong positive' if gdp_life_corr > 0.7 else 'Moderate positive' if gdp_life_corr > 0.3 else 'Weak positive' if gdp_life_corr > 0 else 'No relationship' if gdp_life_corr == 0 else 'Weak negative' if gdp_life_corr > -0.3 else 'Moderate negative' if gdp_life_corr > -0.7 else 'Strong negative'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Income Growth vs GDP</div>
                <div class="metric-value">{income_gdp_corr:.2f}</div>
                <div class="metric-change">{'Strong positive' if income_gdp_corr > 0.7 else 'Moderate positive' if income_gdp_corr > 0.3 else 'Weak positive' if income_gdp_corr > 0 else 'No relationship' if income_gdp_corr == 0 else 'Weak negative' if income_gdp_corr > -0.3 else 'Moderate negative' if income_gdp_corr > -0.7 else 'Strong negative'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Population vs GDP</div>
                <div class="metric-value">{pop_gdp_corr:.2f}</div>
                <div class="metric-change">{'Strong positive' if pop_gdp_corr > 0.7 else 'Moderate positive' if pop_gdp_corr > 0.3 else 'Weak positive' if pop_gdp_corr > 0 else 'No relationship' if pop_gdp_corr == 0 else 'Weak negative' if pop_gdp_corr > -0.3 else 'Moderate negative' if pop_gdp_corr > -0.7 else 'Strong negative'}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data available for the selected countries and year.")
    
    # Interpretation guide (separate from Data Insights)
    st.markdown('<div class="section-header">📖 Correlation Interpretation Guide</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-content">
            <ul>
                <li><strong>1.0 to 0.7:</strong> Strong positive relationship</li>
                <li><strong>0.7 to 0.3:</strong> Moderate positive relationship</li>
                <li><strong>0.3 to 0.1:</strong> Weak positive relationship</li>
                <li><strong>0.0:</strong> No relationship</li>
                <li><strong>-0.1 to -0.3:</strong> Weak negative relationship</li>
                <li><strong>-0.3 to -0.7:</strong> Moderate negative relationship</li>
                <li><strong>-0.7 to -1.0:</strong> Strong negative relationship</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def forecast_page(main_data, latest_snapshot, world_aggregates, selected_countries, selected_years):
    """Forecasting page."""
    st.markdown('<div class="section-header">🔮 Forecast</div>', unsafe_allow_html=True)
    
    # If no countries are selected, show a warning
    if not selected_countries:
        st.warning("Please select at least one country from the sidebar to run forecasts.")
        return
    
    # We'll allow forecasting for one country at a time for simplicity
    selected_country = st.selectbox(
        "Select Country for Forecast",
        options=selected_countries,
        index=0
    )
    
    # Indicator selection
    indicators = {
        'GDP per Capita': 'gdp_pc_usd',
        'Life Expectancy': 'life_expectancy_years',
        'Population': 'population_total',
        'Income Growth': 'ann_income_pc_growth_pct'
    }
    
    selected_indicator = st.selectbox(
        "Select Indicator to Forecast",
        options=list(indicators.keys())
    )
    
    # Forecast method selection
    forecast_method = st.radio(
        "Select Forecast Method",
        options=["Linear Regression", "Exponential Smoothing"],
        horizontal=True
    )
    
    # Number of years to forecast
    forecast_years = st.slider(
        "Years to Forecast",
        min_value=1,
        max_value=10,
        value=5
    )
    
    # Button to run forecast
    if st.button("Generate Forecast"):
        # Prepare data for forecasting
        indicator_code = indicators[selected_indicator]
        ts_data = prepare_forecast_data(main_data, selected_country, indicator_code)
        
        if ts_data is None:
            st.error("Not enough data available for forecasting this indicator for the selected country.")
            return
        
        # Perform forecast based on selected method
        if forecast_method == "Linear Regression":
            forecast_data = linear_regression_forecast(ts_data, forecast_years)
        else:
            forecast_data = exponential_smoothing_forecast(ts_data, forecast_years)
        
        # Create and display the forecast chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        forecast_chart = create_forecast_chart(forecast_data, selected_country, indicator_code)
        st.plotly_chart(forecast_chart, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display forecast summary
        st.markdown('<div class="section-header">Forecast Summary</div>', unsafe_allow_html=True)
        
        # Get the last historical value and the final forecast value
        last_historical = forecast_data[forecast_data['type'] == 'Historical'].iloc[-1]
        final_forecast = forecast_data[forecast_data['type'] == 'Forecast'].iloc[-1]
        
        # Calculate percentage change
        change = ((final_forecast['value'] - last_historical['value']) / last_historical['value']) * 100
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Last Historical Value", 
                f"${last_historical['value']:,.0f}" if indicator_code == 'gdp_pc_usd' else f"{last_historical['value']:,.1f}",
                f"{last_historical['year']}"
            )
        
        with col2:
            st.metric(
                f"{forecast_years}-Year Forecast", 
                f"${final_forecast['value']:,.0f}" if indicator_code == 'gdp_pc_usd' else f"{final_forecast['value']:,.1f}",
                f"{final_forecast['year']}"
            )
        
        with col3:
            st.metric(
                "Projected Change", 
                f"{change:+.1f}%"
            )
        
        # Show forecast data table
        with st.expander("View Forecast Data", expanded=False):
            # Format values based on indicator type
            display_data = forecast_data.copy()
            if indicator_code == 'gdp_pc_usd':
                display_data['value'] = display_data['value'].apply(lambda x: f"${x:,.0f}")
            else:
                display_data['value'] = display_data['value'].apply(lambda x: f"{x:,.1f}")
            
            st.dataframe(
                display_data,
                width='stretch',
                hide_index=True,
                column_config={
                    "year": st.column_config.NumberColumn("Year"),
                    "value": st.column_config.TextColumn("Value"),
                    "type": st.column_config.TextColumn("Type")
                }
            )

def data_page(main_data, latest_snapshot, world_aggregates, selected_countries, selected_years):
    """Data exploration and download page."""
    st.markdown('<div class="section-header">💾 Data & Download</div>', unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["📊 Data Explorer", "📥 Export Data", "📄 Generate Report"])
    
    with tab1:
        st.markdown("### Data Explorer")
        st.write("Explore and filter the dataset with interactive controls.")
        
        # Additional filtering options
        col1, col2 = st.columns(2)
        
        with col1:
            # Indicator selection
            indicators = st.multiselect(
                "Select Indicators to Display",
                options=['gdp_pc_usd', 'life_expectancy_years', 'population_total', 'ann_income_pc_growth_pct'],
                default=['gdp_pc_usd', 'life_expectancy_years'],
                help="Choose which indicators to include in the data table"
            )
        
        with col2:
            # Sort options
            sort_by = st.selectbox(
                "Sort By",
                options=['country', 'year', 'gdp_pc_usd', 'life_expectancy_years', 'population_total'],
                index=0
            )
            
            sort_order = st.radio(
                "Sort Order",
                options=["Ascending", "Descending"],
                horizontal=True
            )
        
        # Filter data based on selections
        filtered_data = filter_data(main_data, selected_countries, selected_years)
        
        if not indicators:
            st.warning("Please select at least one indicator to display.")
            display_data = filtered_data[['country', 'year']]
        else:
            display_data = filtered_data[['country', 'year'] + indicators]
        
        # Apply sorting
        ascending = sort_order == "Ascending"
        display_data = display_data.sort_values(sort_by, ascending=ascending)
        
        # Display the data table - FIXED: use width='stretch' instead of use_container_width=True
        st.dataframe(
            display_data,
            width='stretch',  # Changed from use_container_width=True
            height=400,
            hide_index=True
        )
        
        # Show data summary
        st.markdown("#### Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(display_data))
        
        with col2:
            st.metric("Countries", display_data['country'].nunique())
        
        with col3:
            st.metric("Years", f"{display_data['year'].min()} - {display_data['year'].max()}")
    
    with tab2:
        st.markdown("### Export Data")
        st.write("Export the filtered data in various formats.")
        
        # CSV Export
        st.markdown("#### CSV Export")
        csv_data = filtered_data.to_csv(index=False)
        
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="worldbank_data.csv",
            mime="text/csv",
            help="Download the filtered data as a CSV file"
        )
        
        # JSON Export
        st.markdown("#### JSON Export")
        json_data = filtered_data.to_json(orient="records", indent=2)
        
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="worldbank_data.json",
            mime="application/json",
            help="Download the filtered data as a JSON file"
        )
        
        # Excel Export (requires openpyxl)
        st.markdown("#### Excel Export")
        
        try:
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, sheet_name='WorldBank Data', index=False)
            
            st.download_button(
                label="Download Excel",
                data=buffer.getvalue(),
                file_name="worldbank_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download the filtered data as an Excel file"
            )
        except ImportError:
            st.info("Excel export requires the openpyxl package. Install it with: `pip install openpyxl`")
    
    with tab3:
        st.markdown("### Generate Report")
        st.write("Create a customized report with selected data and visualizations.")
        
        # Report options
        report_title = st.text_input("Report Title", "World Bank Indicators Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_charts = st.checkbox("Include Charts", value=True)
            include_summary = st.checkbox("Include Summary Statistics", value=True)
        
        with col2:
            include_raw_data = st.checkbox("Include Raw Data Preview", value=False)
            report_format = st.selectbox("Report Format", ["PDF", "HTML"])
        
        # Generate report button - FIXED: This should be inside the tab3 block
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                # Create report content
                report_content = f"""
# {report_title}

## Report Overview
- Generated on: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}
- Countries: {', '.join(selected_countries)}
- Time period: {selected_years[0]} - {selected_years[1]}
- Total records: {len(filtered_data)}

## Summary Statistics
"""
                
                # Add summary statistics
                if include_summary:
                    numeric_cols = ['gdp_pc_usd', 'life_expectancy_years', 'population_total', 'ann_income_pc_growth_pct']
                    summary = filtered_data[numeric_cols].describe().round(2)
                    report_content += f"\n{summary.to_markdown()}\n"
                
                # Add raw data preview
                if include_raw_data:
                    report_content += "\n## Data Preview\n"
                    report_content += f"\n{filtered_data.head(10).to_markdown(index=False)}\n"
                
                # Create download button for the report
                if report_format == "PDF":
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                        from reportlab.lib.styles import getSampleStyleSheet
                        from reportlab.lib import colors
                        from reportlab.lib.units import inch
                        
                        # Create a PDF buffer
                        buffer = io.BytesIO()
                        doc = SimpleDocTemplate(buffer, pagesize=letter)
                        styles = getSampleStyleSheet()
                        story = []
                        
                        # Add title
                        title = Paragraph(report_title, styles['Title'])
                        story.append(title)
                        story.append(Spacer(1, 12))
                        
                        # Add report overview
                        overview_text = f"""
                        <b>Report Overview</b><br/>
                        Generated on: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}<br/>
                        Countries: {', '.join(selected_countries)}<br/>
                        Time period: {selected_years[0]} - {selected_years[1]}<br/>
                        Total records: {len(filtered_data)}
                        """
                        overview = Paragraph(overview_text, styles['Normal'])
                        story.append(overview)
                        story.append(Spacer(1, 12))
                        
                        # Add summary statistics
                        if include_summary:
                            summary_header = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
                            story.append(summary_header)
                            
                            # Convert summary to a table
                            summary_data = [list(summary.columns)]
                            for idx in summary.index:
                                summary_data.append([idx] + list(summary.loc[idx]))
                            
                            summary_table = Table(summary_data)
                            summary_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 10),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('FONTSIZE', (0, 1), (-1, -1), 8),
                            ]))
                            story.append(summary_table)
                            story.append(Spacer(1, 12))
                        
                        # Add raw data preview
                        if include_raw_data:
                            data_header = Paragraph("<b>Data Preview</b>", styles['Heading2'])
                            story.append(data_header)
                            
                            # Convert data preview to a table
                            preview_data = [list(filtered_data.head(10).columns)]
                            for _, row in filtered_data.head(10).iterrows():
                                preview_data.append(list(row))
                            
                            preview_table = Table(preview_data)
                            preview_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 8),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('FONTSIZE', (0, 1), (-1, -1), 6),
                            ]))
                            story.append(preview_table)
                        
                        # Build PDF
                        doc.build(story)
                        buffer.seek(0)
                        
                        st.download_button(
                            label="Download PDF Report",
                            data=buffer.getvalue(),
                            file_name="worldbank_report.pdf",
                            mime="application/pdf",
                            help="Download the report as a PDF file"
                        )
                        
                    except ImportError:
                        st.error("PDF generation requires the reportlab package. Install it with: `pip install reportlab`")
                else:
                    # HTML report
                    st.download_button(
                        label="Download HTML Report",
                        data=report_content,
                        file_name="worldbank_report.html",
                        mime="text/html",
                        help="Download the report as an HTML file"
                    )

if __name__ == "__main__":
    main()
