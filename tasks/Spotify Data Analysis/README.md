# Spotify Top 50 Tracks Data Analysis

## Project Overview

This project analyzes the Spotify Top 50 Tracks of 2020 dataset using Python and Pandas. The goal is to clean the data, explore track and artist patterns, and identify which audio features are most visible among popular songs.

The analysis is presented in a Jupyter Notebook so the code, results, and explanations can be read together.

## Files

- `data/spotifytoptracks.csv` - source dataset
- `notebooks/spotify_top_50_eda.ipynb` - completed exploratory data analysis notebook
- `requirements.txt` - Python packages used for the notebook

## Analysis Questions

The notebook answers questions about:

- dataset size, feature types, and data quality
- duplicate samples, duplicate features, missing values, and outliers
- artists and albums with multiple popular tracks
- most represented artists, albums, and genres
- tracks with high or low danceability and loudness
- longest and shortest tracks
- strong positive, strong negative, and weak correlations between audio features
- genre-level comparisons for danceability, loudness, and acousticness

## Key Findings

- The dataset contains 50 tracks.
- After cleaning, the analysis uses 17 working features.
- Billie Eilish, Dua Lipa, and Travis Scott are tied for the highest number of tracks in the dataset.
- Pop is the most common genre, followed by Hip-Hop/Rap.
- `WAP (feat. Megan Thee Stallion)` has the highest danceability score.
- `SICKO MODE` is the longest track, while `Mood (feat. iann dior)` is the shortest.
- Energy and loudness have a strong positive relationship.
- Energy and acousticness have a strong negative relationship.

## Tools Used

- Python
- Pandas
- Jupyter Notebook
- Matplotlib
- Seaborn

## How to Run

From this project folder:

```bash
pip install -r requirements.txt
jupyter notebook notebooks/spotify_top_50_eda.ipynb
```

The notebook expects the dataset at:

```text
data/spotifytoptracks.csv
```

## Improvement Ideas

Future improvements could include adding more years of data, comparing trends over time, grouping similar genres, and adding streaming or popularity metrics to connect audio features with commercial performance.
