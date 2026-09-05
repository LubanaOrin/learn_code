# Coursera Course Dataset Analysis

## Project Overview

This project explores a Coursera course dataset using Python, Pandas, Matplotlib, and Seaborn. The analysis focuses on course providers, certificate types, difficulty levels, ratings, enrollment patterns, and the relationship between course popularity and user ratings.

The final work is available as both a Jupyter Notebook with visible code and an HTML presentation version for easier reading.

## Files

- `data/coursea_data.csv` - original source dataset
- `notebooks/coursera_course_dataset_analysis.ipynb` - completed analysis notebook
- `outputs/coursera_course_dataset_presentation.html` - presentation-friendly HTML export
- `outputs/coursera_courses_cleaned.csv` - cleaned dataset used for analysis
- `outputs/charts/` - exported visualization images
- `requirements.txt` - Python packages used in the notebook

## Analysis Focus

The notebook covers:

- dataset structure and column cleanup
- missing value and duplicate checks
- enrollment conversion from text values into numeric values
- rating validation and category checks
- top course organizations by course count
- certificate type distribution
- rating patterns by difficulty and certificate type
- most enrolled courses
- relationship between rating and enrollment
- enrollment comparison across key course groups

## Key Findings

- Course certificates make up the largest share of the dataset.
- Beginner-level courses are the most common difficulty level.
- Many courses have high ratings, so enrollment is not explained by rating alone.
- Some organizations appear repeatedly, suggesting strong catalog presence.
- Enrollment is highly skewed, with a small number of courses attracting very large audiences.

## Tools Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## How to Run

From this project folder:

```bash
pip install -r requirements.txt
cd notebooks
jupyter notebook coursera_course_dataset_analysis.ipynb
```

The notebook expects the dataset at:

```text
../data/coursea_data.csv
```

## Improvement Ideas

Future improvements could include adding course subject categories, review counts, pricing data, completion metrics, and time-based trends to better explain what drives course demand.
