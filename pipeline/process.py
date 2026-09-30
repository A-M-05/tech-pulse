# process.py — take raw entries, return the final shortlist to summarize.
#
# filter_recent(entries, window_hours): drop anything older than the window.
#   (watch out: feeds use different date formats — normalize before comparing.)
# dedupe(entries): remove repeats. v1 = dedupe by URL. (smarter = title similarity.)
# select_top(entries, max_items): pick the final N (by recency, or source priority).
#
# Output: a clean list ready for summarize.py. Still NO AI calls here.

import calendar, time

def filter_recent(entries : list[dict], window_hours : int) -> list[dict]:
    recents = []
    for entry in entries:
        date = entry["date"]

        if date is None:
            continue

        epoch = calendar.timegm(date)
        if epoch > (time.time() - window_hours * 3600):
            recents.append(entry)

    return recents

def dedupe(entries : list[dict]) -> list[dict]:
    deduped = []
    seen = set()
    for entry in entries:
        link = entry["link"]
        if link not in seen:
            seen.add(link)
            deduped.append(entry)

    return deduped

def select_top(entries : list[dict], max_items : int) -> list[dict]:
    entries = sorted(entries, key = lambda e: e["date"], reverse = True)
    return entries[:max_items]


if __name__ == "__main__":
    # Test
    from fetch import fetch_all

    FEEDS = [
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
        "https://www.engadget.com/rss.xml",
    ]
    WINDOW_HOURS = 48
    MAX_ITEMS = 10

    raw = fetch_all(FEEDS)
    print(f"fetched: {len(raw)}")

    recent = filter_recent(raw, WINDOW_HOURS)
    print(f"recent: {len(recent)}")

    deduped = dedupe(recent)
    print(f"deduped: {len(deduped)}")

    top = select_top(deduped, MAX_ITEMS)
    print(f"top: {len(top)}")

    print("\n--- final shortlist ---")
    for item in top:
        print(f"[{item['source']}] {item['title']}")

