#!/usr/bin/env python3
"""
GTM Engineer Data Analysis - ICP Scoring and Prioritization
Author: GTM Engineer Candidate
Date: September 2025

This script defines ICP archetypes and creates scoring logic to prioritize
accounts for the Diligent sales team based on firmographic and behavioral signals.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ICPScorer:
    def __init__(self, cleaned_data_path):
        self.df = pd.read_csv(cleaned_data_path)
        self.scored_df = None

        # Define ICP archetypes and scoring criteria
        self.icp_archetypes = {
            'Enterprise_Risk_Management': {
                'description': 'Large enterprises with complex risk management needs',
                'ideal_employee_range': ['1000+', '500-1,000'],
                'ideal_revenue': ['$100M', '$250M', '$1000M'],  # High revenue
                'target_industries': ['Financial Services', 'Healthcare', 'Energy', 'Manufacturing'],
                'key_solutions': ['Risk'],
                'high_value_roles': ['Chief Risk Officer', 'Risk Manager', 'Board Secretary'],
                'priority_certifications': ['SOX', 'PCI DSS', 'ISO27001'],
                'tech_stack_indicators': ['Salesforce', 'ServiceNow', 'Workday']
            },
            'Mid_Market_Compliance': {
                'description': 'Growing companies needing compliance frameworks',
                'ideal_employee_range': ['200-500', '500-1,000'],
                'ideal_revenue': ['$20M', '$100M'],
                'target_industries': ['Technology', 'Financial Services', 'Healthcare', 'Legal'],
                'key_solutions': ['Compliance'],
                'high_value_roles': ['General Counsel', 'Legal Counsel', 'Compliance Officer'],
                'priority_certifications': ['GDPR', 'HIPAA', 'ISO27001'],
                'tech_stack_indicators': ['HubSpot', 'Marketo', 'Pardot', 'Okta']
            },
            'Board_Governance': {
                'description': 'Organizations focused on board management and governance',
                'ideal_employee_range': ['200-500', '500-1,000', '1000+'],
                'ideal_revenue': ['$100M', '$250M', '$1000M'],
                'target_industries': ['Financial Services', 'Non-Profit', 'Legal', 'Government'],
                'key_solutions': ['Boards'],
                'high_value_roles': ['Board Secretary', 'Director of Security', 'General Counsel'],
                'priority_certifications': ['SOX', 'GDPR'],
                'tech_stack_indicators': ['Salesforce', 'Workday', 'ServiceNow']
            }
        }

    def calculate_firmographic_score(self, row):
        """Calculate firmographic fit score (0-40 points)"""
        score = 0

        # Employee Count Score (0-15 points)
        employee_count = row['Employee_Count_Clean']
        if employee_count in ['1000+']:
            score += 15
        elif employee_count in ['500-1,000', '500-1000']:
            score += 12
        elif employee_count in ['200-500']:
            score += 10
        elif employee_count in ['50-200']:
            score += 5

        # Revenue Score (0-15 points)
        revenue = row['Revenue_Clean']
        if revenue in ['$1000M', '$250M']:
            score += 15
        elif revenue in ['$100M']:
            score += 12
        elif revenue in ['$20M']:
            score += 8
        elif revenue in ['$5M']:
            score += 4

        # Industry Score (0-10 points)
        industry = row['Industry']
        high_value_industries = ['Financial Services',
                                 'Healthcare', 'Energy', 'Manufacturing', 'Legal']
        if industry in high_value_industries:
            score += 10
        elif industry in ['Technology', 'Government']:
            score += 7
        else:
            score += 3

        return score

    def calculate_solution_fit_score(self, row):
        """Calculate solution interest and role fit score (0-25 points)"""
        score = 0

        # Solution Interest Score (0-15 points)
        solution_interest = row['Solution Interest']
        if solution_interest == 'Risk':
            score += 15  # Highest value solution
        elif solution_interest == 'Compliance':
            score += 12
        elif solution_interest == 'Boards':
            score += 10
        else:
            score += 5

        # Contact Role Score (0-10 points)
        role = str(row['Contact Role/Title']).lower()
        high_value_roles = ['chief risk officer', 'risk manager', 'board secretary',
                            'general counsel', 'legal counsel', 'compliance officer']
        medium_value_roles = ['director of security',
                              'it director', 'cfo', 'ciso']

        if any(hvr in role for hvr in high_value_roles):
            score += 10
        elif any(mvr in role for mvr in medium_value_roles):
            score += 7
        else:
            score += 3

        return score

    def calculate_intent_signals_score(self, row):
        """Calculate intent and engagement signals score (0-20 points)"""
        score = 0

        # Intent Score (0-10 points)
        intent_score = row['Intent_Score_Clean']
        if pd.notna(intent_score):
            if intent_score >= 80:
                score += 10
            elif intent_score >= 60:
                score += 8
            elif intent_score >= 40:
                score += 6
            else:
                score += 3

        # Lead Source Score (0-5 points)
        lead_source = row['Lead Source']
        if lead_source == 'Referral':
            score += 5
        elif lead_source == 'Event':
            score += 4
        elif lead_source == 'Web':
            score += 3
        else:
            score += 2

        # Recency Score (0-5 points)
        last_touch = row['Last_Marketing_Touch_Clean']
        if pd.notna(last_touch):
            try:
                touch_date = pd.to_datetime(last_touch)
                days_ago = (datetime.now() - touch_date).days
                if days_ago <= 30:
                    score += 5
                elif days_ago <= 90:
                    score += 3
                else:
                    score += 1
            except:
                score += 1

        return score

    def calculate_tech_compliance_score(self, row):
        """Calculate technology and compliance readiness score (0-15 points)"""
        score = 0

        # Technology Stack Score (0-8 points)
        tech_stack = str(row['Tech_Stack_Clean']).lower()
        enterprise_tech = ['salesforce', 'servicenow', 'workday', 'okta']
        mid_market_tech = ['hubspot', 'marketo', 'pardot']

        if any(et in tech_stack for et in enterprise_tech):
            score += 8
        elif any(mt in tech_stack for mt in mid_market_tech):
            score += 5
        elif tech_stack != 'nan':
            score += 3

        # Compliance Certifications Score (0-7 points)
        certifications = str(row['Compliance Certifications']).lower()
        high_value_certs = ['sox', 'pci dss', 'iso27001']
        medium_value_certs = ['gdpr', 'hipaa']

        if any(hvc in certifications for hvc in high_value_certs):
            score += 7
        elif any(mvc in certifications for mvc in medium_value_certs):
            score += 5
        elif certifications != 'nan':
            score += 2

        return score

    def assign_icp_archetype(self, row):
        """Assign the best-fit ICP archetype based on characteristics"""
        # Score each archetype
        archetype_scores = {}

        for archetype_name, criteria in self.icp_archetypes.items():
            score = 0

            # Employee range fit
            if row['Employee_Count_Clean'] in criteria['ideal_employee_range']:
                score += 3

            # Revenue fit
            if row['Revenue_Clean'] in criteria['ideal_revenue']:
                score += 3

            # Industry fit
            if row['Industry'] in criteria['target_industries']:
                score += 3

            # Solution interest fit
            if row['Solution Interest'] in criteria['key_solutions']:
                score += 4

            # Role fit
            role = str(row['Contact Role/Title']).lower()
            if any(hvr in role for hvr in [r.lower() for r in criteria['high_value_roles']]):
                score += 3

            archetype_scores[archetype_name] = score

        # Return the highest scoring archetype
        best_archetype = max(archetype_scores, key=archetype_scores.get)
        best_score = archetype_scores[best_archetype]

        # Only assign if score is meaningful (>=6)
        if best_score >= 6:
            return best_archetype
        else:
            return 'Other'

    def calculate_total_icp_score(self):
        """Calculate comprehensive ICP scores for all accounts"""
        print("Calculating ICP scores...")

        # Calculate component scores
        self.df['Firmographic_Score'] = self.df.apply(
            self.calculate_firmographic_score, axis=1)
        self.df['Solution_Fit_Score'] = self.df.apply(
            self.calculate_solution_fit_score, axis=1)
        self.df['Intent_Signals_Score'] = self.df.apply(
            self.calculate_intent_signals_score, axis=1)
        self.df['Tech_Compliance_Score'] = self.df.apply(
            self.calculate_tech_compliance_score, axis=1)

        # Calculate total score (0-100)
        self.df['Total_ICP_Score'] = (
            self.df['Firmographic_Score'] +
            self.df['Solution_Fit_Score'] +
            self.df['Intent_Signals_Score'] +
            self.df['Tech_Compliance_Score']
        )

        # Assign ICP archetypes
        self.df['ICP_Archetype'] = self.df.apply(
            self.assign_icp_archetype, axis=1)

        # Create priority tiers
        self.df['Priority_Tier'] = pd.cut(
            self.df['Total_ICP_Score'],
            bins=[0, 40, 60, 80, 100],
            labels=['Low', 'Medium', 'High', 'Critical'],
            include_lowest=True
        )

        self.scored_df = self.df.copy()
        print("ICP scoring completed!")

        return self.scored_df

    def generate_prioritization_report(self):
        """Generate prioritization analysis and recommendations"""
        if self.scored_df is None:
            print("Please run calculate_total_icp_score() first")
            return

        print("\n" + "="*60)
        print("ICP PRIORITIZATION REPORT")
        print("="*60)

        # Overall score distribution
        print("\nSCORE DISTRIBUTION:")
        print(
            f"Average ICP Score: {self.scored_df['Total_ICP_Score'].mean():.1f}")
        print(
            f"Median ICP Score: {self.scored_df['Total_ICP_Score'].median():.1f}")
        print(
            f"Top 10% Threshold: {self.scored_df['Total_ICP_Score'].quantile(0.9):.1f}")

        # Priority tier breakdown
        print("\nPRIORITY TIER DISTRIBUTION:")
        priority_dist = self.scored_df['Priority_Tier'].value_counts()
        for tier, count in priority_dist.items():
            percentage = (count / len(self.scored_df)) * 100
            print(f"{tier}: {count} accounts ({percentage:.1f}%)")

        # ICP archetype distribution
        print("\nICP ARCHETYPE DISTRIBUTION:")
        archetype_dist = self.scored_df['ICP_Archetype'].value_counts()
        for archetype, count in archetype_dist.items():
            percentage = (count / len(self.scored_df)) * 100
            print(f"{archetype}: {count} accounts ({percentage:.1f}%)")

        # Top 50 accounts for sales prioritization
        top_accounts = self.scored_df.nlargest(50, 'Total_ICP_Score')[
            ['Company Name', 'Industry', 'Employee_Count_Clean', 'Revenue_Clean',
             'Solution Interest', 'Contact Role/Title', 'ICP_Archetype',
             'Total_ICP_Score', 'Priority_Tier', 'Region_Clean']
        ]

        print("\nTOP 50 PRIORITY ACCOUNTS:")
        print(top_accounts.to_string(index=False, max_colwidth=20))

        # Save prioritized accounts
        output_path = 'deliverables/prioritized_accounts.csv'
        self.scored_df.to_csv(output_path, index=False)
        print(f"\nFull prioritized dataset saved to: {output_path}")

        # Save top 100 for sales team
        top_100_path = 'deliverables/top_100_priority_accounts.csv'
        self.scored_df.nlargest(100, 'Total_ICP_Score').to_csv(
            top_100_path, index=False)
        print(f"Top 100 priority accounts saved to: {top_100_path}")

        return top_accounts

    def create_scoring_visualization(self):
        """Create visualizations for scoring analysis"""
        if self.scored_df is None:
            print("Please run calculate_total_icp_score() first")
            return

        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('ICP Scoring Analysis Dashboard',
                     fontsize=16, fontweight='bold')

        # 1. Score distribution histogram
        axes[0, 0].hist(self.scored_df['Total_ICP_Score'], bins=20,
                        alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].axvline(self.scored_df['Total_ICP_Score'].mean(
        ), color='red', linestyle='--', label='Mean')
        axes[0, 0].set_title('Total ICP Score Distribution')
        axes[0, 0].set_xlabel('ICP Score')
        axes[0, 0].set_ylabel('Number of Accounts')
        axes[0, 0].legend()

        # 2. Priority tier distribution
        priority_counts = self.scored_df['Priority_Tier'].value_counts()
        axes[0, 1].pie(priority_counts.values,
                       labels=priority_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Priority Tier Distribution')

        # 3. ICP Archetype vs Score
        archetype_scores = self.scored_df.groupby(
            'ICP_Archetype')['Total_ICP_Score'].mean().sort_values(ascending=False)
        axes[1, 0].bar(range(len(archetype_scores)),
                       archetype_scores.values, color='lightcoral')
        axes[1, 0].set_title('Average Score by ICP Archetype')
        axes[1, 0].set_xlabel('ICP Archetype')
        axes[1, 0].set_ylabel('Average ICP Score')
        axes[1, 0].set_xticks(range(len(archetype_scores)))
        axes[1, 0].set_xticklabels(archetype_scores.index, rotation=45)

        # 4. Score components breakdown
        score_components = ['Firmographic_Score', 'Solution_Fit_Score',
                            'Intent_Signals_Score', 'Tech_Compliance_Score']
        component_means = [self.scored_df[comp].mean()
                           for comp in score_components]
        axes[1, 1].bar(range(len(score_components)),
                       component_means, color='lightgreen')
        axes[1, 1].set_title('Average Score by Component')
        axes[1, 1].set_xlabel('Score Component')
        axes[1, 1].set_ylabel('Average Score')
        axes[1, 1].set_xticks(range(len(score_components)))
        axes[1, 1].set_xticklabels([comp.replace('_', '\n')
                                   for comp in score_components], rotation=45)

        plt.tight_layout()
        plt.savefig('deliverables/icp_scoring_dashboard.png',
                    dpi=300, bbox_inches='tight')
        plt.show()

        print("Scoring visualization saved to deliverables/icp_scoring_dashboard.png")


def main():
    """Main execution function"""
    print("GTM Engineer ICP Scoring and Prioritization")
    print("="*50)

    # Initialize scorer with cleaned data
    cleaned_data_path = 'data/cleaned_diligent_dataset.csv'
    scorer = ICPScorer(cleaned_data_path)

    # Calculate scores and generate reports
    scored_df = scorer.calculate_total_icp_score()
    top_accounts = scorer.generate_prioritization_report()
    scorer.create_scoring_visualization()

    print("\nICP scoring and prioritization completed successfully!")
    return scored_df, top_accounts


if __name__ == "__main__":
    main()
