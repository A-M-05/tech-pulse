# TechPulse

A personal tech-news app for iPhone that pulls the latest hardware, software, AI, and industry headlines, summarizes them with AI, and shows them in a clean app and a rotating home-screen widget.

## How it works

TechPulse is a small end-to-end system in one repo:

1. **Pipeline (`pipeline/`, Python)** — fetches recent articles from tech RSS feeds (The Verge, TechCrunch, Engadget), filters by recency, de-duplicates (by URL and title similarity), and sends the top stories to Google Gemini for 2–3 sentence summaries and a category. Writes `output/digest.json`.
2. **Automation (`.github/`)** — a GitHub Action runs the pipeline on a weekly schedule and commits the fresh `digest.json` back to the repo, served over HTTPS via raw GitHub.
3. **Proxy (`proxy/`, Cloudflare Worker)** — a tiny serverless endpoint that holds the Gemini API key server-side and relays the app's "Tell me more" deep-dive requests, so no key ever ships in the app.
4. **App (`app/`, Swift / SwiftUI)** — fetches the digest, shows a scrollable list and a detail view with an AI "Tell me more" deep-dive (cached, with retry), plus a WidgetKit home-screen widget that rotates through the latest stories.

## Architecture

```
RSS feeds ─► pipeline (Python + Gemini) ─► digest.json ─► raw GitHub (HTTPS)
                   ▲                                           │
            GitHub Action (weekly)                            ▼
                                                   iOS app ◄── fetch
                                                       │
                                        "Tell me more" ▼
                                              Cloudflare Worker ─► Gemini
```

## Tech stack

Python (feedparser, google-genai, pydantic) · Google Gemini API · GitHub Actions · Cloudflare Workers (JavaScript) · Swift / SwiftUI / WidgetKit

## Run the pipeline locally

```bash
cd pipeline
pip install -r requirements.txt
# add GEMINI_API_KEY to pipeline/.env
python main.py        # writes ../output/digest.json
```

## Deploy the proxy

```bash
cd proxy
npx wrangler deploy
# key is stored as a Cloudflare secret, not in code:
npx wrangler secret put GEMINI_API_KEY
```

## Notes

- API keys are never committed — the pipeline reads `pipeline/.env` (gitignored); the Worker reads a Cloudflare secret. The app ships no key.
- The app talks only to the public digest URL and the Worker proxy.

## Roadmap

- TestFlight / notarized distribution for easier sharing
- macOS (Mac Catalyst) build
- Full-article summaries (vs. RSS blurb only)
- Semantic (LLM-based) de-duplication
