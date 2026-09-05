-- Deduplicate raw event data so each user is counted once per event type.
-- Replace `your_project.your_dataset.raw_events` with the real table path.

SELECT
  *
FROM `your_project.your_dataset.raw_events`
QUALIFY
  ROW_NUMBER() OVER (
    PARTITION BY user_pseudo_id, event_name
    ORDER BY event_timestamp, event_date, page_location, transaction_id
  ) = 1;
