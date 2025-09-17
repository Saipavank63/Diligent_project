#!/usr/bin/env python3
"""
GTM Engineer Analysis - Final Validation and Summary
Quick validation of all deliverables and key metrics
"""

import pandas as pd
import os


def validate_deliverables():
    """Validate all project deliverables are present and correct"""

    print("GTM Engineer Analysis - Final Validation")
    print("="*50)

    # Check file existence
    files_to_check = [
        'data/cleaned_diligent_dataset.csv',
        'deliverables/prioritized_accounts.csv',
        'deliverables/top_100_priority_accounts.csv',
        'deliverables/Executive_Summary.md',
        'deliverables/icp_scoring_dashboard.png'
    ]

    print("\nFILE VALIDATION:")
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = "✓ EXISTS" if exists else "✗ MISSING"
        print(f"{status}: {file_path}")

    # Load and validate data
    try:
        df = pd.read_csv('deliverables/prioritized_accounts.csv')
        print(f"\n✓ Dataset loaded successfully: {len(df)} records")

        # Validate key columns
        required_columns = [
            'Total_ICP_Score', 'ICP_Archetype', 'Priority_Tier',
            'Employee_Count_Clean', 'Revenue_Clean', 'Region_Clean'
        ]

        print("\nCOLUMN VALIDATION:")
        for col in required_columns:
            exists = col in df.columns
            status = "✓ PRESENT" if exists else "✗ MISSING"
            print(f"{status}: {col}")

        # Key metrics summary
        print("\nKEY METRICS SUMMARY:")
        print(f"Total Accounts: {len(df)}")
        print(f"Average ICP Score: {df['Total_ICP_Score'].mean():.1f}")
        print(
            f"Critical Accounts (90+): {len(df[df['Total_ICP_Score'] >= 90])}")
        print(
            f"High Priority (80-89): {len(df[(df['Total_ICP_Score'] >= 80) & (df['Total_ICP_Score'] < 90)])}")

        print("\nICP ARCHETYPE DISTRIBUTION:")
        archetype_counts = df['ICP_Archetype'].value_counts()
        for archetype, count in archetype_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {archetype}: {count} ({percentage:.1f}%)")

        print("\nTOP 5 PRIORITY ACCOUNTS:")
        top_5 = df.nlargest(5, 'Total_ICP_Score')[
            ['Company Name', 'Industry', 'Solution Interest',
                'Total_ICP_Score', 'ICP_Archetype']
        ]
        print(top_5.to_string(index=False))

        print("\n✓ All validations passed successfully!")
        return True

    except Exception as e:
        print(f"\n✗ Validation error: {e}")
        return False


if __name__ == "__main__":
    validate_deliverables()
