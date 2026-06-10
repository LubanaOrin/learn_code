# Workplace Mental Health Disclosure And Support In The Technology Sector

## Executive Summary

This report analyzes the OSMI Mental Health in Tech Survey, a public Kaggle dataset with 1,259 survey responses about mental health treatment, workplace support, disclosure comfort, and perceived workplace consequences in technology-related workplaces.

The analysis found that 637 respondents, or 50.6%, reported seeking mental health treatment. However, workplace disclosure comfort was lower: 516 respondents, or 41.0%, were comfortable discussing mental health with a supervisor, and only 225 respondents, or 17.9%, were comfortable discussing it with coworkers.

The strongest treatment-seeking differences appeared across work interference, family history, employer care options, and employer mental health benefits. Hypothesis testing showed statistically significant associations between treatment-seeking and benefits, care options, family history, and work interference. A logistic regression model predicting treatment-seeking reached ROC AUC 0.891 on the test set.

The main conclusion is that treatment-seeking is common in this sample, but workplace openness is limited. Employers should improve benefit clarity, care-option visibility, confidentiality communication, manager training, and stigma reduction.

## Introduction

Mental health has become an important workplace topic, especially in technology workplaces where stress, remote work, fast-paced delivery, and knowledge work can affect employee wellbeing. Even when employees seek mental health treatment privately, they may not feel comfortable discussing mental health needs at work.

This project uses quantitative survey analysis to study workplace mental health support in the technology sector. The goal is to identify which workplace and personal factors are associated with treatment-seeking and mental health disclosure comfort.

## Data Source And Context

The dataset used in this project is the OSMI Mental Health in Tech Survey from Kaggle:

https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

The raw dataset contains 1,259 rows and 27 columns. One row represents one survey response. The dataset includes variables about:

- mental health treatment-seeking
- family history
- work interference
- company size
- remote work
- tech-company status
- mental health benefits
- care options
- wellness programs
- help-seeking resources
- anonymity
- mental health leave difficulty
- perceived workplace consequences
- comfort discussing mental health with coworkers and supervisors

The dataset is observational and self-reported. This means the analysis can identify associations, but it cannot prove cause and effect.

## Target Audience

The primary audience for this analysis is academic or research-oriented reviewers who want to see evidence of quantitative research ability. A secondary audience is HR analytics teams, people operations teams, and workplace wellbeing researchers in technology organizations.

## Research Question

What workplace and personal factors are associated with mental health treatment-seeking and disclosure comfort among technology workers?

## Hypotheses

H1: Respondents who know their employer provides mental health benefits are more likely to seek treatment.

H2: Respondents who expect negative workplace consequences are less comfortable discussing mental health with supervisors or coworkers.

H3: Respondents whose mental health interferes with work are more likely to have sought treatment.

H4: Workplace support indicators differ by company size, remote work status, and whether the employer is primarily a tech company.

## Methodology

The analysis used three main techniques.

First, segmentation was used to compare treatment-seeking rates across groups such as mental health benefits, care options, family history, work interference, company size, remote work, and tech-company status.

Second, hypothesis testing was used to check whether selected group differences were statistically meaningful. Chi-square tests were used for categorical variables, such as benefits and treatment-seeking. Kruskal-Wallis tests were used for ordered scores across company-size groups.

Third, logistic regression was used to model treatment-seeking as a binary outcome. The model predicted whether a respondent had sought mental health treatment using workplace support, work context, family history, age, and gender variables.

## Data Preparation

The raw dataset required cleaning before analysis. Column names were converted to snake_case. Age values outside the 18-75 range were treated as missing because the raw data included impossible values such as negative ages and extremely large numbers. In total, 8 age values were invalid or outside the chosen analysis range.

Gender required cleaning because the raw dataset contained 49 unique gender values. These were grouped into 4 broader categories for analysis: Male, Female, Non-binary / gender diverse, and Other / unclear.

The cleaned dataset contains 1,259 rows and 56 columns. New variables were created for analysis, including:

- treatment_yes
- benefits_yes
- care_options_yes
- family_history_yes
- remote_work_yes
- tech_company_yes
- work_interfere_score
- leave_difficulty_score
- discussion_comfort_score

## Analysis And Results

### Overall Treatment And Disclosure Patterns

Out of 1,259 respondents, 637 respondents, or 50.6%, reported seeking mental health treatment.

Workplace disclosure comfort was lower. 516 respondents, or 41.0%, were comfortable discussing mental health with a supervisor. Only 225 respondents, or 17.9%, were comfortable discussing mental health with coworkers.

This suggests a gap between private treatment-seeking and workplace openness.

### Workplace Benefits And Treatment-Seeking

Respondents who knew their employer provided mental health benefits had a treatment-seeking rate of 63.9%. Respondents whose employer did not provide benefits had a treatment-seeking rate of 48.4%. Respondents who did not know whether benefits existed had a treatment-seeking rate of 37.0%.

The chi-square test showed a statistically significant association between benefits and treatment-seeking:

- chi-square = 64.8386
- p-value < 0.001

This supports H1.

### Care Options And Treatment-Seeking

Respondents who knew their employer provided mental health care options had a treatment-seeking rate of 69.1%. Respondents with no care options had a treatment-seeking rate of 41.3%. Respondents who were not sure had a treatment-seeking rate of 39.2%.

The chi-square test showed a statistically significant association between care options and treatment-seeking:

- chi-square = 94.7587
- p-value < 0.001

### Family History And Treatment-Seeking

Respondents with a family history of mental illness had a treatment-seeking rate of 74.2%. Respondents without family history had a treatment-seeking rate of 35.5%.

The chi-square test showed a statistically significant association between family history and treatment-seeking:

- chi-square = 178.2668
- p-value < 0.001

### Work Interference And Treatment-Seeking

Treatment-seeking differed strongly by reported work interference:

- Often: 85.4%
- Sometimes: 77.0%
- Rarely: 70.5%
- Never: 14.1%
- Missing: 1.5%

The chi-square test showed a statistically significant association between work interference and treatment-seeking:

- chi-square = 594.9243
- p-value < 0.001

This supports H3.

### Perceived Consequences And Disclosure Comfort

Expected negative workplace consequences were strongly associated with discussion comfort.

For supervisor discussion comfort:

- chi-square = 461.6603
- p-value < 0.001

For coworker discussion comfort:

- chi-square = 285.5339
- p-value < 0.001

This supports H2.

### Company Size

Discussion comfort differed across company-size groups:

- Kruskal-Wallis statistic = 23.7876
- p-value = 0.000238

Leave difficulty did not show a statistically significant difference across company-size groups at the 0.05 level:

- Kruskal-Wallis statistic = 10.3592
- p-value = 0.065674

This partially supports H4.

## Logistic Regression Model

A logistic regression model was built to predict treatment-seeking. The model used workplace support, work context, family history, age, and gender variables.

Model performance:

- train rows: 944
- test rows: 315
- accuracy: 0.819
- ROC AUC: 0.891
- precision for treatment-seeking class: 0.797
- recall for treatment-seeking class: 0.862
- F1 score for treatment-seeking class: 0.828

The strongest positive model signals included:

- work interference often
- work interference sometimes
- work interference rarely
- family history of mental illness
- comfort discussing mental health with coworkers
- knowing employer provides care options
- knowing employer provides mental health benefits

The model confirms that work interference, personal context, and workplace support variables are strongly associated with treatment-seeking. However, the model should not be interpreted causally.

## Dashboard Summary

The dashboard presents the same story visually. It includes:

- treatment-seeking overview
- treatment rate by employer benefits
- treatment rate by work interference
- treatment rate by company size
- supervisor discussion comfort by expected consequences
- hypothesis-test table
- logistic regression model summary

The dashboard file is saved as:

`outputs/dashboard/osmi_mental_health_dashboard.html`

## Recommendations

Technology employers should make mental health benefits and care options easier to understand. Respondents who knew benefits and care options existed had higher treatment-seeking rates than respondents who did not know or did not have access.

Employers should strengthen anonymity and confidentiality communication. If employees fear negative consequences, they may avoid discussing mental health needs even when they seek treatment privately.

Managers should receive training on safe mental health conversations. Only 41.0% of respondents were comfortable discussing mental health with a supervisor.

Organizations should reduce stigma in team culture. Only 17.9% of respondents were comfortable discussing mental health with coworkers.

Employers should monitor work interference as a warning signal. Respondents reporting work interference had much higher treatment-seeking rates, especially those reporting that mental health often interfered with work.

## Limitations

The dataset is observational, so the analysis cannot prove cause and effect.

The survey respondents are not a perfectly random sample of all technology workers.

The data is self-reported, so responses may include recall bias or social desirability bias.

Some variables have missing values, especially work_interfere.

Gender was grouped from many raw self-described values, which simplifies identity categories for analysis.

The dataset is from one public Kaggle source, so the findings should be generalized carefully.

## Conclusion

This analysis shows that mental health treatment-seeking is common in the OSMI technology-sector survey sample, but workplace disclosure comfort is much lower. 50.6% of respondents reported seeking treatment, while only 41.0% were comfortable discussing mental health with supervisors and only 17.9% were comfortable discussing it with coworkers.

The strongest evidence points to the importance of workplace support, benefit awareness, care options, perceived consequences, and work interference. The findings suggest that organizations should not only offer mental health resources, but also make them visible, confidential, and culturally safe to use.

## References

OSMI Mental Health in Tech Survey. Kaggle. https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

University of Leeds. Report writing. https://library.leeds.ac.uk/info/14011/writing/114/report_writing

Grammarly. How to write a report. https://www.grammarly.com/blog/academic-writing/how-to-write-a-report/
