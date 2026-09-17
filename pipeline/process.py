# process.py — take raw entries, return the final shortlist to summarize.
#
# filter_recent(entries, window_hours): drop anything older than the window.
#   (watch out: feeds use different date formats — normalize before comparing.)
# dedupe(entries): remove repeats. v1 = dedupe by URL. (smarter = title similarity.)
# select_top(entries, max_items): pick the final N (by recency, or source priority).
#
# Output: a clean list ready for summarize.py. Still NO AI calls here.
