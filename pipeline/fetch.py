# fetch.py — turn feed URLs into raw, unprocessed entries.
#
# fetch_all(feeds) -> list of raw entries:
#   for each feed URL, parse it (feedparser) and collect its entries.
#   from each entry pull: title, link, summary/description, published date, source.
#   don't filter or dedupe here — that's process.py's job. Just normalize the
#   messy feed fields into a consistent intermediate dict/object.
#   handle a feed that fails to load without crashing the whole run.

import feedparser as fp

def fetch_all(feeds : list[str]):
    results = []

    for feed in feeds:
        try:
            parsed = fp.parse(feed)
            entries = parsed.entries
            if not entries:
                    print(f"SOMETHING WENT WRONG WITH {feed}")
                    print(f"{parsed.bozo} | {parsed.bozo_exception}")
                    print("MOVING TO NEXT FEED")
                    continue
            source = parsed.feed.title

            for entry in entries:
                group = dict()

                title = entry.get("title")
                group["title"] = title

                link = entry.get("link")
                group["link"] = link

                summary = entry.get("summary")
                group["summary"] = summary

                date = entry.get("published_parsed")
                group["date"] = date

                group["source"] = source

                results.append(group)
        except Exception as e:
            print(f"FEED URL: {feed}")
            print(e)
            continue

    return results

