# Diligent GTM Engineer Analysis Project

## Overview

This project addresses the Growth Manager / GTM Engineer role assessment for Diligent, focusing on building a data-driven ICP framework and account prioritization system from a messy 1,000-prospect dataset.

## Project Structure

```
Diligent_project/
├── data/
│   ├── Diligent_GTM_Engineer_Exercise_with_Instructions.xlsx  # Original dataset
│   └── cleaned_diligent_dataset.csv                         # Cleaned data
├── scripts/
│   ├── 01_data_exploration.py        # Initial data analysis
│   ├── 02_data_cleaning.py          # Data normalization pipeline
│   └── 03_icp_scoring.py            # ICP scoring and prioritization
├── analysis/
│   ├── data_quality_assessment.csv  # Data quality report
│   └── sample_raw_data.csv         # Sample of raw data
├── deliverables/
│   ├── Executive_Summary.md         # Main analysis summary
│   ├── prioritized_accounts.csv    # Full scored dataset
│   ├── top_100_priority_accounts.csv # Top prospects for sales
│   └── icp_scoring_dashboard.png   # Visualization dashboard
└── README.md
```

## Key Deliverables

### 1. Cleaned Dataset

- **File:** `deliverables/prioritized_accounts.csv`
- **Records:** 1,000 accounts with standardized formats
- **New Fields:** ICP scores, priority tiers, archetype assignments

### 2. ICP Scoring Framework

- **Enterprise Risk Management:** Large companies focused on risk
- **Mid-Market Compliance:** Growing companies needing compliance
- **Board Governance:** Organizations managing board processes
- **Scoring:** 0-100 points across firmographic, solution, intent, and tech dimensions

### 3. Priority Account Lists

- **Critical Tier (90+ points):** 20 accounts for immediate outreach
- **High Tier (80-89 points):** 405 accounts for sales focus
- **Top 100 List:** Ready-to-use prioritized prospect list

### 4. Systems Integration Plan

- Quick wins: CRM integration, lead routing, dashboards
- Scalable pipeline: Marketing automation, enrichment APIs
- Long-term: CDP implementation, ML scoring, attribution analysis

## How to Run

### Prerequisites

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Execution Steps

1. **Data Exploration:**

   ```bash
   cd scripts
   python 01_data_exploration.py
   ```

2. **Data Cleaning:**

   ```bash
   python 02_data_cleaning.py
   ```

3. **ICP Scoring:**
   ```bash
   python 03_icp_scoring.py
   ```

## Data Cleaning Approach

### Employee Count Normalization

- Standardized ranges: "500-1,000", "1000+", etc.
- Converted text: "five hundred" → "500-1,000"
- Unified format: "500 to 1000" → "500-1,000"

### Revenue Standardization

- Universal format: "$XXXm" in USD
- Currency conversion: "€20M" → "$20M"
- Number formatting: "5000000" → "$5M"

### Region Mapping

- Code expansion: "AMS" → "Americas"
- Standardization: "DACH", "UKI", "EMEA", etc.
- Unknown handling: Consistent "Unknown" label

### Date Normalization

- Standard format: YYYY-MM-DD
- Multiple input formats supported
- Pattern matching for various date styles

## AI Usage Declaration

AI assistance was used for:

- **Data normalization logic:** Regex patterns for cleaning messy data formats
- **Visualization creation:** matplotlib/seaborn chart generation code
- **Code optimization:** Pandas operations and function structuring
- **Documentation:** README structure and technical explanations

**Human IP:** All strategic decisions, ICP framework design, scoring methodology, business recommendations, and analysis insights are original work.

## Key Insights

### Data Quality Issues Identified

- 19.5% missing employee count data
- 19.2% missing revenue information
- Inconsistent date formats across 5+ patterns
- Mixed currency notations and scales
- Region code inconsistencies

### ICP Distribution Results

- Enterprise Risk Management: 28.8% (288 accounts)
- Mid-Market Compliance: 30.0% (300 accounts)
- Board Governance: 27.2% (272 accounts)
- Other: 14.0% (140 accounts)

### Priority Scoring Results

- Critical (90+): 20 accounts (2.0%)
- High (80-89): 405 accounts (40.5%)
- Medium (60-79): 506 accounts (50.6%)
- Low (<60): 69 accounts (6.9%)

## Business Impact

### Immediate Value

- 20 critical accounts identified for immediate sales focus
- Data quality improved from 80% to 95%+ completeness
- Clear prioritization framework for 1,000 prospects

### Strategic Value

- Repeatable ICP scoring methodology
- Foundation for marketing automation integration
- Data-driven sales territory planning capability

## Next Steps

1. **Immediate (Week 1):**

   - Import scored data into Salesforce
   - Begin outreach to top 20 critical accounts
   - Train sales team on ICP archetypes

2. **Short-term (Month 1):**

   - Implement lead routing based on scores
   - Create archetype-specific marketing content
   - Begin data enrichment for missing fields

3. **Long-term (Quarter 1):**
   - Build automated scoring pipeline
   - Connect marketing automation platforms
   - Establish success metrics and tracking

## Contact

For questions about this analysis or implementation support, please contact the GTM Engineer candidate.

---

_Project completed in 2.5 hours as part of Diligent Growth Manager / GTM Engineer assessment._
