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

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, calendar
import html

@dataclass
class NewsItem:
    id : str
    title : str
    source : str
    url : str
    published : str
    summary : str = ""
    category : str = ""
    blurb : str = ""

    @classmethod
    def from_raw(cls, raw : dict) -> "NewsItem":
        url = raw["link"]
        id = hashlib.sha1(url.encode()).hexdigest()[:12]
        epoch = calendar.timegm(raw["date"])
        published = datetime.fromtimestamp(epoch, tz = timezone.utc).isoformat()
        title = html.unescape(raw["title"])
        source = html.unescape(raw["source"])
        blurb = raw.get("summary") or ""

        return cls(id = id, title = title, source = source, url = url, published = published, blurb = blurb)
    
@dataclass
class Digest:
    generated_at : str
    items : list[NewsItem] = field(default_factory = list)


if __name__ == "__main__":
    import time

    sample = {
        "title": "BYD says its new solid-state EV battery tech is nearly ready",
        "link": "https://www.engadget.com/transportation/byd-solid-state-battery",
        "summary": "BYD announced its solid-state battery is close to production &#8230;",
        "date": time.struct_time((2026, 9, 17, 3, 0, 0, 3, 260, 0)),
        "source": "Engadget",
    }

    item = NewsItem.from_raw(sample)
    print(item)
    print("id:", item.id)
    print("published:", item.published)
    print("summary/category (should be empty):", repr(item.summary), repr(item.category))