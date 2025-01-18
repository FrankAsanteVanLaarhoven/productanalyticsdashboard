# /Users/frankvanlaarhoven/airflow_project/product_analysis_app/pages/home.py
import streamlit as st

def show():
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem;'>
                Welcome to Product Analysis
            </h1>
            <p style='font-size: 1.4rem; color: #86868b; font-weight: 500;'>
                Navigate through our insights using the sidebar
            </p>
        </div>
        
        <div class='metric-card'>
            <h3>Quick Start Guide</h3>
            <ul>
                <li>📊 <strong>Analytics:</strong> View detailed charts and metrics</li>
                <li>🎯 <strong>Recommendations:</strong> Get strategic insights</li>
                <li>📈 <strong>Dashboard:</strong> Executive overview</li>
                <li>💬 <strong>Chat:</strong> Ask questions about your data</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()