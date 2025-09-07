"""
CSS styles and theme configuration for the Streamlit dashboard.
"""

def get_css_styles():
    """
    Return CSS styles for the dashboard.
    """
    return """
    <style>
    /* Main styles */
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Header styles */
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        color: white;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Card styles */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 4px solid #667eea;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: #2d3748;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    .metric-change {
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.3rem;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        background-color: #f7fafc;
        margin: 0 auto;
        width: fit-content;
    }
    
    .positive-change {
        color: #38a169;
        background-color: #f0fff4;
    }
    
    .negative-change {
        color: #e53e3e;
        background-color: #fff5f5;
    }
    
    /* Sidebar styles - FIXED FOR YEAR RANGE */
    .sidebar .sidebar-content {
        background: #ffffff;
        padding: 1.5rem 1rem;
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-header {
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #2d3748;
    }
    
    .sidebar-subtitle {
        font-size: 0.85rem;
        color: #718096;
    }
    
    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .filter-header {
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #2d3748;
        font-size: 1rem;
    }
    
    /* Improved form elements with specific fix for slider */
    .stSelectbox > div > div, 
    .stMultiselect > div > div {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* Specific fix for the slider to prevent cutting off */
    .stSlider > div {
        padding-bottom: 1.5rem; /* Add space at bottom for slider labels */
        margin-bottom: 0.5rem;
    }
    
    .stSlider div[data-testid="stSlider"] {
        width: 100%;
    }
    
    .stSlider div[data-testid="stSlider"] > div {
        padding-bottom: 0; /* Reset any padding that might be causing issues */
    }
    
    /* Ensure slider track and thumb are properly visible */
    .stSlider div[data-testid="stSlider"] div {
        background-color: #667eea;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    /* Remove default streamlit decorations */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Navigation selectbox styling */
    .navigation-select {
        margin: 1.5rem 0;
    }
    
    .navigation-select > div > div {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 0.5rem;
    }

    .insight-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
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
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .title {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 1.6rem;
        }
        
        .chart-container {
            padding: 1rem;
        }
        
        /* Extra space for slider on mobile */
        .stSlider > div {
            padding-bottom: 2rem;
        }
    }
    </style>
    """