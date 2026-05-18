# Repository Instructions

This repository supports a beginner Data Analytics course.

The user is not a software engineer and is learning programming while completing course tasks. For course assignment tasks in this repository:

1. Create a phase document for the task before doing the main work.
2. Organize everything related to a task inside that task's own folder under `tasks/`.
3. For the Spotify project, use `tasks/Spotify Data Analysis/`.
4. Inside each task folder, use folders such as `data/`, `notebooks/`, `outputs/`, `notes/`, and `phases/`.
5. Store phase documents inside the task's `phases/` folder.
6. Name phase documents clearly, for example `phases/spotify-top-50-eda.md`.
7. Use the phase document to track the plan, progress, explanations, and final checklist.
8. Start by making a clear phased plan.
9. Complete the task phase by phase.
10. Teach what was done after each phase.
11. Use beginner-friendly explanations.
12. Avoid assuming prior programming knowledge.
13. Explain technical terms in plain English.
14. Keep files organized and easy to review.
15. Show exactly how to run, test, or check the result.

For future data analytics notebooks, also follow these reviewer lessons:

16. Structure the final notebook in the same order as the assignment requirements unless the user asks for a different format.
17. Add a dataset description near the top: source, number of rows, number of columns, what one row represents, and what the main columns mean.
18. Include a short executive summary near the top when useful, especially for reviewers or non-technical readers.
19. Put numbers in summaries and insights. Avoid weak wording like "most", "many", or "lots" unless it is supported by exact counts, percentages, or values.
20. Add visualizations for important findings. Data analysts should make results understandable for non-technical people, not only show tables.
21. Use appropriate charts such as bar charts for counts, boxplots for comparing distributions between groups, histograms for numeric distributions, scatterplots for relationships, and heatmaps for correlations.
22. When comparing groups, do not rely only on averages. Use visual checks such as boxplots and remember the lesson of Anscombe's quartet: datasets can have the same summary statistics but very different shapes.
23. Avoid unnecessary `for` loops in Pandas work. Prefer Pandas methods such as `value_counts()`, `groupby()`, `agg()`, `duplicated()`, `corr()`, `stack()`, and boolean filtering.
24. For duplicate feature checks, prefer vectorized Pandas patterns such as transposing the DataFrame and using `df.T.duplicated()` instead of manual nested loops.
25. For correlation-pair analysis, prefer creating the correlation matrix, masking one triangle, and using `.stack()` to turn it into a clean pair table instead of manually looping through column pairs.
26. Avoid chained indexing. Use `.loc[row_filter, column_list]` when filtering rows and selecting columns at the same time.
27. Keep code quality suitable for evaluation: readable variable names, no commented-out experiments, no unused code, PEP8-friendly formatting, and simple reusable variables for repeated column lists.
28. For presentation notebooks, make the notebook readable with markdown explanations and visuals. If needed at the end, code cells can be hidden or collapsed for a cleaner non-technical presentation view, while keeping the code available for review.

For small repository housekeeping tasks, such as fixing documentation wording, Git setup, or cleaning confusing helper files, do not create extra task folders under `tasks/`. Keep those changes simple and document only what is useful in `AGENTS.md`, `CODEx.md`, or the relevant existing task folder.

Preferred response style:

- Plain English first.
- Short plan before implementation.
- Keep responses concise and avoid repeating the user's command or request unless it is needed for clarity.
- Share only command output that is relevant for teaching, checking results, or deciding the next step.
- Keep the phase document updated as the task progresses.
- Explain why each step matters.
- When writing code, explain the important lines.
- When using terminal commands, explain what each command does.
- Do not skip teaching moments.

The goal is both to complete assignments and to help the user understand data analytics tools, programming concepts, and workflow habits.
