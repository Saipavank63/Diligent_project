#!/usr/bin/env python3
"""
GTM Engineer Data Analysis - Data Cleaning and Processing Pipeline
Author: GTM Engineer Candidate
Date: September 2025

This script cleans and standardizes the Diligent prospect dataset,
including normalization of employee ranges, revenue values, regions, and dates.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DiligentDataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None

    def load_data(self):
        """Load the dataset from Excel file"""
        self.df = pd.read_excel(self.file_path, sheet_name='Dataset')
        print(
            f"Loaded {len(self.df)} records with {len(self.df.columns)} columns")
        return self.df

    def normalize_employee_count(self, value):
        """Normalize employee count to standardized ranges"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return 'Unknown'

        value_str = str(value).lower().strip()

        # Handle text descriptions
        if 'five hundred' in value_str:
            return '500-1,000'
        elif 'approx 800' in value_str:
            return '500-1,000'

        # Handle range formats
        if '-' in value_str:
            return value_str.title()  # Keep as-is but capitalize
        elif 'to' in value_str:
            # Convert "500 to 1000" to "500-1,000"
            parts = value_str.split('to')
            if len(parts) == 2:
                start = parts[0].strip()
                end = parts[1].strip()
                return f"{start}-{end}"
        elif '+' in value_str:
            return value_str.upper()  # "1000+" -> "1000+"

        return value_str.title()

    def normalize_revenue(self, value):
        """Normalize revenue to USD millions format"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return 'Unknown'

        value_str = str(value).strip()

        # Extract numeric value and currency
        # Handle formats: €20M, $20M, USD 250M, 5000000, 20,000,000 USD

        # Remove currency symbols and convert to number
        clean_value = re.sub(r'[€$,]', '', value_str)

        # Handle different notations
        if 'USD' in clean_value.upper():
            clean_value = re.sub(r'USD', '', clean_value,
                                 flags=re.IGNORECASE).strip()

        # Extract the numeric part
        numeric_match = re.search(r'(\d+(?:\.\d+)?)', clean_value)
        if not numeric_match:
            return 'Unknown'

        number = float(numeric_match.group(1))

        # Handle scale indicators
        if 'M' in value_str.upper():
            return f"${int(number)}M"
        elif 'B' in value_str.upper():
            return f"${int(number * 1000)}M"  # Convert billions to millions
        elif len(str(int(number))) >= 7:  # 5000000 format
            return f"${int(number / 1000000)}M"
        else:
            return f"${int(number)}M"

    def normalize_region(self, value):
        """Normalize region codes to standard format"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return 'Unknown'

        value_str = str(value).upper().strip()

        # Mapping of region codes
        region_mapping = {
            'AMS': 'Americas',
            'EMEA': 'EMEA',
            'APAC': 'APAC',
            'UKI': 'UK & Ireland',
            'DACH': 'DACH',
            'FR': 'France',
            'MDO': 'MEA'  # Middle East & Other
        }

        return region_mapping.get(value_str, value_str)

    def normalize_date(self, value):
        """Normalize date to YYYY-MM-DD format"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return None

        value_str = str(value).strip()

        # Handle different date formats
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',  # 2025-07-01
            r'(\d{1,2})/(\d{1,2})/(\d{2,4})',  # 7/1/25 or 07/01/2025
            r'(\d{2})/(\d{2})/(\d{2})',  # 05/16/25
            # July 1, 2025 or April 04, 2025
            r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})',
            r'([A-Za-z]+)\s+(\d{2}),?\s+(\d{4})'   # March 01, 2025
        ]

        for pattern in date_patterns:
            match = re.search(pattern, value_str)
            if match:
                if pattern == date_patterns[0]:  # YYYY-MM-DD
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                elif pattern in date_patterns[1:3]:  # M/D/Y formats
                    month, day, year = match.groups()
                    if len(year) == 2:
                        year = f"20{year}"
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                elif pattern in date_patterns[3:]:  # Month Day, Year
                    month_name, day, year = match.groups()
                    month_map = {
                        'january': '01', 'february': '02', 'march': '03', 'april': '04',
                        'may': '05', 'june': '06', 'july': '07', 'august': '08',
                        'september': '09', 'october': '10', 'november': '11', 'december': '12'
                    }
                    month_num = month_map.get(month_name.lower(), '01')
                    return f"{year}-{month_num}-{day.zfill(2)}"

        return value_str  # Return as-is if no pattern matches

    def normalize_website(self, value):
        """Clean and normalize website URLs"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return None

        url = str(value).strip().lower()

        # Remove http/https
        url = re.sub(r'^https?://', '', url)

        # Remove www
        url = re.sub(r'^www\.', '', url)

        # Remove trailing slash
        url = url.rstrip('/')

        return url

    def standardize_tech_stack(self, value):
        """Standardize tech stack signals"""
        if pd.isna(value) or str(value).lower() in ['nan', 'unknown', 'n/a', '']:
            return None

        # Split by common delimiters and clean
        delimiters = [';', ',', '|', '&']
        tech_list = [str(value)]

        for delimiter in delimiters:
            new_list = []
            for item in tech_list:
                new_list.extend(item.split(delimiter))
            tech_list = new_list

        # Clean and standardize each tech
        cleaned_tech = []
        for tech in tech_list:
            tech = tech.strip()
            if tech and tech.lower() not in ['unknown', 'n/a', 'nan']:
                # Capitalize properly
                tech = ' '.join(word.capitalize() for word in tech.split())
                cleaned_tech.append(tech)

        return ', '.join(cleaned_tech) if cleaned_tech else None

    def clean_data(self):
        """Main data cleaning pipeline"""
        print("Starting data cleaning pipeline...")

        # Create a copy for cleaning
        self.cleaned_df = self.df.copy()

        # Clean Employee Count
        print("Cleaning Employee Count...")
        self.cleaned_df['Employee_Count_Clean'] = self.cleaned_df['Employee Count'].apply(
            self.normalize_employee_count)

        # Clean Revenue
        print("Cleaning Revenue...")
        self.cleaned_df['Revenue_Clean'] = self.cleaned_df['Revenue'].apply(
            self.normalize_revenue)

        # Clean Region
        print("Cleaning Region...")
        self.cleaned_df['Region_Clean'] = self.cleaned_df['Region'].apply(
            self.normalize_region)

        # Clean Date
        print("Cleaning Last Marketing Touch...")
        self.cleaned_df['Last_Marketing_Touch_Clean'] = self.cleaned_df['Last Marketing Touch'].apply(
            self.normalize_date)

        # Clean Website
        print("Cleaning Website...")
        self.cleaned_df['Website_Clean'] = self.cleaned_df['Website'].apply(
            self.normalize_website)

        # Clean Tech Stack
        print("Cleaning Tech Stack...")
        self.cleaned_df['Tech_Stack_Clean'] = self.cleaned_df['Tech Stack Signals'].apply(
            self.standardize_tech_stack)

        # Handle missing SFDC IDs
        print("Handling missing SFDC Account IDs...")
        self.cleaned_df['SFDC_Account_ID_Clean'] = self.cleaned_df['SFDC Account ID'].fillna(
            'Missing')

        # Clean Lead Owner (remove test users)
        print("Cleaning Lead Owner...")
        self.cleaned_df['Lead_Owner_Clean'] = self.cleaned_df['Lead Owner'].apply(
            lambda x: 'Unassigned' if pd.isna(x) or 'test' in str(x).lower() or x == 'TBD' else x)

        # Standardize Intent Score
        print("Cleaning Intent Score...")
        self.cleaned_df['Intent_Score_Clean'] = pd.to_numeric(
            self.cleaned_df['Intent Score'], errors='coerce')

        print("Data cleaning completed!")
        return self.cleaned_df

    def generate_cleaning_report(self):
        """Generate a report on data cleaning results"""
        if self.cleaned_df is None:
            print("Please run clean_data() first")
            return

        print("\n" + "="*60)
        print("DATA CLEANING REPORT")
        print("="*60)

        # Before/After comparison for key fields
        fields_to_compare = [
            ('Employee Count', 'Employee_Count_Clean'),
            ('Revenue', 'Revenue_Clean'),
            ('Region', 'Region_Clean'),
            ('Website', 'Website_Clean')
        ]

        for original, cleaned in fields_to_compare:
            print(f"\n{original.upper()} CLEANING RESULTS:")
            print(f"Original unique values: {self.df[original].nunique()}")
            print(
                f"Cleaned unique values: {self.cleaned_df[cleaned].nunique()}")
            print(f"Original missing: {self.df[original].isna().sum()}")
            print(
                f"Cleaned missing/unknown: {(self.cleaned_df[cleaned].isna() | (self.cleaned_df[cleaned] == 'Unknown')).sum()}")

        # Save the cleaned dataset
        output_path = 'data/cleaned_diligent_dataset.csv'
        self.cleaned_df.to_csv(output_path, index=False)
        print(f"\nCleaned dataset saved to: {output_path}")

        return self.cleaned_df


def main():
    """Main execution function"""
    print("GTM Engineer Data Cleaning Pipeline")
    print("="*50)

    # Initialize cleaner
    file_path = 'data/Diligent_GTM_Engineer_Exercise_with_Instructions.xlsx'
    cleaner = DiligentDataCleaner(file_path)

    # Load and clean data
    cleaner.load_data()
    cleaned_df = cleaner.clean_data()
    cleaner.generate_cleaning_report()

    print("\nData cleaning pipeline completed successfully!")
    return cleaned_df


if __name__ == "__main__":
    main()
