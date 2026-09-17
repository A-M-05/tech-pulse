# main.py — run the whole pipeline top to bottom.
#
#   1. load config
#   2. raw   = fetch.fetch_all(FEEDS)
#   3. short = process (filter_recent -> dedupe -> select_top)
#   4. items = summarize.summarize(short)
#   5. wrap items + generated_at into the Digest shape
#   6. serialize to JSON and write to OUTPUT_PATH
#   print a one-line summary (how many items written) so a run is easy to verify.
