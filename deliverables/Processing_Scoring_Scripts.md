# GTM Engineer Data Processing & Scoring Scripts

## Overview

This document provides the pseudocode and key logic for the Diligent GTM data processing and ICP scoring pipeline.

---

## Script 1: Data Exploration Pipeline

### Purpose

Initial data discovery and quality assessment

### Pseudocode:

```
FUNCTION explore_data():
    // Load Excel file with multiple sheets
    excel_file = LOAD_EXCEL("dataset.xlsx")
    dataset = READ_SHEET(excel_file, "Dataset")

    // Basic data profiling
    PRINT dataset.shape, dataset.columns

    // Data quality assessment
    FOR each column IN dataset:
        missing_count = COUNT_NULL(column)
        missing_percentage = (missing_count / total_rows) * 100
        unique_values = COUNT_UNIQUE(column)
        STORE quality_metrics

    // Field categorization
    company_fields = FILTER columns WHERE name CONTAINS ["company", "website", "domain"]
    firmographic_fields = FILTER columns WHERE name CONTAINS ["industry", "employee", "revenue"]
    gtm_fields = FILTER columns WHERE name CONTAINS ["interest", "source", "intent", "touch"]

    // Generate quality report
    SAVE quality_assessment TO "analysis/data_quality_assessment.csv"
    SAVE sample_data TO "analysis/sample_raw_data.csv"
END FUNCTION
```

### Key Outputs:

- Data structure analysis (1000 rows × 22 columns)
- Quality assessment showing 19.5% missing employee data, 19.2% missing revenue
- Field categorization for targeted cleaning

---

## Script 2: Data Cleaning Pipeline

### Purpose

Normalize and standardize messy data formats

### Pseudocode:

```
CLASS DataCleaner:

    FUNCTION normalize_employee_count(value):
        IF value IS null OR value IN ["unknown", "n/a"]:
            RETURN "Unknown"

        value = CONVERT_TO_STRING(value).lowercase()

        // Handle text descriptions
        IF "five hundred" IN value:
            RETURN "500-1,000"
        IF "approx 800" IN value:
            RETURN "500-1,000"

        // Standardize range formats
        IF " to " IN value:
            parts = SPLIT(value, " to ")
            RETURN parts[0] + "-" + parts[1]

        RETURN CAPITALIZE(value)

    FUNCTION normalize_revenue(value):
        IF value IS null:
            RETURN "Unknown"

        // Remove currency symbols
        clean_value = REMOVE_CHARACTERS(value, ["€", "$", ","])

        // Extract numeric part
        number = EXTRACT_NUMBER(clean_value)

        // Handle scale indicators
        IF "M" IN value:
            RETURN "$" + number + "M"
        IF "B" IN value:
            RETURN "$" + (number * 1000) + "M"  // Convert billions to millions
        IF LENGTH(number) >= 7:  // Raw numbers like 5000000
            RETURN "$" + (number / 1000000) + "M"

        RETURN "$" + number + "M"

    FUNCTION normalize_region(value):
        region_mapping = {
            "AMS": "Americas",
            "EMEA": "EMEA",
            "APAC": "APAC",
            "UKI": "UK & Ireland",
            "DACH": "DACH",
            "FR": "France",
            "MDO": "MEA"
        }

        RETURN region_mapping.get(value, "Unknown")

    FUNCTION normalize_date(value):
        date_patterns = [
            "YYYY-MM-DD",     // 2025-07-01
            "M/D/YY",         // 7/1/25
            "Month D, YYYY"   // July 1, 2025
        ]

        FOR each pattern IN date_patterns:
            IF MATCH(value, pattern):
                RETURN CONVERT_TO_STANDARD_FORMAT(value, "YYYY-MM-DD")

        RETURN value  // Return as-is if no pattern matches

    FUNCTION clean_pipeline():
        // Apply all cleaning functions
        dataset['Employee_Count_Clean'] = APPLY(normalize_employee_count, dataset['Employee Count'])
        dataset['Revenue_Clean'] = APPLY(normalize_revenue, dataset['Revenue'])
        dataset['Region_Clean'] = APPLY(normalize_region, dataset['Region'])
        dataset['Date_Clean'] = APPLY(normalize_date, dataset['Last Marketing Touch'])

        SAVE dataset TO "data/cleaned_diligent_dataset.csv"
END CLASS
```

### Key Transformations:

- Employee ranges: "five hundred" → "500-1,000"
- Revenue: "€20M" → "$20M", "5000000" → "$5M"
- Regions: "AMS" → "Americas", "FR" → "France"
- Dates: All formats → "YYYY-MM-DD"

---

## Script 3: ICP Scoring Engine

### Purpose

Calculate comprehensive ICP fit scores and assign priority tiers

### Pseudocode:

```
CLASS ICPScorer:

    // Define ICP archetypes with scoring criteria
    icp_archetypes = {
        "Enterprise_Risk_Management": {
            "ideal_employee_range": ["1000+", "500-1,000"],
            "ideal_revenue": ["$100M", "$250M", "$1000M"],
            "target_industries": ["Financial Services", "Healthcare", "Energy"],
            "key_solutions": ["Risk"],
            "high_value_roles": ["Chief Risk Officer", "Risk Manager", "Board Secretary"]
        },
        "Mid_Market_Compliance": {
            "ideal_employee_range": ["200-500", "500-1,000"],
            "ideal_revenue": ["$20M", "$100M"],
            "target_industries": ["Technology", "Financial Services", "Legal"],
            "key_solutions": ["Compliance"],
            "high_value_roles": ["General Counsel", "Legal Counsel", "Compliance Officer"]
        },
        "Board_Governance": {
            "ideal_employee_range": ["200-500", "500-1,000", "1000+"],
            "ideal_revenue": ["$100M", "$250M", "$1000M"],
            "target_industries": ["Financial Services", "Non-Profit", "Legal"],
            "key_solutions": ["Boards"],
            "high_value_roles": ["Board Secretary", "Director of Security"]
        }
    }

    FUNCTION calculate_firmographic_score(account):
        score = 0

        // Employee Count (0-15 points)
        IF account.employee_count == "1000+":
            score += 15
        ELSE IF account.employee_count IN ["500-1,000"]:
            score += 12
        ELSE IF account.employee_count IN ["200-500"]:
            score += 10
        ELSE IF account.employee_count IN ["50-200"]:
            score += 5

        // Revenue (0-15 points)
        IF account.revenue IN ["$1000M", "$250M"]:
            score += 15
        ELSE IF account.revenue == "$100M":
            score += 12
        ELSE IF account.revenue == "$20M":
            score += 8
        ELSE IF account.revenue == "$5M":
            score += 4

        // Industry (0-10 points)
        high_value_industries = ["Financial Services", "Healthcare", "Energy", "Manufacturing", "Legal"]
        IF account.industry IN high_value_industries:
            score += 10
        ELSE IF account.industry IN ["Technology", "Government"]:
            score += 7
        ELSE:
            score += 3

        RETURN score

    FUNCTION calculate_solution_fit_score(account):
        score = 0

        // Solution Interest (0-15 points)
        IF account.solution_interest == "Risk":
            score += 15  // Highest value solution
        ELSE IF account.solution_interest == "Compliance":
            score += 12
        ELSE IF account.solution_interest == "Boards":
            score += 10
        ELSE:
            score += 5

        // Contact Role (0-10 points)
        high_value_roles = ["chief risk officer", "risk manager", "board secretary", "general counsel"]
        IF ANY(role IN account.contact_role.lowercase() FOR role IN high_value_roles):
            score += 10
        ELSE IF ANY(role IN account.contact_role.lowercase() FOR role IN ["director", "manager", "cfo"]):
            score += 7
        ELSE:
            score += 3

        RETURN score

    FUNCTION calculate_intent_signals_score(account):
        score = 0

        // Intent Score (0-10 points)
        IF account.intent_score >= 80:
            score += 10
        ELSE IF account.intent_score >= 60:
            score += 8
        ELSE IF account.intent_score >= 40:
            score += 6
        ELSE IF account.intent_score IS NOT null:
            score += 3

        // Lead Source (0-5 points)
        source_scores = {
            "Referral": 5,
            "Event": 4,
            "Web": 3,
            "Purchased": 2
        }
        score += source_scores.get(account.lead_source, 2)

        // Recency (0-5 points)
        days_since_touch = CALCULATE_DAYS(today, account.last_marketing_touch)
        IF days_since_touch <= 30:
            score += 5
        ELSE IF days_since_touch <= 90:
            score += 3
        ELSE:
            score += 1

        RETURN score

    FUNCTION calculate_tech_compliance_score(account):
        score = 0

        // Technology Stack (0-8 points)
        enterprise_tech = ["salesforce", "servicenow", "workday", "okta"]
        mid_market_tech = ["hubspot", "marketo", "pardot"]

        IF ANY(tech IN account.tech_stack.lowercase() FOR tech IN enterprise_tech):
            score += 8
        ELSE IF ANY(tech IN account.tech_stack.lowercase() FOR tech IN mid_market_tech):
            score += 5
        ELSE IF account.tech_stack IS NOT null:
            score += 3

        // Compliance Certifications (0-7 points)
        high_value_certs = ["sox", "pci dss", "iso27001"]
        medium_value_certs = ["gdpr", "hipaa"]

        IF ANY(cert IN account.certifications.lowercase() FOR cert IN high_value_certs):
            score += 7
        ELSE IF ANY(cert IN account.certifications.lowercase() FOR cert IN medium_value_certs):
            score += 5
        ELSE IF account.certifications IS NOT null:
            score += 2

        RETURN score

    FUNCTION assign_icp_archetype(account):
        best_fit_score = 0
        best_archetype = "Other"

        FOR archetype_name, criteria IN icp_archetypes:
            fit_score = 0

            // Score fit against archetype criteria
            IF account.employee_count IN criteria.ideal_employee_range:
                fit_score += 3
            IF account.revenue IN criteria.ideal_revenue:
                fit_score += 3
            IF account.industry IN criteria.target_industries:
                fit_score += 3
            IF account.solution_interest IN criteria.key_solutions:
                fit_score += 4
            IF ANY(role IN account.contact_role FOR role IN criteria.high_value_roles):
                fit_score += 3

            IF fit_score > best_fit_score AND fit_score >= 6:
                best_fit_score = fit_score
                best_archetype = archetype_name

        RETURN best_archetype

    FUNCTION calculate_total_scores():
        FOR each account IN dataset:
            account.firmographic_score = calculate_firmographic_score(account)
            account.solution_fit_score = calculate_solution_fit_score(account)
            account.intent_signals_score = calculate_intent_signals_score(account)
            account.tech_compliance_score = calculate_tech_compliance_score(account)

            // Total score (0-100)
            account.total_icp_score = (
                account.firmographic_score +
                account.solution_fit_score +
                account.intent_signals_score +
                account.tech_compliance_score
            )

            account.icp_archetype = assign_icp_archetype(account)

            // Assign priority tiers
            IF account.total_icp_score >= 90:
                account.priority_tier = "Critical"
            ELSE IF account.total_icp_score >= 80:
                account.priority_tier = "High"
            ELSE IF account.total_icp_score >= 60:
                account.priority_tier = "Medium"
            ELSE:
                account.priority_tier = "Low"

        SAVE dataset TO "deliverables/prioritized_accounts.csv"
        SAVE TOP_N(dataset, 100, by="total_icp_score") TO "deliverables/top_100_priority_accounts.csv"
END CLASS
```

### Scoring Framework Summary:

- **Total Score:** 0-100 points across 4 dimensions
- **Firmographic Fit:** 40 points (size, revenue, industry)
- **Solution Alignment:** 25 points (interest, role)
- **Intent Signals:** 20 points (intent score, source, recency)
- **Tech/Compliance:** 15 points (tech stack, certifications)

---

## Script 4: Validation & Quality Assurance

### Purpose

Validate deliverables and ensure data integrity

### Pseudocode:

```
FUNCTION validate_deliverables():
    required_files = [
        "data/cleaned_diligent_dataset.csv",
        "deliverables/prioritized_accounts.csv",
        "deliverables/top_100_priority_accounts.csv"
    ]

    // File existence check
    FOR each file IN required_files:
        IF NOT EXISTS(file):
            RAISE ERROR("Missing required file: " + file)

    // Data validation
    dataset = LOAD("deliverables/prioritized_accounts.csv")

    required_columns = [
        "Total_ICP_Score", "ICP_Archetype", "Priority_Tier",
        "Employee_Count_Clean", "Revenue_Clean", "Region_Clean"
    ]

    FOR each column IN required_columns:
        IF column NOT IN dataset.columns:
            RAISE ERROR("Missing required column: " + column)

    // Data quality checks
    ASSERT dataset.Total_ICP_Score.min() >= 0
    ASSERT dataset.Total_ICP_Score.max() <= 100
    ASSERT COUNT(dataset WHERE Priority_Tier == "Critical") > 0

    // Generate summary metrics
    PRINT "Total accounts:", LENGTH(dataset)
    PRINT "Average ICP Score:", MEAN(dataset.Total_ICP_Score)
    PRINT "Critical accounts:", COUNT(dataset WHERE Total_ICP_Score >= 90)

    PRINT "✓ All validations passed"
END FUNCTION
```

### Key Validations:

- File completeness check
- Required column presence
- Score range validation (0-100)
- Priority tier distribution
- Summary statistics generation

---

## Implementation Notes

### Programming Language: Python 3.9+

### Key Libraries Used:

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib/seaborn**: Data visualization
- **openpyxl**: Excel file handling
- **re**: Regular expressions for text processing

### Execution Order:

1. `01_data_exploration.py` - Understand data structure and quality
2. `02_data_cleaning.py` - Normalize and standardize data
3. `03_icp_scoring.py` - Calculate scores and assign priorities
4. `04_validation.py` - Validate results and generate summary

### Output Files:

- **Cleaned Dataset**: `data/cleaned_diligent_dataset.csv`
- **Full Scored Dataset**: `deliverables/prioritized_accounts.csv`
- **Sales Priority List**: `deliverables/top_100_priority_accounts.csv`
- **Visualization Dashboard**: `deliverables/icp_scoring_dashboard.png`

---

_This pseudocode represents the core logic of the GTM data processing pipeline, designed for scalability and maintainability in a production environment._
