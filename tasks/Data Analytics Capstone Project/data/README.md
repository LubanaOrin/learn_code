# Data Folder

## Planned Dataset

Selected dataset:

**OSMI Mental Health in Tech Survey**

Source:

https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

Local files:

- `osmi-mental-health-in-tech-survey.zip`
- `osmi-mental-health-in-tech-survey/survey.csv`

## Download Status

As of 2026-06-10, the survey result pages are accessible, but the direct ZIP URLs tested from the terminal returned 404 pages instead of real ZIP files.

The user downloaded the Kaggle archive and provided it as `/Users/lubana/Downloads/archive.zip`.

The archive was copied into this folder as `osmi-mental-health-in-tech-survey.zip` and extracted into `osmi-mental-health-in-tech-survey/`.

## Expected Files

After download and extraction, this folder should contain files similar to:

- `survey.csv`

## Why We Save The Raw Data Here

Saving the raw survey files makes the project reproducible. Reproducible means another person can run the analysis again using the same input data and check how the results were produced.

## Dataset Summary

- Rows: 1,259
- Columns: 27
- One row represents one survey response.
- Full inventory note: `notes/osmi-dataset-inventory.md`
