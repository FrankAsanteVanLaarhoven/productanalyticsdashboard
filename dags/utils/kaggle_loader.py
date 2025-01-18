import kagglehub
import pandas as pd
import os
from datetime import datetime

def download_kaggle_dataset():
    """Download the e-commerce dataset from Kaggle"""
    try:
        path = kagglehub.dataset_download(
            "thedevastator/unlock-profits-with-e-commerce-sales-data"
        )
        # Find the CSV file in the directory
        for file in os.listdir(path):
            if file.endswith('.csv'):
                return os.path.join(path, file)
        raise FileNotFoundError("No CSV file found in the dataset")
    except Exception as e:
        raise Exception(f"Failed to download Kaggle dataset: {str(e)}")

def load_and_transform_data(file_path):
    """Load and transform the e-commerce dataset"""
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Rename columns to match our schema
    df = df.rename(columns={
        'Sku': 'sku',
        'Style Id': 'style_id',
        'Myntra MRP': 'mrp',  # Using Myntra MRP as base price
    })
    
    # Add required columns
    df['sale_date'] = datetime.now().date()  # You might want to generate random dates
    df['category'] = df['style_id'].str.split('_').str[0]  # Extract category from style_id
    df['status'] = 'Active'
    df['fulfillment'] = 'Marketplace'
    df['courier_status'] = 'Pending'
    df['quantity'] = 1  # Default quantity
    df['amount'] = df['mrp']  # Using MRP as amount
    df['is_b2b'] = False
    df['currency'] = 'INR'
    df['amount_usd'] = df['amount'] / 83.0  # Approximate INR to USD conversion
    
    # Select and reorder columns
    columns = [
        'category',
        'sku',
        'sale_date',
        'status',
        'fulfillment',
        'style_id',
        'courier_status',
        'quantity',
        'amount',
        'is_b2b',
        'currency',
        'amount_usd'
    ]
    
    return df[columns]

def analyze_dataset(df):
    """Print analysis of the dataset"""
    print("\n=== Dataset Analysis ===")
    print(f"Total Records: {len(df):,}")
    print(f"Unique Products: {df['sku'].nunique():,}")
    print(f"Categories: {df['category'].unique().tolist()}")
    print(f"\nValue Ranges:")
    print(f"Price Range: {df['amount'].min():,.2f} to {df['amount'].max():,.2f} {df['currency'].iloc[0]}")
    print(f"USD Range: ${df['amount_usd'].min():,.2f} to ${df['amount_usd'].max():,.2f}")
    
    print("\nCategory Distribution:")
    print(df['category'].value_counts())
    
    return True
