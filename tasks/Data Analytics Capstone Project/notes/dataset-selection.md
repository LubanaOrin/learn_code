# Dataset Selection Notes

## Goal

Choose a capstone dataset that can become a strong portfolio project and support at least three course analysis techniques.

## Privacy Boundary

Do **not** use the user's Suhkonen/university capstone files for this college capstone.

Reason:

- The Suhkonen project is private university work.
- This capstone should use a public dataset from Kaggle, GitHub, BigQuery, or another acceptable public source.
- Keeping the projects separate protects privacy and avoids reusing private academic work.

## Recommended Direction

Updated recommended project type: **public quantitative survey-based research project**.

Why this is strong:

- It directly supports a PhD application story by showing experience with quantitative research.
- It can still satisfy the college requirements: data source, context, target audience, dashboard, presentation, written report, hypotheses, techniques, limitations, and recommendations.
- It allows a more academic structure: research question, hypotheses, variable operationalization, statistical testing, model interpretation, and reproducible analysis.
- It can still produce a useful dashboard, but the dashboard will summarize evidence rather than only business KPIs.

Important framing:

The capstone does not need to mention the thesis directly. It should show transferable quantitative research skills that are useful for doctoral study.

## Candidate Dataset 1 - OSMI Mental Health In Tech Survey, Kaggle

Working title:

**Workplace Mental Health Disclosure And Support In The Technology Sector: A Quantitative Survey Analysis**

Dataset source:

https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

Possible research problem:

Mental health support in technology workplaces may affect whether employees seek treatment, disclose mental health concerns, or believe workplace consequences are likely. This project would analyze how workplace support, perceived stigma, family history, work interference, and demographic/work factors relate to treatment-seeking behavior.

Possible target audience:

- Academic reviewers
- PhD admissions or research supervisors
- HR analytics teams
- Workplace wellbeing researchers
- Technology company people operations teams

Possible research questions:

1. Which factors are associated with whether tech workers seek mental health treatment?
2. Is perceived workplace support related to comfort discussing mental health at work?
3. Do respondents who report work interference differ from those who do not?
4. Are company benefits, anonymity, and leave policies associated with treatment-seeking behavior?

Possible hypotheses:

1. Respondents who know their employer provides mental health benefits are more likely to seek treatment.
2. Respondents who believe discussing mental health may have negative consequences are less comfortable discussing mental health with supervisors or coworkers.
3. Respondents reporting frequent work interference are more likely to have sought treatment.
4. Workplace support indicators differ by company size, remote work status, and tech-company status.

Possible techniques:

- Segmentation: compare treatment-seeking and comfort levels by workplace policy, company size, remote work, and demographic groups.
- Hypothesis testing: test associations between categorical survey variables, such as benefits and treatment.
- Logistic regression/classification: model likelihood of treatment-seeking or workplace discussion comfort.
- Dashboard analysis: show treatment, support, stigma, and workplace-policy patterns.

Strengths:

- Public Kaggle dataset.
- Survey-based, which fits the quantitative research profile goal.
- Clear academic-style hypotheses.
- Strong ethical/organizational research angle.
- Can satisfy college requirements without using private university capstone data.

Risks:

- Kaggle download usually requires a Kaggle account login.
- We need to confirm the exact row count, column count, and license after download.
- This is observational survey data, so the report can discuss associations, not causal effects.

## Candidate Dataset 2 - Stack Overflow Annual Developer Survey

Working title:

**AI Tool Adoption, Trust, And Developer Outcomes: A Quantitative Survey Analysis**

Possible research problem:

AI tools are increasingly used by software developers, but adoption does not necessarily mean trust, satisfaction, or perceived productivity. This project would analyze whether developer experience, work context, and AI attitudes are associated with AI tool usage and trust.

Possible target audience:

- Academic reviewers
- PhD admissions or research supervisors
- Technology workforce researchers
- Developer experience or AI adoption teams

Possible research questions:

1. Which developer characteristics are associated with AI tool adoption?
2. Do professional experience, education, or work arrangement relate to trust in AI-generated outputs?
3. Are AI users more likely to report productivity benefits than non-users?
4. Which groups show the largest gap between AI adoption and AI trust?

Possible hypotheses:

1. Developers with fewer years of professional experience are more likely to use AI tools than highly experienced developers.
2. Developers who report positive AI sentiment are more likely to report productivity benefits.
3. Trust in AI outputs differs by professional experience level and work environment.
4. AI adoption is high even among respondents who report concerns about accuracy or ethics.

Possible techniques:

- Segmentation: compare groups by experience, education, geography, work environment, and AI usage.
- Hypothesis testing: test whether differences between groups are statistically meaningful.
- Logistic regression or classification: model whether a respondent uses AI tools or trusts AI outputs.
- Correlation/association analysis: check relationships between experience, AI sentiment, trust, and productivity.
- Dashboard analysis: summarize adoption, trust, productivity, and group differences.

Strengths:

- Strong fit for a quantitative study profile.
- Has survey methodology and large sample size.
- Current and relevant to technology, AI, work, and education.
- Official public data is available as CSV from Stack Overflow.
- The report can use an academic structure while still meeting the college capstone requirements.

Risks:

- It is observational survey data, so the analysis can show associations, not causation.
- Some survey variables are categorical and multi-select, so cleaning must be careful.
- We need to choose a focused question so the project does not become too broad.

Status:

Blocked for now because the user did not see a download option on the survey page and direct URL attempts returned 404 pages.

## Candidate Dataset 3 - European Social Survey

Working title:

**Digital Social Contact, Trust, And Wellbeing In Europe**

Possible research problem:

European societies differ in social trust, digital contact patterns, and wellbeing. This project could analyze whether digital social contact and demographic factors are associated with wellbeing or trust.

Possible techniques:

- Segmentation
- Hypothesis testing
- Regression modeling
- Cross-country comparison

Strengths:

- Very academic and respected social science data source.
- Strong fit for PhD-style quantitative work.
- Good for research methodology language.

Risks:

- Data access and variable documentation can take longer.
- The dashboard story may be less direct than Stack Overflow.

## Candidate Dataset 4 - OECD PISA 2022

Working title:

**Student Performance, Learning Resources, And Wellbeing: A Quantitative Analysis Of PISA 2022**

Possible research problem:

Student achievement may be associated with learning resources, school context, wellbeing, and socioeconomic background.

Possible techniques:

- Segmentation
- Hypothesis testing
- Regression modeling
- Cross-country comparison

Strengths:

- Very strong education research dataset.
- Good for PhD applications if education or social research is relevant.

Risks:

- Large and complex dataset.
- Requires careful handling of sampling weights and plausible values, which may be too much for the capstone timeline.

## Earlier Business Option - TheLook E-commerce

This remains a good option for business analytics, but it is no longer the strongest recommendation if the main profile goal is to show quantitative research experience for future PhD applications.

## Candidate Dataset 1 - TheLook E-commerce, BigQuery Public Dataset

Working title:

**Improving E-commerce Growth Through Funnel, Retention, and Customer Value Analysis**

Possible business problem:

An online retailer wants to understand where customers drop off, which customer groups create the most value, and what actions could improve repeat purchases and revenue.

Possible target audience:

- Head of E-commerce
- Product manager
- Marketing manager
- Growth analyst team

Possible techniques:

- Funnel analysis: where users move from browsing to purchase, and where drop-offs happen.
- Cohort analysis: whether customers who first purchased in different months behave differently over time.
- RFM analysis: segment customers by recency, frequency, and monetary value.
- Customer segmentation: compare value and behavior by country, age group, traffic source, or product category.
- Time-series analysis: monthly revenue, orders, repeat purchases, and seasonality.

Strengths:

- Very good fit for a portfolio because it sounds like real business work.
- BigQuery is a good place to practice SQL joins and aggregation.
- Supports more than the required three techniques.
- Dashboard story can be clear: acquisition -> conversion -> retention -> customer value -> recommendations.

Risks:

- We need to confirm it was not used in your course Hands-On or Graded Tasks.
- We need BigQuery access or exported tables before analysis.

## Candidate Dataset 2 - Olist Brazilian E-commerce Dataset

Working title:

**Customer Experience And Revenue Drivers In Brazilian E-commerce**

Possible business problem:

An e-commerce marketplace wants to understand how delivery performance, reviews, payments, and customer geography relate to revenue and customer satisfaction.

Possible techniques:

- RFM analysis
- Customer segmentation
- Delivery delay analysis
- Review score analysis
- Time-series analysis

Strengths:

- Real-world marketplace dataset.
- Good for customer satisfaction and logistics questions.
- Can be analyzed locally after downloading CSV files.

Risks:

- Kaggle download may need account access.
- It may be a common student portfolio dataset, so it may feel less unique unless we choose a strong angle.

## Candidate Dataset 3 - Citi Bike Trip Data

Working title:

**Improving Bike Share Operations Through Usage Pattern And Station Demand Analysis**

Possible business problem:

A bike-share operator wants to understand demand patterns, station usage, and member/casual behavior to improve bike availability and service planning.

Possible techniques:

- Time-series analysis
- User segmentation
- Geospatial/station analysis
- Peak/off-peak analysis

Strengths:

- Public and well-documented source.
- Strong operations analytics angle.
- Good dashboard potential with maps and time patterns.

Risks:

- Harder to use classic course techniques like RFM, cohort analysis, or funnel analysis because current trip files do not include a stable customer ID.
- It may become more operational than customer/business growth focused.

## Current Recommendation

Start with **Candidate Dataset 1: OSMI Mental Health In Tech Survey from Kaggle**.

Reason:

It gives the best balance of quantitative research framing, public Kaggle sourcing, dashboard potential, and college requirement coverage without using private Suhkonen data.

## Proposed Capstone Story

Question:

**What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?**

Hypotheses:

1. Respondents who know their employer provides mental health benefits are more likely to seek treatment.
2. Respondents who expect negative workplace consequences are less comfortable discussing mental health at work.
3. Respondents whose mental health interferes with work are more likely to have sought treatment.
4. Workplace support indicators differ by company size, remote work status, and whether the employer is primarily a tech company.

Core deliverables:

- Kaggle source notes, cleaned survey dataset, and reproducible analysis notebook.
- SQL or Pandas queries used for cleaning, aggregation, and statistical tables.
- Dashboard showing mental health treatment, workplace support, stigma/disclosure comfort, and subgroup differences.
- Written report with executive summary, data source, methodology, hypothesis tests/models, limitations, and recommendations.
- Presentation with speaker notes for a 10-15 minute research-style walkthrough.

## Source Notes

- OSMI Mental Health in Tech Survey on Kaggle: https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
- Stack Overflow states that its 2025 Developer Survey received more than 49,000 responses from 177 countries and provides public CSV data: https://survey.stackoverflow.co/
- Stack Overflow states that its 2024 Developer Survey had 65,437 respondents from 185 countries and includes AI, work, developer profile, technology, and methodology sections: https://survey.stackoverflow.co/2024/
- European Social Survey data portal: https://ess.sikt.no/en/
- OECD PISA 2022 database: https://www.oecd.org/en/data/datasets/pisa-2022-database.html
- Citi Bike publishes downloadable trip history files and documents fields such as ride ID, rideable type, start/end timestamps, station names, coordinates, and member/casual rider type: https://citibikenyc.com/system-data
- Google Cloud BigQuery free tier includes 1 TiB of query processing and 10 GiB of storage per month, but we still need to manage costs carefully if billing is enabled: https://cloud.google.com/free/docs/free-cloud-features#bigquery
- BigQuery Sandbox tables, views, and partitions expire after 60 days, so SQL and exported results should be saved outside BigQuery: https://cloud.google.com/bigquery/docs/sandbox
