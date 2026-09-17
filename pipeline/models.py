# models.py — the shape of ONE digest item. This is the contract.
#
# Define a dataclass (e.g. NewsItem) with the fields the app needs:
#   id         : stable unique id (hash of the URL works)
#   title      : headline
#   source     : which outlet it came from
#   url        : link to the original article (for "open article")
#   published  : publish timestamp, ISO 8601 string (Swift decodes this cleanly)
#   summary    : the AI-written 2–3 sentence summary
#   category   : e.g. "hardware", "software", "company-news"
#
# Also consider a top-level wrapper (e.g. Digest) holding:
#   generated_at : when this run produced the file
#   items        : list[NewsItem]
# Decide the JSON key names now — the Swift structs must match them exactly.