#!/usr/bin/env python3
"""
Data Enrichment & Quality Assurance Example
Demonstrates how to enrich missing data and validate data quality
"""

import pandas as pd
import time
from datetime import datetime


class DataEnrichmentEngine:
    """
    Example data enrichment and quality assurance system
    Shows how to fill missing firmographic data and validate records
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.enrichment_stats = {
            'records_processed': 0,
            'records_enriched': 0,
            'api_calls_made': 0,
            'errors_encountered': 0
        }

    def enrich_company_data(self, company_name, website=None):
        """
        Example enrichment function (pseudo-API call)
        In production, this would call ZoomInfo, Clearbit, or similar APIs
        """
        try:
            # Simulate API enrichment (replace with actual API calls)
            enriched_data = self._simulate_api_call(company_name, website)

            self.enrichment_stats['api_calls_made'] += 1

            if enriched_data:
                self.enrichment_stats['records_enriched'] += 1
                return enriched_data

            return None

        except Exception as e:
            self.enrichment_stats['errors_encountered'] += 1
            print(f"Enrichment error for {company_name}: {e}")
            return None

    def _simulate_api_call(self, company_name, website):
        """
        Simulates external API enrichment response
        Replace with actual API integration (ZoomInfo, Clearbit, etc.)
        """

        # Simulate API response delay
        time.sleep(0.1)

        # Mock enrichment data based on company patterns
        enrichment_data = {}

        # Employee count enrichment logic
        if 'Corp' in company_name or 'Industries' in company_name:
            enrichment_data['estimated_employees'] = '1000+'
            enrichment_data['estimated_revenue'] = '$250M'
        elif 'Tech' in company_name or 'Systems' in company_name:
            enrichment_data['estimated_employees'] = '500-1,000'
            enrichment_data['estimated_revenue'] = '$100M'
        elif 'Group' in company_name or 'Ventures' in company_name:
            enrichment_data['estimated_employees'] = '200-500'
            enrichment_data['estimated_revenue'] = '$50M'
        else:
            enrichment_data['estimated_employees'] = '50-200'
            enrichment_data['estimated_revenue'] = '$20M'

        # Industry classification
        if 'Bank' in company_name or 'Financial' in company_name:
            enrichment_data['industry_classification'] = 'Financial Services'
        elif 'Electric' in company_name or 'Energy' in company_name:
            enrichment_data['industry_classification'] = 'Energy'
        elif 'Tech' in company_name or 'Systems' in company_name:
            enrichment_data['industry_classification'] = 'Technology'
        else:
            enrichment_data['industry_classification'] = 'Other'

        # Technology stack indicators
        tech_indicators = ['Salesforce', 'HubSpot',
                           'Marketo', 'ServiceNow', 'Workday']
        import random
        enrichment_data['tech_stack_detected'] = random.choice(tech_indicators)

        # Compliance indicators
        compliance_options = ['SOX', 'GDPR', 'HIPAA', 'ISO27001', 'PCI DSS']
        enrichment_data['compliance_indicators'] = random.choice(
            compliance_options)

        # LinkedIn company URL
        if website:
            company_slug = company_name.lower().replace(' ', '-').replace('_', '-')
            enrichment_data['linkedin_url'] = f"https://linkedin.com/company/{company_slug}"

        return enrichment_data


class DataQualityValidator:
    """
    Quality assurance system for validating enriched data
    """

    def __init__(self):
        self.validation_rules = {
            'employee_count': self._validate_employee_count,
            'revenue': self._validate_revenue,
            'industry': self._validate_industry,
            'website': self._validate_website,
            'email_domain': self._validate_email_domain
        }

        self.quality_scores = {}

    def validate_record(self, record):
        """
        Validates a single record against quality rules
        Returns quality score (0-100) and list of issues
        """
        issues = []
        quality_score = 100

        for field, validator in self.validation_rules.items():
            if field in record:
                is_valid, issue = validator(record[field])
                if not is_valid:
                    issues.append(f"{field}: {issue}")
                    quality_score -= 10  # Deduct 10 points per issue

        # Bonus points for completeness
        completeness = len([v for v in record.values() if v and str(
            v).lower() not in ['nan', 'unknown', 'n/a']]) / len(record)
        completeness_bonus = int(completeness * 20)  # Up to 20 bonus points

        final_score = min(100, quality_score + completeness_bonus)

        return final_score, issues

    def _validate_employee_count(self, value):
        """Validate employee count format"""
        if not value or str(value).lower() in ['nan', 'unknown']:
            return False, "Missing employee count"

        valid_formats = ['1000+', '500-1,000', '200-500', '50-200', '1-50']
        if str(value) not in valid_formats:
            return False, f"Invalid format: {value}"

        return True, None

    def _validate_revenue(self, value):
        """Validate revenue format"""
        if not value or str(value).lower() in ['nan', 'unknown']:
            return False, "Missing revenue"

        if not str(value).startswith('$') or not str(value).endswith('M'):
            return False, f"Invalid format: {value} (should be $XXXm)"

        return True, None

    def _validate_industry(self, value):
        """Validate industry classification"""
        if not value or str(value).lower() in ['nan', 'unknown']:
            return False, "Missing industry"

        valid_industries = [
            'Financial Services', 'Technology', 'Healthcare', 'Energy',
            'Manufacturing', 'Legal', 'Education', 'Government', 'Non-Profit'
        ]

        if value not in valid_industries:
            return False, f"Non-standard industry: {value}"

        return True, None

    def _validate_website(self, value):
        """Validate website format"""
        if not value:
            return False, "Missing website"

        # Basic URL validation
        if not ('.' in str(value) and len(str(value)) > 4):
            return False, f"Invalid website format: {value}"

        return True, None

    def _validate_email_domain(self, value):
        """Validate email domain format"""
        if not value:
            return False, "Missing email domain"

        if not ('.' in str(value) and '@' not in str(value)):
            return False, f"Invalid domain format: {value}"

        return True, None


def enrichment_example():
    """
    Example workflow showing data enrichment and quality validation
    """
    print("Data Enrichment & QA Example")
    print("=" * 50)

    # Load sample data with missing information
    sample_data = [
        {
            'Company Name': 'Stark Industries_740',
            'Website': 'starkindustries_740.com',
            'Employee Count': None,  # Missing
            'Revenue': None,  # Missing
            'Industry': 'Financial Services',
            'Email Domain': 'starkindustries_740.com'
        },
        {
            'Company Name': 'Wonka Tech_653',
            'Website': 'wonkatech_653.io',
            'Employee Count': 'Unknown',  # Needs cleaning
            'Revenue': '€20M',  # Needs normalization
            'Industry': 'Energy',
            'Email Domain': 'wonkatech_653.io'
        },
        {
            'Company Name': 'Blue Sun Corp_607',
            'Website': None,  # Missing
            'Employee Count': '200-500',
            'Revenue': '$20M',
            'Industry': 'Manufacturing',
            'Email Domain': None  # Missing
        }
    ]

    # Initialize enrichment and validation engines
    enricher = DataEnrichmentEngine()
    validator = DataQualityValidator()

    print("\nProcessing records...")
    enriched_records = []

    for i, record in enumerate(sample_data):
        print(f"\n--- Record {i+1}: {record['Company Name']} ---")

        # Step 1: Validate original data quality
        original_score, original_issues = validator.validate_record(record)
        print(f"Original Quality Score: {original_score}/100")
        if original_issues:
            print(f"Issues found: {original_issues}")

        # Step 2: Enrich missing data
        enriched_data = enricher.enrich_company_data(
            record['Company Name'],
            record.get('Website')
        )

        if enriched_data:
            print(f"Enrichment successful!")
            print(
                f"  - Estimated Employees: {enriched_data.get('estimated_employees')}")
            print(
                f"  - Estimated Revenue: {enriched_data.get('estimated_revenue')}")
            print(
                f"  - Industry Classification: {enriched_data.get('industry_classification')}")
            print(
                f"  - Tech Stack: {enriched_data.get('tech_stack_detected')}")
            print(
                f"  - Compliance: {enriched_data.get('compliance_indicators')}")

            # Merge enriched data with original record
            enriched_record = record.copy()
            if not enriched_record.get('Employee Count'):
                enriched_record['Employee Count'] = enriched_data.get(
                    'estimated_employees')
            if not enriched_record.get('Revenue'):
                enriched_record['Revenue'] = enriched_data.get(
                    'estimated_revenue')
            if enriched_data.get('tech_stack_detected'):
                enriched_record['Tech Stack'] = enriched_data.get(
                    'tech_stack_detected')
            if enriched_data.get('compliance_indicators'):
                enriched_record['Compliance'] = enriched_data.get(
                    'compliance_indicators')

            # Step 3: Validate enriched data quality
            final_score, final_issues = validator.validate_record(
                enriched_record)
            print(
                f"Final Quality Score: {final_score}/100 (Improvement: +{final_score - original_score})")

            enriched_records.append(enriched_record)
        else:
            print("Enrichment failed - using original data")
            enriched_records.append(record)

        enricher.enrichment_stats['records_processed'] += 1

    # Print final statistics
    print(f"\n{'='*50}")
    print("ENRICHMENT SUMMARY")
    print(f"{'='*50}")
    print(
        f"Records Processed: {enricher.enrichment_stats['records_processed']}")
    print(f"Records Enriched: {enricher.enrichment_stats['records_enriched']}")
    print(f"API Calls Made: {enricher.enrichment_stats['api_calls_made']}")
    print(
        f"Errors Encountered: {enricher.enrichment_stats['errors_encountered']}")
    print(
        f"Success Rate: {(enricher.enrichment_stats['records_enriched'] / enricher.enrichment_stats['records_processed']) * 100:.1f}%")

    return enriched_records

# Quality Assurance Checks


def qa_validation_example():
    """
    Example of automated quality assurance checks
    """
    print(f"\n{'='*50}")
    print("QUALITY ASSURANCE VALIDATION")
    print(f"{'='*50}")

    # Load the actual prioritized dataset for QA
    try:
        df = pd.read_csv('../deliverables/prioritized_accounts.csv')

        validator = DataQualityValidator()

        # Sample QA checks
        qa_results = {
            'total_records': len(df),
            'records_with_scores': len(df[df['Total_ICP_Score'].notna()]),
            'records_missing_employee_data': len(df[df['Employee_Count_Clean'].isin(['Unknown', None])]),
            'records_missing_revenue_data': len(df[df['Revenue_Clean'].isin(['Unknown', None])]),
            'records_with_high_scores': len(df[df['Total_ICP_Score'] >= 80]),
            'average_quality_score': 0
        }

        # Calculate average quality score for sample
        sample_records = df.head(10).to_dict('records')
        quality_scores = []

        for record in sample_records:
            score, issues = validator.validate_record(record)
            quality_scores.append(score)

        qa_results['average_quality_score'] = sum(
            quality_scores) / len(quality_scores)

        print(f"QA Results:")
        for key, value in qa_results.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

        # Flag potential data quality issues
        issues_found = []
        if qa_results['records_missing_employee_data'] > qa_results['total_records'] * 0.15:
            issues_found.append("High percentage of missing employee data")
        if qa_results['records_missing_revenue_data'] > qa_results['total_records'] * 0.15:
            issues_found.append("High percentage of missing revenue data")
        if qa_results['average_quality_score'] < 75:
            issues_found.append("Low average data quality score")

        if issues_found:
            print(f"\n⚠️  Quality Issues Detected:")
            for issue in issues_found:
                print(f"   - {issue}")
        else:
            print(f"\n✅ Data quality meets standards")

    except FileNotFoundError:
        print("Prioritized accounts file not found - run main scoring script first")


if __name__ == "__main__":
    # Run enrichment example
    enriched_data = enrichment_example()

    # Run QA validation
    qa_validation_example()

    print(f"\n{'='*50}")
    print("PRODUCTION RECOMMENDATIONS")
    print(f"{'='*50}")
    print("1. Implement ZoomInfo API for employee count enrichment")
    print("2. Use Clearbit for revenue and industry classification")
    print("3. Connect Bombora for real-time intent data updates")
    print("4. Set up automated QA checks in data pipeline")
    print("5. Create alerts for data quality score drops below 80%")
    print("6. Schedule weekly enrichment runs for new leads")
    print("\nExample API Integration Code:")
    print("""
# ZoomInfo API Example
def enrich_with_zoominfo(company_name, api_key):
    url = "https://api.zoominfo.com/lookup/company"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"companyName": company_name}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'employees': data.get('employeeCount'),
            'revenue': data.get('revenue'),
            'industry': data.get('industry')
        }
    return None
    """)
