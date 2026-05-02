# Spotify Top 50 Tracks of 2020 EDA

## Task Summary

We are acting as a data analyst working for Spotify. The goal is to analyze the Spotify Top 50 Tracks of 2020 dataset from Kaggle and answer business and data questions about what makes a hit song.

This task will practice:

- Downloading and working with Kaggle data.
- Loading data with Pandas.
- Cleaning data.
- Performing basic exploratory data analysis, also called EDA.
- Filtering, querying, grouping, and comparing data using Pandas.
- Explaining findings clearly in a notebook.

## Phase Plan

### Phase 1: Project Setup

Goal: Create an organized project structure for the assignment.

Work to do:

- Create folders for data, notebooks, outputs, and notes.
- Add dependency files if needed.
- Add a README explaining how to run the project.

Teaching focus:

- What each folder is for.
- Why data analytics projects should be organized before analysis begins.

Status: Completed.

Progress:

- Created a `data/` folder where the Kaggle CSV file should be placed.
- Created `notebooks/`, `outputs/`, and `notes/` folders for the later parts of the project.
- Added a README with the expected dataset location and a beginner explanation of Python scripts versus Jupyter notebooks.
- Reorganized all Spotify task files under `tasks/Spotify Data Analysis/` so this task is self-contained.
- Confirmed the Spotify CSV file has been added to `tasks/Spotify Data Analysis/data/`.

Current decision:

- We will start in a Python-friendly way because the user has already worked with Python.
- We will likely use a Jupyter Notebook for the final analysis because notebooks are better for data analysis explanations, charts, and project review.

### Phase 2: Get and Load the Dataset

Goal: Download the Spotify Top 50 Tracks of 2020 dataset from Kaggle and load it with Pandas.

Work to do:

- Place the dataset in the project.
- Load the CSV file into a Pandas DataFrame.
- Preview the first rows and column names.

Teaching focus:

- What a CSV file is.
- What a Pandas DataFrame is.
- Why we inspect data before cleaning it.

Status: Completed.

Progress:

- Found the dataset file at `data/spotifytoptracks.csv`.
- Decided to use the real filename in the code instead of renaming it.
- Tried to load the CSV with Pandas, but Pandas was not installed yet.
- Added `requirements.txt` with the Python libraries needed for this analysis.
- Created a project virtual environment in `.venv/`.
- Installed the analysis libraries successfully.
- Loaded the CSV with Pandas and confirmed it has 50 rows and 17 columns.
- Created the first Jupyter Notebook at `notebooks/spotify_top_50_eda.ipynb`.
- Executed the notebook successfully to verify it runs.

### Phase 3: Initial Data Understanding

Goal: Understand the dataset shape, columns, and data types.

Work to do:

- Count observations.
- Count features.
- Identify categorical features.
- Identify numeric features.

Teaching focus:

- Difference between observations and features.
- Difference between categorical and numeric data.

Status: Completed.

Progress:

- Previewed the dataset shape.
- Previewed the column names.
- Previewed the data types.
- Counted 50 observations, meaning 50 song rows.
- Counted 17 features, meaning 17 columns.
- Identified categorical features: `artist`, `album`, `track_name`, `track_id`, and `genre`.
- Identified numeric features: `Unnamed: 0`, `energy`, `danceability`, `key`, `loudness`, `acousticness`, `speechiness`, `instrumentalness`, `liveness`, `valence`, `tempo`, and `duration_ms`.
- Noted that `Unnamed: 0` looks like an old row number and should be handled during cleaning.

### Phase 4: Data Cleaning

Goal: Prepare the dataset for reliable analysis.

Work to do:

- Check and handle missing values.
- Check and remove duplicate rows.
- Check and remove duplicate columns if any exist.
- Detect and decide how to treat outliers.

Teaching focus:

- Why missing values, duplicates, and outliers matter.
- Why we document cleaning decisions instead of silently changing data.

Status: Not started.

### Phase 5: Exploratory Data Analysis

Goal: Answer the required business questions using Pandas.

Work to do:

- Analyze artists, albums, tracks, and genres.
- Filter songs by danceability and loudness.
- Find longest and shortest tracks.
- Compare selected genres.
- Analyze correlations between numeric features.

Teaching focus:

- Filtering rows.
- Grouping and counting.
- Sorting results.
- Reading correlation tables.
- Comparing groups with summary statistics.

Status: Not started.

### Phase 6: Notebook Explanations

Goal: Make the notebook clear for a reader.

Work to do:

- Add explanations before and after code cells.
- Explain what each result means.
- Connect technical findings to business meaning.

Teaching focus:

- How to write analysis for a product manager and senior analyst.
- Difference between code output and insight.

Status: Not started.

### Phase 7: Improvements and Review Preparation

Goal: Prepare final suggestions and review answers.

Work to do:

- Suggest how the analysis could be improved.
- Prepare answers to review questions:
  - What is a DataFrame in Pandas?
  - What makes computation on Pandas so fast?
  - What advantages do Pandas Series objects have over Python lists?

Teaching focus:

- How to explain technical concepts in plain English.
- How to present findings confidently.

Status: Not started.

## Questions To Confirm

1. The dataset folder has been created. The user will put the Kaggle dataset in `data/`.
2. The user has not started with Jupyter Notebook yet and has worked with Python. We will teach notebooks gradually and use them when it helps the analysis.

## Teaching Notes

### What is better for data analysis: Python script or Jupyter Notebook?

A Python script is a plain `.py` file. It is good when you want to run a finished process from start to end.

A Jupyter Notebook is an `.ipynb` file. It is good when you are exploring data because you can run one small section at a time, see the result immediately, add charts, and write explanations beside the code.

For this project, Jupyter Notebook is the better final format because the assignment asks for clear explanations in the notebook. We can still use Python scripts while learning or testing small pieces.
