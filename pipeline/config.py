# config.py — all tunables live here so nothing is hard-coded elsewhere.

import os
from dotenv import load_dotenv
from pathlib import Path

# FEEDS: list of RSS feed URLs to pull from (Ars Technica, The Verge, HN, ...).
FEEDS = ["https://www.theverge.com/rss/index.xml", "https://techcrunch.com/feed/", "https://www.engadget.com/rss.xml"]

# TIME_WINDOW_HOURS: how far back to keep items (24 = daily, 72 = every few days).
WINDOW_HOURS = 168

# MAX_ITEMS: cap on how many stories make it into the digest (e.g. 12).
MAX_ITEMS = 20

# MODEL_NAME: which Gemini model (e.g. gemini flash variant).
MODEL_NAME = "gemini-3.8-flash"

# OUTPUT_PATH: where main.py writes the JSON (../output/digest.json).
OUTPUT_PATH = Path("output/digest.json")

# Load GEMINI_API_KEY from .env here (python-dotenv), don't paste the key inline.
load_dotenv("pipeline/.env")
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
