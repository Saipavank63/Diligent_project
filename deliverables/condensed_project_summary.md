# Diligent GTM Engineer Analysis Project - Condensed Summary

## Overview

This project builds a data-driven ICP framework and account prioritization system from a messy 1,000-prospect dataset for Diligent's GTM team. Completed in 2.5 hours, it includes data cleaning, ICP archetype definition, scoring, and prioritized account lists.

## Project Structure

- **data/**: Original Excel dataset and cleaned CSV
- **scripts/**: Python scripts for exploration, cleaning, and scoring
- **analysis/**: Data quality reports and samples
- **deliverables/**: Summaries, prioritized CSVs, dashboard PNG

## Key Deliverables

- **Cleaned Dataset**: 1,000 accounts with standardized formats, ICP scores, and priority tiers
- **ICP Scoring Framework**: 3 archetypes (Enterprise Risk, Mid-Market Compliance, Board Governance) scored 0-100 across firmographic, solution, intent, and tech dimensions
- **Priority Lists**: 20 critical (90+), 405 high (80-89), top 100 accounts
- **Systems Integration Plan**: Quick wins (CRM integration), scalable pipeline (automation), long-term (ML scoring)

## Data Cleaning Approach

- **Employee Count**: Standardized ranges (e.g., "500-1,000"), converted text to numbers
- **Revenue**: Universal USD format, currency conversion
- **Region**: Consistent labels (e.g., "AMS" → "Americas")
- **Date**: YYYY-MM-DD format with pattern matching
- **Quality Improvement**: From 80% to 95%+ completeness

## ICP Archetypes

1. **Enterprise Risk Management** (28.8%): Large enterprises (500+ employees, $100M+) in Financial Services/Healthcare; focus on risk platforms
2. **Mid-Market Compliance** (30.0%): Growing companies (200-1000 employees, $20M-$100M) needing compliance automation
3. **Board Governance** (27.2%): Organizations managing board processes

## Key Results

- **Data Quality Issues**: 19.5% missing employee data, 19.2% missing revenue
- **Priority Distribution**: Critical (2.0%), High (40.5%), Medium (50.6%), Low (6.9%)
- **Business Impact**: 20 critical accounts for immediate outreach; repeatable scoring methodology

## Next Steps

1. **Immediate (Week 1)**: Import to Salesforce, outreach to top 20, train sales team
2. **Short-term (Month 1)**: Lead routing, archetype-specific content, data enrichment
3. **Long-term (Quarter 1)**: Automated pipeline, marketing automation, success metrics

## AI Usage Declaration

AI assisted with regex patterns, visualization code, and documentation. All strategic decisions, ICP design, scoring methodology, and insights are original human work.

_Project completed September 9, 2025_</content>
<parameter name="filePath">/Users/saipavankatineedi/Desktop/Diligent_project/deliverables/condensed_project_summary.md
