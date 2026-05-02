# Spotify Top 50 Tracks Data Analysis

This repository is for a beginner-friendly Data Analytics course project.

## Where To Put The Kaggle Dataset

Put the downloaded Kaggle CSV file in this folder:

```text
data/
```

For this project, we will expect the file to be named:

```text
data/spotify_top_50_2020.csv
```

If the downloaded file has a different name, that is okay. We can rename it later or update the code to match the real file name.

## Project Folders

- `data/` - the raw Kaggle dataset goes here.
- `notebooks/` - Jupyter notebooks go here when we start using them.
- `outputs/` - charts, cleaned data, or final exported results go here.
- `notes/` - learning notes and explanations go here.
- `phases/` - task plans and progress notes go here.

## How To Open The Notebook

From the repository root, run:

```bash
cd "tasks/Spotify Data Analysis/notebooks"
```

This command moves your terminal into the notebook folder.

Then run:

```bash
../.venv/bin/jupyter notebook spotify_top_50_eda.ipynb
```

This opens the Spotify analysis notebook in Jupyter.

If the browser does not open automatically, the terminal should show a local link that starts with `http://localhost:`. Copy that link into your browser.

## Python Script Or Jupyter Notebook?

For data analysis, Jupyter Notebook is usually better for learning and presenting your work.

A notebook lets you mix:

- code,
- results,
- charts,
- and written explanations

in one readable document.

A Python script is still useful when you want to run the same code again and again, but it is less friendly for explaining your thinking step by step.

For this course project, the best approach is:

1. Start with Python basics because you are already familiar with `.py` files.
2. Move the final analysis into a Jupyter Notebook so your explanations and results are together.
3. Keep any reusable helper code in Python files if the project becomes larger.

## Next Step

Continue the notebook by identifying which columns are text categories and which columns are numeric measurements.
