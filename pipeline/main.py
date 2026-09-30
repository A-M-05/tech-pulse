# main.py — run the whole pipeline top to bottom.
#
#   1. load config
#   2. raw   = fetch.fetch_all(FEEDS)
#   3. short = process (filter_recent -> dedupe -> select_top)
#   4. items = summarize.summarize(short)
#   5. wrap items + generated_at into the Digest shape
#   6. serialize to JSON and write to OUTPUT_PATH
#   print a one-line summary (how many items written) so a run is easy to verify.

from fetch import fetch_all
from process import filter_recent, dedupe, select_top
from summarize import summarize
from models import NewsItem, Digest
from dataclasses import asdict
import json
from datetime import datetime, timezone
from config import FEEDS, WINDOW_HOURS, MAX_ITEMS, OUTPUT_PATH
import os
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

raw = fetch_all(FEEDS)
top = select_top(dedupe(filter_recent(raw, WINDOW_HOURS)), MAX_ITEMS)
entries = [NewsItem.from_raw(d) for d in top]
items = summarize(entries)

generated_at = datetime.now(timezone.utc).isoformat()
digest = Digest(generated_at, items)

# Serialize and write to output path
output = json.dumps(asdict(digest), indent = 2)
with open(OUTPUT_PATH, "w", encoding = "utf-8") as output_file:
    output_file.write(output)

print(f"Number of Items: {len(items)}")
