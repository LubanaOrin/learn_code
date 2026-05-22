# Coursera Course Dataset Analysis - Phase Plan

## Project Goal

Analyze the Coursera Course Dataset as a data analyst preparing a final assignment for review. The final notebook should be clean, readable, visual, and presentable to a technical reviewer.

Dataset source from assignment brief:
https://www.kaggle.com/datasets/siddharthm1698/coursera-course-dataset

## Files

- Assignment brief: `notes/Coursera Dataset.docx`
- Dataset: `data/coursea_data.csv`
- Final notebook: `notebooks/` folder
- Charts or exported files: `outputs/` folder

## Assignment Requirements

The final work should:

1. Load the dataset using Pandas.
2. Perform careful data cleaning, especially checking every column and differences between rows.
3. Perform exploratory data analysis.
4. Use Matplotlib, Seaborn, or Plotly for visualizations.
5. Explain what each analysis step is trying to achieve.
6. Explain what the results mean.
7. Suggest how the analysis could be improved.
8. Keep code clean, readable, and efficient.
9. Make the notebook presentable for a technical team lead or senior coworker.

## Phase 1 - Project Setup and Data Understanding

Status: Complete

Tasks:

- [x] Read the assignment brief.
- [x] Create organized project folders.
- [x] Copy the dataset into the task folder.
- [x] Inspect the dataset columns, shape, and sample rows.
- [x] Write a clear dataset description.

Dataset description draft:

- The dataset contains 891 Coursera course records.
- Each row represents one course or course-related offering on Coursera.
- The dataset has 7 columns in the raw CSV.
- One column is unnamed and appears to be an old index column, so it should be removed during cleaning.
- Main columns include course title, organization, certificate type, rating, difficulty, and students enrolled.
- There are no missing values in the raw CSV.
- There are no duplicate full rows.
- There are 3 repeated course titles that need closer checking during cleaning.
- `course_students_enrolled` is currently stored as text values such as `5.3k` and `130k`; it should be converted to numeric enrollment counts.
- Ratings range from 3.3 to 5.0, with an average rating of about 4.677.

What this phase teaches:

- How a data analyst starts by understanding the assignment and the dataset before writing analysis.
- Why keeping files organized makes the project easier to review and submit.

## Phase 2 - Data Cleaning

Status: Not started

Tasks:

- [ ] Check column names and rename them if needed.
- [ ] Check missing values.
- [ ] Check duplicate rows and duplicate course titles.
- [ ] Convert enrolled student counts such as `5.3k` and `130k` into numbers.
- [ ] Check whether ratings are valid numeric values.
- [ ] Check category values in certificate type and difficulty.
- [ ] Save or document the cleaned dataset.

What this phase teaches:

- Data cleaning means making the dataset reliable before answering questions.
- Text values like `130k` may look numeric to humans, but Pandas reads them as text until we convert them.

## Phase 3 - Exploratory Data Analysis

Status: Not started

Tasks:

- [ ] Identify top organizations by number of courses.
- [ ] Compare course ratings by difficulty level.
- [ ] Compare course ratings by certificate type.
- [ ] Find the most enrolled courses.
- [ ] Explore relationships between rating and enrollment.
- [ ] Look for interesting patterns or outliers.

What this phase teaches:

- Exploratory data analysis means asking useful questions and using data to answer them.
- Good analysis uses exact numbers, not vague words.

## Phase 4 - Visualizations and Insights

Status: Not started

Tasks:

- [ ] Create bar charts for category counts and top organizations.
- [ ] Create boxplots for rating comparisons.
- [ ] Create a histogram for rating distribution.
- [ ] Create a scatterplot for rating versus enrollment.
- [ ] Write plain-English insights under important charts.

What this phase teaches:

- Charts help readers see patterns faster than tables alone.
- Different questions need different chart types.

## Phase 5 - Final Notebook Polish

Status: Not started

Tasks:

- [ ] Put the notebook in the same order as the assignment requirements.
- [ ] Add a title and dataset description near the top.
- [ ] Add an executive summary with exact numbers.
- [ ] Add limitations and suggestions for improvement.
- [ ] Remove unused code and commented-out experiments.
- [ ] Run the notebook from top to bottom.
- [ ] Confirm the final notebook is ready for review.

What this phase teaches:

- A final notebook is not only code. It is also a report that should communicate clearly.

## Final Checklist

- [ ] Dataset loaded successfully.
- [ ] Cleaning steps are explained.
- [ ] EDA questions are answered with exact numbers.
- [ ] Important findings have visualizations.
- [ ] Notebook has clear markdown explanations.
- [ ] Suggestions for improvement are included.
- [ ] Notebook runs from start to finish without errors.
