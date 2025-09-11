# GTM Engineer Analysis - Executive Summary

## Diligent Prospect Dataset Analysis & ICP Prioritization

**Author:** GTM Engineer Candidate  
**Date:** September 9, 2025  
**Analysis Duration:** 2.5 hours

---

## Executive Summary

Analyzed 1,000 prospect accounts to build a data-driven ICP framework and prioritization system for Diligent's GTM team. The analysis cleaned messy data, defined 3 core ICP archetypes, and delivered a scored dataset with 20 critical accounts ready for immediate sales attention.

### Key Findings

- **Data Quality:** 19.5% missing employee data, 19.2% missing revenue data - significant enrichment opportunity
- **ICP Distribution:** 58.8% of accounts fit our core Enterprise Risk (28.8%) and Mid-Market Compliance (30.0%) archetypes
- **High-Priority Targets:** 20 critical accounts (90+ scores) with strong firmographic fit and solution alignment
- **Revenue Opportunity:** Critical accounts represent estimated $2.5B+ in combined revenue

---

## ICP Archetypes Defined

### 1. Enterprise Risk Management (28.8% of dataset)

**Profile:** Large enterprises with complex risk management needs

- **Size:** 500+ employees, $100M+ revenue
- **Industries:** Financial Services, Healthcare, Energy, Manufacturing
- **Key Personas:** Chief Risk Officer, Risk Manager, Board Secretary
- **Solution Focus:** Risk management platforms
- **Tech Stack:** Salesforce, ServiceNow, Workday
- **Priority Certifications:** SOX, PCI DSS, ISO27001

### 2. Mid-Market Compliance (30.0% of dataset)

**Profile:** Growing companies needing compliance frameworks

- **Size:** 200-1000 employees, $20M-$100M revenue
- **Industries:** Technology, Financial Services, Healthcare, Legal
- **Key Personas:** General Counsel, Legal Counsel, Compliance Officer
- **Solution Focus:** Compliance automation
- **Tech Stack:** HubSpot, Marketo, Pardot, Okta
- **Priority Certifications:** GDPR, HIPAA, ISO27001

### 3. Board Governance (27.2% of dataset)

**Profile:** Organizations focused on board management

- **Size:** 200+ employees, $100M+ revenue
- **Industries:** Financial Services, Non-Profit, Legal, Government
- **Key Personas:** Board Secretary, Director of Security, General Counsel
- **Solution Focus:** Board management software
- **Tech Stack:** Salesforce, Workday, ServiceNow
- **Priority Certifications:** SOX, GDPR

---

## Scoring Methodology

**Total Score: 0-100 points across 4 dimensions:**

1. **Firmographic Fit (40 points)**

   - Employee count: 15 pts (1000+ = max score)
   - Revenue size: 15 pts ($250M+ = max score)
   - Industry vertical: 10 pts (Financial Services = max score)

2. **Solution Alignment (25 points)**

   - Solution interest: 15 pts (Risk = max score)
   - Contact role: 10 pts (C-level risk/compliance = max score)

3. **Intent Signals (20 points)**

   - Intent score: 10 pts (80+ = max score)
   - Lead source: 5 pts (Referral = max score)
   - Recency: 5 pts (<30 days = max score)

4. **Technology/Compliance Readiness (15 points)**
   - Tech stack: 8 pts (Enterprise tools = max score)
   - Certifications: 7 pts (SOX/PCI DSS = max score)

---

## Priority Recommendations

### Immediate Actions (Next 30 Days)

1. **Contact Top 20 Critical Accounts** (90+ scores)

   - Focus on Enterprise Risk prospects with Risk solution interest
   - Prioritize accounts with referral sources and recent engagement
   - Examples: Luthor Enterprises, Shinra Electric, Clampett Oil

2. **Sales Enablement for High-Priority Tier** (80-89 scores, 405 accounts)
   - Create archetype-specific talk tracks
   - Develop compliance-focused content for Mid-Market segment
   - Focus on persona-based messaging

### Medium-Term Strategy (Next 90 Days)

1. **Data Enrichment Initiative**

   - Target 195 accounts missing employee count data
   - Enrich 192 accounts missing revenue information
   - Focus on accounts with high solution alignment scores

2. **Regional Prioritization**
   - EMEA and Americas show highest concentration of critical accounts
   - Allocate sales resources based on regional ICP density

---

## Systems Integration Plan

### Quick Wins (2-4 weeks)

- **CRM Integration:** Import scored dataset into Salesforce with custom ICP score fields
- **Lead Routing:** Implement score-based assignment rules (90+ to senior reps)
- **Dashboard Creation:** Build executive dashboard showing ICP distribution and pipeline health

### Scalable Pipeline (3-6 months)

- **Marketing Automation:** Integrate ICP scores with Marketo/Pardot for personalized campaigns
- **Data Enrichment API:** Connect ZoomInfo/Clearbit for automated firmographic updates
- **Real-time Scoring:** Implement webhook-based scoring updates as data changes

### Long-term Architecture (6-12 months)

- **CDP Implementation:** Customer Data Platform for unified prospect/customer view
- **Machine Learning:** Enhance ICP scoring with behavioral prediction models
- **Attribution Analysis:** Connect ICP scores to conversion rates and deal sizes

### Technology Tradeoffs

**Scripts vs. Pipelines:**

- **Scripts:** Fast to implement, good for initial validation, manual maintenance
- **Pipelines:** Scalable, automated, requires more infrastructure investment
- **Recommendation:** Start with scripts for immediate ROI, build pipelines for scale

---

## Data Enrichment Priorities

### High-Impact Fields to Enrich

1. **Employee Count** (195 missing) - Critical for firmographic scoring
2. **Revenue Data** (192 missing) - Essential for deal sizing
3. **SFDC Account IDs** (36 missing) - Required for CRM integration
4. **Intent Scores** (125 missing) - Key for timing and prioritization

### Recommended Enrichment Sources

- **Firmographic Data:** ZoomInfo, LinkedIn Sales Navigator, Clearbit
- **Intent Data:** Bombora, 6sense, TechTarget
- **Technographic Data:** BuiltWith, Datanyze, HG Insights
- **Financial Data:** D&B Hoovers, PitchBook

---

## Success Metrics

### Leading Indicators

- ICP score distribution shifts (target: 15% in Critical tier)
- Data completeness improvement (target: <5% missing key fields)
- Sales qualification rates by ICP tier

### Lagging Indicators

- Conversion rates by ICP archetype
- Average deal size by priority tier
- Sales cycle length correlation with ICP scores

---

**Next Steps:** Schedule stakeholder review, begin CRM integration, and initiate top 20 account outreach campaign.

_Analysis completed using Python data pipeline with pandas, numpy, and custom scoring algorithms. AI assistance used for data normalization logic and visualization creation._
