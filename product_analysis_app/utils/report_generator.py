# utils/report_generator.py
import pandas as pd
import plotly
import json

class ReportGenerator:
    @staticmethod
    def generate_excel(df, charts):
        """Generate Excel report with embedded charts"""
        pass
    
    @staticmethod
    def generate_pdf(df, charts):
        """Generate PDF report"""
        pass
    
    @staticmethod
    def generate_json(df):
        """Generate JSON export"""
        return df.to_json(orient='records')