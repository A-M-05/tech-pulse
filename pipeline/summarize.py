# summarize.py — add AI summaries + categories to the shortlisted entries.
#
# summarize(entries) -> list[NewsItem]:
#   build a prompt asking for a 2–3 sentence summary + a category per story.
#   >>> DECISION 1: blurb-only (send the RSS description) vs full-article
#       (fetch the page text first). Start blurb-only; leave a TODO to upgrade.
#   >>> DECISION 2: per-item calls (simple) vs one batched call returning a
#       JSON array (fewer requests). Structure this function so you can swap later.
#   ask the model to return structured/JSON output so parsing is reliable.
#   map each result onto a NewsItem from models.py.
#   keep API-key handling out of here — read it from config.
