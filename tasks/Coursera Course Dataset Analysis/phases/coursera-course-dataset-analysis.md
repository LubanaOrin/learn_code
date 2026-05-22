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

Status: Complete

Tasks:

- [x] Check column names and rename them if needed.
- [x] Check missing values.
- [x] Check duplicate rows and duplicate course titles.
- [x] Convert enrolled student counts such as `5.3k` and `130k` into numbers.
- [x] Check whether ratings are valid numeric values.
- [x] Check category values in certificate type and difficulty.
- [x] Save or document the cleaned dataset.

Phase 2 results:

- Created the first notebook: `notebooks/coursera_course_dataset_analysis.ipynb`.
- Added project requirements: `requirements.txt`.
- Installed the required Python packages: Pandas, Jupyter, Matplotlib, and Seaborn.
- Removed the unnamed column because it is an old exported index, not a real course feature.
- Renamed columns to clearer names:
  - `course_organization` became `organization`.
  - `course_Certificate_type` became `certificate_type`.
  - `course_rating` became `rating`.
  - `course_difficulty` became `difficulty`.
  - `course_students_enrolled` became `students_enrolled_raw`.
- Added a numeric `students_enrolled` column.
- Saved the cleaned dataset to `outputs/coursera_courses_cleaned.csv`.

Cleaning checks:

- Cleaned dataset shape: 891 rows and 7 columns.
- Missing values: 0.
- Duplicate full rows: 0.
- Repeated course titles: 3 repeated title cases, affecting 6 rows.
- Rating range: 3.3 to 5.0.
- Enrollment range: 1,500 to 3,200,000 students.
- Certificate types:
  - COURSE: 582.
  - SPECIALIZATION: 297.
  - PROFESSIONAL CERTIFICATE: 12.
- Difficulty levels:
  - Beginner: 487.
  - Intermediate: 198.
  - Mixed: 187.
  - Advanced: 19.

Repeated title note:

The repeated titles are not duplicate rows. They represent different organizations or certificate types, so they should stay in the dataset for analysis:

- `Developing Your Musicianship`
- `Machine Learning`
- `Marketing Digital`

What this phase teaches:

- Data cleaning means making the dataset reliable before answering questions.
- Text values like `130k` may look numeric to humans, but Pandas reads them as text until we convert them.

## Phase 3 - Exploratory Data Analysis

Status: Complete

Tasks:

- [x] Identify top organizations by number of courses.
- [x] Compare course ratings by difficulty level.
- [x] Compare course ratings by certificate type.
- [x] Find the most enrolled courses.
- [x] Explore relationships between rating and enrollment.
- [x] Look for interesting patterns or outliers.

Phase 3 results:

- Added the exploratory data analysis section to `notebooks/coursera_course_dataset_analysis.ipynb`.
- Used the cleaned dataset from `outputs/coursera_courses_cleaned.csv`.
- Found the top organizations by number of courses.
- Compared ratings by difficulty level.
- Compared ratings by certificate type.
- Found the top enrolled courses.
- Checked the correlation between rating and enrollment.
- Compared enrollment patterns by difficulty and certificate type.

Key findings:

- The cleaned dataset contains 891 course records.
- University of Pennsylvania has the most courses in the dataset, with 59 courses.
- University of Michigan is second with 41 courses.
- Google Cloud is third with 34 courses.
- Mixed-difficulty courses have the highest average rating at 4.709.
- Advanced courses have the lowest average rating at 4.600, but there are only 19 Advanced courses.
- Regular courses have the highest average rating by certificate type at 4.707.
- Specializations have an average rating of 4.618.
- The most enrolled course is Stanford University's `Machine Learning`, with 3,200,000 students.
- The second most enrolled course is Yale University's `The Science of Well-Being`, with 2,500,000 students.
- The correlation between rating and enrollment is 0.0711, which means there is no strong linear relationship between rating and enrollment in this dataset.
- Mixed-difficulty courses have the highest median enrollment by difficulty, with 62,000 students.
- Professional certificates have the highest median enrollment by certificate type, with 145,000 students, but there are only 12 professional certificate records.

Important interpretation:

Enrollment is skewed by a few very large courses. This means the average enrollment can be pulled upward by unusually popular courses, so median enrollment is often more useful for comparing typical courses.

What this phase teaches:

- Exploratory data analysis means asking useful questions and using data to answer them.
- Good analysis uses exact numbers, not vague words.

## Phase 4 - Visualizations and Insights

Status: Complete

Tasks:

- [x] Create bar charts for category counts and top organizations.
- [x] Create boxplots for rating comparisons.
- [x] Create a histogram for rating distribution.
- [x] Create a scatterplot for rating versus enrollment.
- [x] Write plain-English insights under important charts.

Phase 4 results:

- Added a visualization section to `notebooks/coursera_course_dataset_analysis.ipynb`.
- Reran the notebook successfully from top to bottom.
- Saved chart images in `outputs/charts/`.

Charts created:

- `top_organizations_by_course_count.png`
- `course_count_by_certificate_type.png`
- `rating_distribution.png`
- `ratings_by_difficulty.png`
- `ratings_by_certificate_type.png`
- `rating_vs_enrollment.png`

Key visualization insights:

- Bar charts show that University of Pennsylvania, University of Michigan, and Google Cloud are the most common organizations in the dataset.
- The certificate type bar chart shows that regular courses dominate the dataset with 582 records.
- The rating histogram shows that ratings are concentrated near the high end of the scale.
- The difficulty boxplot shows that all difficulty groups have generally high ratings.
- The certificate type boxplot shows that regular courses have the highest average rating, but all groups rate strongly.
- The scatterplot shows no strong visual relationship between rating and enrollment, matching the weak correlation of 0.0711.

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
