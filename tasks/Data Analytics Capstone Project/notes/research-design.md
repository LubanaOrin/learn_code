# Research Design

## Privacy Boundary

Do **not** use the user's Suhkonen/university capstone files for this project.

This capstone should use a public dataset from Kaggle, GitHub, BigQuery, or another allowed public source.

## Working Title

**Workplace Mental Health Disclosure And Support In The Technology Sector: A Quantitative Survey Analysis**

## Profile Purpose

This capstone should show quantitative research readiness for future PhD applications.

The project will demonstrate that the analyst can:

- Define a research problem.
- Form hypotheses.
- Use a public survey dataset.
- Convert survey answers into measurable variables.
- Clean and prepare data reproducibly.
- Compare groups.
- Run statistical tests or models.
- Interpret results carefully.
- Explain limitations.
- Present findings through a dashboard, written report, and presentation.

## Dataset

Recommended dataset:

**OSMI Mental Health In Tech Survey**

Source:

https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

Why this dataset:

- It is a public Kaggle survey dataset.
- It allows the capstone to demonstrate quantitative research methods without using private university capstone data.
- It includes workplace, demographic, support, stigma, and treatment-seeking variables.
- It is suitable for segmentation, hypothesis testing, and logistic regression/classification.

Fallback dataset:

**Stack Overflow Developer Survey 2024**

Source:

https://survey.stackoverflow.co/2024/

Why keep this fallback:

- It is still conceptually strong, but currently blocked because the public result pages did not expose a download option for the user.

## Research Problem

Mental health support in technology workplaces may affect whether employees seek treatment, disclose concerns, or believe workplace consequences are likely.

This project studies the relationship between workplace support, perceived stigma, work interference, and mental health treatment-seeking behavior.

## Main Research Question

**What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?**

## Sub-questions

1. How common is mental health treatment-seeking among survey respondents?
2. How do workplace benefits, care options, anonymity, and leave policies relate to treatment-seeking?
3. Is perceived workplace stigma related to comfort discussing mental health with supervisors or coworkers?
4. Do respondents who report mental health interference with work differ from those who do not?
5. Which workplace groups show lower support or higher disclosure concern?

## Hypotheses

H1: Respondents who know their employer provides mental health benefits are more likely to seek treatment.

H2: Respondents who expect negative workplace consequences are less comfortable discussing mental health with supervisors or coworkers.

H3: Respondents whose mental health interferes with work are more likely to have sought treatment.

H4: Workplace support indicators differ by company size, remote work status, and whether the employer is primarily a tech company.

## Target Audience

Primary audience:

- PhD admissions reviewers or research supervisors who want evidence of quantitative research ability.

Secondary audience:

- Workplace wellbeing researchers.
- HR analytics or people operations teams.
- Technology employers evaluating workplace mental health support.

## Required College Techniques

Technique 1: **Segmentation**

Purpose:

Compare treatment-seeking, disclosure comfort, and support indicators across groups such as company size, remote work, benefits knowledge, care options, anonymity, and tech-company status.

Why it matters:

Segmentation shows whether the overall result hides different patterns across respondent groups.

Technique 2: **Hypothesis Testing**

Purpose:

Test whether observed group differences are likely to be meaningful rather than random variation.

Possible tests:

- Chi-square test for categorical variables, such as benefits knowledge versus treatment-seeking.
- Mann-Whitney U or Kruskal-Wallis test for ordinal responses, depending on final variable structure.

Why it matters:

Hypothesis testing is important for quantitative research because it adds evidence beyond descriptive charts.

Technique 3: **Regression Or Classification Modeling**

Purpose:

Model whether selected predictors are associated with treatment-seeking or disclosure comfort.

Possible models:

- Logistic regression for treatment-seeking, such as sought treatment versus did not seek treatment.
- Logistic regression for disclosure comfort, such as comfortable discussing mental health versus not comfortable.

Why it matters:

Regression helps estimate relationships while considering several variables at the same time.

Optional technique 4: **Correlation Or Association Analysis**

Purpose:

Explore relationships among ordered survey responses, such as work interference, leave difficulty, and discussion comfort.

## Variable Plan

Outcome variables:

- Treatment-seeking behavior.
- Comfort discussing mental health with supervisor or coworkers.
- Work interference due to mental health.

Predictor variables:

- Employer mental health benefits.
- Care options.
- Wellness program.
- Anonymity protection.
- Mental health leave difficulty.
- Perceived negative consequences.
- Company size.
- Remote work.
- Tech-company status.
- Family history.

Control variables, if available and clean enough:

- Age.
- Gender.
- Country.
- Employment status.

## Dashboard Story

The dashboard should summarize the evidence in four sections:

1. Mental health treatment overview.
2. Workplace support and policy awareness.
3. Stigma, disclosure comfort, and perceived consequences.
4. Group differences and model findings.

Possible dashboard pages:

- Overview
- Workplace support
- Disclosure and stigma
- Model findings

## Written Report Story

Recommended structure:

1. Executive summary
2. Introduction
3. Data source and survey context
4. Target audience
5. Research questions and hypotheses
6. Methodology
7. Analysis and results
8. Dashboard summary
9. Limitations
10. Recommendations
11. Conclusion
12. References

## Presentation Story

Recommended 10-15 minute flow:

1. Why workplace mental health support matters
2. Dataset and research question
3. Hypotheses
4. Methodology and techniques
5. Key descriptive findings
6. Segmentation findings
7. Hypothesis test/model findings
8. Dashboard walkthrough
9. Limitations
10. Recommendations and conclusion

## Important Limitations To Include Later

- The data is observational, so the project can show associations, not prove causation.
- The survey respondents are Kaggle/OSMI dataset participants, not a perfectly random sample of all technology workers.
- Some variables are self-reported, which can introduce recall or perception bias.
- Multi-select survey questions may require careful transformation.
- The public dataset may remove or anonymize some fields.

## Source Notes

- OSMI Mental Health in Tech Survey on Kaggle: https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
- Stack Overflow 2025 survey page: https://survey.stackoverflow.co/2025/
- Stack Overflow 2024 survey page: https://survey.stackoverflow.co/2024/
- Stack Overflow states that the 2024 survey data is licensed under the Open Database License on the survey result page.
