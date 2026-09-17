# config.py — all tunables live here so nothing is hard-coded elsewhere.
#
# FEEDS: list of RSS feed URLs to pull from (Ars Technica, The Verge, HN, ...).
FEEDS = []

# TIME_WINDOW_HOURS: how far back to keep items (24 = daily, 72 = every few days).
TIME_WINDOW_HOURS = int

# MAX_ITEMS: cap on how many stories make it into the digest (e.g. 12).
MAX_ITEMS = 15

# MODEL_NAME: which Gemini model (e.g. gemini flash variant).
MODEL_NAME = str

# OUTPUT_PATH: where main.py writes the JSON (../output/digest.json).
OUTPUT_PATH = "output/digest.json"

# Load GEMINI_API_KEY from .env here (python-dotenv), don't paste the key inline.
GEMINI_API_KEY = str

