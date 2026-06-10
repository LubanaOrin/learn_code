# OSMI Mental Health In Tech Survey - Dataset Inventory

## Source

Dataset:

**OSMI Mental Health in Tech Survey**

Kaggle page:

https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

Local files:

- `data/osmi-mental-health-in-tech-survey.zip`
- `data/osmi-mental-health-in-tech-survey/survey.csv`

## Dataset Size

- Rows: 1,259
- Columns: 27

One row represents one survey response.

## Main Topic

The dataset contains survey responses about mental health in technology workplaces, including:

- treatment-seeking behavior
- family history
- work interference
- company size
- remote work
- whether the employer is a tech company
- mental health benefits
- care options
- wellness programs
- help-seeking resources
- anonymity
- leave difficulty
- perceived workplace consequences
- comfort discussing mental health with coworkers and supervisors

## Important Columns

Outcome variables:

- `treatment`: whether the respondent has sought treatment for a mental health condition.
- `coworkers`: willingness to discuss mental health with coworkers.
- `supervisor`: willingness to discuss mental health with supervisors.
- `work_interfere`: whether mental health interferes with work.

Predictor variables:

- `family_history`
- `benefits`
- `care_options`
- `wellness_program`
- `seek_help`
- `anonymity`
- `leave`
- `mental_health_consequence`
- `phys_health_consequence`
- `mental_vs_physical`
- `obs_consequence`
- `no_employees`
- `remote_work`
- `tech_company`
- `self_employed`

Context/control variables:

- `Age`
- `Gender`
- `Country`
- `state`

## Data Quality Notes

- `Age` contains invalid values:
  - minimum: -1726
  - maximum: 99,999,999,999
- `Gender` has 49 unique raw values and will need grouping into clean categories.
- `state` has 515 missing values because it mostly applies to US respondents.
- `work_interfere` has 264 missing values and needs a clear missing-value decision.
- `comments` has 1,095 missing values and should probably not be used as a core quantitative variable.

## Recommended Cleaning Decisions

- Keep ages in a reasonable range, such as 18 to 75, and treat impossible ages as missing.
- Standardize gender values into clear categories, such as:
  - Female
  - Male
  - Non-binary / gender diverse
  - Other / unclear
  - Missing
- Keep `state` as optional context only, not as a main analysis variable.
- Create binary variables for modeling:
  - `treatment_yes`
  - `benefits_yes`
  - `care_options_yes`
  - `remote_work_yes`
  - `tech_company_yes`
  - `family_history_yes`
  - `observed_consequence_yes`
- Create grouped/ordered variables:
  - work interference level
  - leave difficulty level
  - company size order
  - discussion comfort with coworkers/supervisors

## Capstone Fit

This dataset is a good fit because it supports:

- segmentation
- hypothesis testing
- logistic regression/classification
- dashboarding
- research-style written reporting

It is also public and separate from the user's private university/Suhkonen capstone work.
