# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/config/styles.py
CUSTOM_STYLES = """
<style>
    /* Base styles */
    * {
        transition: all 0.3s ease-in-out;
    }
    
    .stApp {
        background: linear-gradient(180deg, #f5f5f7 0%, #fff 100%);
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Price Rating Colors - Matching view CASE statements */
    .price-rating-AAA {
        background-color: #28a745;  /* Maintain premium pricing */
        color: white;
    }
    
    .price-rating-AA {
        background-color: #17a2b8;  /* Consider price optimization */
        color: white;
    }
    
    .price-rating-A {
        background-color: #ffc107;  /* Review pricing strategy */
        color: black;
    }
    
    .price-rating-B {
        background-color: #dc3545;  /* Evaluate market position */
        color: white;
    }
    
    /* Volume Rating Colors - Matching view CASE statements */
    .volume-high {
        background-color: #28a745;  /* Maintain inventory levels */
        color: white;
    }
    
    .volume-medium {
        background-color: #ffc107;  /* Monitor stock levels */
        color: black;
    }
    
    .volume-standard {
        background-color: #17a2b8;  /* Review stock strategy */
        color: white;
    }
    
    /* Strategy badges */
    .strategy-badge {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.875rem;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    /* Metrics styling */
    .metric-container {
        padding: 1rem;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #666;
        margin-top: 0.25rem;
    }
    
    /* Table enhancements */
    .dataframe {
        border: none !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: #f8f9fa;
        font-weight: 600;
        padding: 0.75rem 1rem !important;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem !important;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Strategy recommendations */
    .recommendation {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .recommendation-premium {
        background-color: rgba(40, 167, 69, 0.1);
        border-left: 4px solid #28a745;
    }
    
    .recommendation-optimize {
        background-color: rgba(23, 162, 184, 0.1);
        border-left: 4px solid #17a2b8;
    }
    
    .recommendation-review {
        background-color: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
    }
    
    .recommendation-evaluate {
        background-color: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #dc3545;
    }
</style>
"""