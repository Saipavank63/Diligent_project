#!/usr/bin/env python3
"""
GTM Engineer Data Analysis - Initial Data Exploration
Author: GTM Engineer Candidate
Date: September 2025

This script provides initial exploration of the Diligent prospect dataset
to understand data structure, quality, and fields for cleaning.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


def load_and_explore_data():
    """Load the dataset and perform initial exploration"""

    # Load the Excel file
    file_path = '../data/Diligent_GTM_Engineer_Exercise_with_Instructions.xlsx'

    try:
        # Read all sheets to understand structure
        excel_file = pd.ExcelFile(file_path)
        print("Available sheets:", excel_file.sheet_names)

        # Load the main dataset from 'Dataset' sheet
        df = pd.read_excel(file_path, sheet_name='Dataset')

        print(f"\nDataset Shape: {df.shape}")
        print(f"Total Records: {len(df)}")

        # Display basic info
        print("\n" + "="*50)
        print("DATASET OVERVIEW")
        print("="*50)

        print("\nColumn Names and Types:")
        for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes)):
            print(f"{i+1:2d}. {col:<30} ({dtype})")

        print("\n" + "="*50)
        print("DATA QUALITY ASSESSMENT")
        print("="*50)

        # Missing data analysis
        missing_data = df.isnull().sum()
        missing_pct = (missing_data / len(df)) * 100

        quality_df = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': missing_data.values,
            'Missing_Percentage': missing_pct.values,
            'Unique_Values': [df[col].nunique() for col in df.columns],
            'Data_Type': df.dtypes.values
        })

        quality_df = quality_df.sort_values(
            'Missing_Percentage', ascending=False)
        print(quality_df.to_string(index=False))

        print("\n" + "="*50)
        print("SAMPLE DATA (First 5 rows)")
        print("="*50)
        print(df.head().to_string())

        # Identify key fields for analysis
        print("\n" + "="*50)
        print("KEY FIELD CATEGORIES")
        print("="*50)

        company_fields = [col for col in df.columns if any(term in col.lower()
                                                           for term in ['company', 'name', 'website', 'domain', 'sfdc'])]
        firmographic_fields = [col for col in df.columns if any(term in col.lower()
                                                                for term in ['industry', 'employee', 'revenue', 'tier', 'location', 'region'])]
        gtm_fields = [col for col in df.columns if any(term in col.lower()
                                                       for term in ['interest', 'source', 'role', 'title', 'tech', 'intent', 'touch', 'status'])]

        print("Company Info Fields:", company_fields)
        print("Firmographic Fields:", firmographic_fields)
        print("GTM Signal Fields:", gtm_fields)

        return df, quality_df

    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None


def analyze_key_fields(df):
    """Analyze key fields that need cleaning/standardization"""

    print("\n" + "="*50)
    print("FIELD-SPECIFIC ANALYSIS")
    print("="*50)

    # Employee count analysis
    if 'Employee Count' in df.columns:
        print("\nEmployee Count Values:")
        print(df['Employee Count'].value_counts().head(10))

    # Revenue analysis
    revenue_cols = [col for col in df.columns if 'revenue' in col.lower()]
    for col in revenue_cols:
        print(f"\n{col} Values:")
        print(df[col].value_counts().head(10))

    # Region analysis
    region_cols = [col for col in df.columns if 'region' in col.lower()]
    for col in region_cols:
        print(f"\n{col} Values:")
        print(df[col].value_counts())

    # Industry analysis
    industry_cols = [col for col in df.columns if 'industry' in col.lower()]
    for col in industry_cols:
        print(f"\n{col} Values:")
        print(df[col].value_counts().head(10))


if __name__ == "__main__":
    print("GTM Engineer Data Analysis - Dataset Exploration")
    print("="*60)

    df, quality_df = load_and_explore_data()

    if df is not None:
        analyze_key_fields(df)

        # Save quality assessment
        quality_df.to_csv(
            '../analysis/data_quality_assessment.csv', index=False)
        print(f"\nData quality assessment saved to ../analysis/data_quality_assessment.csv")

        # Save sample of raw data for reference
        df.head(20).to_csv('../analysis/sample_raw_data.csv', index=False)
        print(f"Sample raw data saved to ../analysis/sample_raw_data.csv")

    print("\nExploration complete!")
