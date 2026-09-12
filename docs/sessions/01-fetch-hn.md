# Session 01 — fetch_hn

## Prompt

Write src/fetch_hn.py. Hit http://hn.algolia.com/api/v1/search_by_date with params
tags=story, query="Launch HN", numericFilters=created_at_i>{90 days ago as unix
timestamp}, hitsPerPage=50. Save the raw JSON response to cache/hn_raw.json before
parsing. Then print one row per story: title, points, num_comments, url. Plain
script, no classes, runs with python src/fetch_hn.py.
