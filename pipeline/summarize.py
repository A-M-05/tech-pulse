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

from models import NewsItem
import html, re
from pydantic import BaseModel
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, MODEL_NAME
import time
from google.genai.errors import ServerError
from typing import cast

client = genai.Client(api_key = GEMINI_API_KEY)

class SummaryResult(BaseModel):
    id : str
    summary : str
    category : str


def clean(text : str):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text

def call_gemini(prompt, retries=3):
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model = MODEL_NAME,
                contents = prompt,
                config = types.GenerateContentConfig(
                    response_mime_type = "application/json",
                    response_schema = list[SummaryResult],
                ),
            )
        except ServerError:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("call_gemini exhausted retries")

def summarize(entries : list[NewsItem]) -> list[NewsItem]:
    items_block = ""
    for entry in entries:
        blurb = clean(entry.blurb)
        if not blurb:
            blurb = "no blurb"
        line = f"id: {entry.id} | title: {entry.title} | blurb: {blurb}"
        items_block += line + "\n"

    prompt = f"""You summarize tech news. For each article below, write a 2-3 sentence summary and assign exactly one category from this list: hardware, software, ai, company-news, other.

Rules:
- Base the summary only on the title and blurb provided. Do not invent facts not present in them.
- Return the id for each article exactly as given, unchanged.
- Respond with ONLY a JSON array — no markdown, no code fences, no extra text.
- Each object must have exactly these keys: "id", "summary", "category".

Articles:
{items_block}"""

    response = call_gemini(prompt)
    if response.parsed is None:
        raise ValueError("Model returned unparseable output")
    
    results = cast(list[SummaryResult], response.parsed)
    if results is None:
        raise ValueError("Model returned unparseable output")
    
    lookup = {r.id : r for r in results}

    for entry in entries:
        result = lookup.get(entry.id)
        if result is None:
            continue
        entry.summary = result.summary
        entry.category = result.category
    
    return entries

if __name__ == "__main__":
    from fetch import fetch_all
    from process import filter_recent, dedupe, select_top

    FEEDS = [
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
        "https://www.engadget.com/rss.xml",
    ]

    raw = fetch_all(FEEDS)
    top = select_top(dedupe(filter_recent(raw, 48)), 5)   # 5 items = short prompt to eyeball
    entries = [NewsItem.from_raw(d) for d in top]          # dicts -> NewsItems (normalize)

    print(summarize(entries))