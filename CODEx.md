# Data Analytics Course Workflow

This repository is for my Data Analytics course tasks.

## How Codex Should Help

I am not a software engineer and I am learning programming as part of data analytics. For every task I give, Codex should:

1. Break the task into clear phases before starting.
2. Complete one phase at a time.
3. Explain what was done in each phase in beginner-friendly language.
4. Teach the programming or data analytics concept behind the work.
5. Avoid assuming I already know technical terms.
6. Use simple examples where helpful.
7. Keep code and files organized so I can review them later.
8. Tell me exactly how to run or check the work.

For data analytics projects, Codex should also help me think like a data analyst:

9. Make the final notebook follow the assignment requirements in order, so reviewers can check it easily.
10. Add a clear dataset description near the top of the notebook.
11. Add a short summary near the top when useful, especially for non-technical readers.
12. Use exact numbers in summaries and conclusions. Numbers are proof. Avoid vague words like "most", "many", or "lots" unless the exact count, percentage, or value is also shown.
13. Include visualizations for important findings, because data analysis should communicate clearly to non-technical people.
14. Use charts that match the question:
    - Bar charts for category counts.
    - Boxplots for comparing numeric values across groups.
    - Histograms for numeric distributions.
    - Scatterplots for relationships between two numeric columns.
    - Heatmaps for correlation tables.
15. Do not rely only on averages when comparing groups. Use visual checks such as boxplots, because Anscombe's quartet shows that averages and correlations can hide very different data shapes.
16. Prefer Pandas methods over manual loops when possible.
17. Avoid chained indexing. Use `.loc[row_filter, column_list]` when filtering rows and choosing columns together.
18. For duplicate feature checks, prefer Pandas approaches such as `df.T.duplicated()` instead of nested loops.
19. For correlation-pair analysis, prefer `corr()`, masking one triangle, and `.stack()` instead of manually looping over column pairs.
20. Keep code clean for evaluation: readable variable names, PEP8-friendly formatting, no unused code, and no commented-out experiment code.
21. For final presentation, help me make the notebook readable with markdown explanations and visuals. Code cells can be hidden or collapsed at the end if the presentation needs a cleaner look, but the code should remain available for review.

## Preferred Response Style

- Start with a short plan.
- Use plain English.
- Explain why each step matters.
- When code is written, explain the important lines.
- When a command is needed, show the command and what it does.
- Do not move too fast or skip explanations.

## Task Workflow

For each new task:

1. Understand the task.
2. Create a phased plan.
3. Create or update the phase document.
4. Implement Phase 1.
5. Explain Phase 1.
6. Continue with the next phase until the task is complete.
7. Check the final notebook against the assignment requirements and evaluation criteria.
8. Finish with a short summary, next steps, and exact commands for saving or submitting.

## Data Analysis Notebook Checklist

For future notebooks, include these parts unless the assignment says otherwise:

1. Title.
2. Dataset description.
3. Executive summary with exact numbers.
4. Data loading.
5. Data cleaning.
6. Exploratory data analysis in the same order as the assignment questions.
7. Visualizations for key findings.
8. Clear explanations of what each result means.
9. Suggestions for improvement.
10. Limitations.
11. Final check that the notebook runs from top to bottom.

## Repository Organization

- Keep each course assignment in its own folder under `tasks/`.
- For the Spotify Data Analysis project, use `tasks/Spotify Data Analysis/`.
- Inside task folders, use clear subfolders such as `data/`, `notebooks/`, `outputs/`, `notes/`, and `phases/`.
- Store phase documents in the task's `phases/` folder.
- Do not create extra task folders for small housekeeping work such as Git setup or documentation cleanup.

## Learning Goal

The main goal is not only to finish assignments, but also to help me understand what was done so I can gradually become more confident with data analytics tools and programming.
