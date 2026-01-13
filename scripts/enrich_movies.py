import csv
import json
import os
import requests
from pathlib import Path
from typing import List, Dict

# =========================
# CONFIG
# =========================

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SHEET_CSV_URL = os.getenv("GOOGLE_SHEET_CSV_URL")

OUTPUT_PATH = Path("data/movies_enriched.json")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_KEY}",
    "Content-Type": "application/json",
}

# -------------------------
# Normalization maps
# -------------------------

TMDB_GENRE_MAP = {
    "Drama": "drama",
    "Crime": "crime",
    "Thriller": "thriller",
    "Mystery": "thriller",
    "Comedy": "comedy",
    "Romance": "romance",
    "Action": "action",
    "Science Fiction": "scifi",
    "Fantasy": "fantasy",
    "Horror": "horror",
    "Animation": "animation",
}

PROVIDER_MAP = {
    "Netflix": "netflix",
    "Amazon Prime Video": "prime",
    "Disney Plus": "disney",
    "Apple TV Plus": "apple",
    "Now TV": "now",
}

# =========================
# HELPERS
# =========================

def require_env(var_name: str):
    if not os.getenv(var_name):
        raise RuntimeError(f"Missing environment variable: {var_name}")


def tmdb_get(endpoint: str):
    url = f"{TMDB_BASE_URL}{endpoint}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


# =========================
# LOAD SHEET
# =========================

def load_movies_from_sheet() -> List[Dict]:
    print("→ Loading Google Sheet")

    response = requests.get(SHEET_CSV_URL)
    response.raise_for_status()

    rows = csv.DictReader(response.text.splitlines())

    movies = []
    for row in rows:
        active = row.get("active", "").strip().lower()
        if active != "true":
            continue

        movies.append({
            "tmdb_id": int(row["tmdb_id"]),
            "title": row.get("title", "").strip(),
        })

    print(f"✓ Loaded {len(movies)} active movies")
    return movies


# =========================
# TMDB FETCH
# =========================

def fetch_tmdb_movie(tmdb_id: int) -> Dict:
    return tmdb_get(f"/movie/{tmdb_id}?language=en-US")


def fetch_watch_providers(tmdb_id: int) -> Dict:
    return tmdb_get(f"/movie/{tmdb_id}/watch/providers")


# =========================
# NORMALIZATION
# =========================

def normalize_genres(tmdb_genres: List[Dict]) -> List[str]:
    genres = []
    for g in tmdb_genres:
        name = g.get("name")
        mapped = TMDB_GENRE_MAP.get(name)
        if mapped and mapped not in genres:
            genres.append(mapped)

    return genres[:2]  # max 2 generi


def normalize_platforms(providers_data: Dict) -> List[str]:
    platforms = []

    country = providers_data.get("results", {}).get("IT")
    if not country:
        return platforms

    for p in country.get("flatrate", []):
        name = p.get("provider_name")
        mapped = PROVIDER_MAP.get(name)
        if mapped and mapped not in platforms:
            platforms.append(mapped)

    return platforms


# =========================
# BUILD RECORD
# =========================

def build_movie_record(base: Dict) -> Dict:
    tmdb_id = base["tmdb_id"]

    movie = fetch_tmdb_movie(tmdb_id)
    providers = fetch_watch_providers(tmdb_id)

    year = None
    if movie.get("release_date"):
        year = int(movie["release_date"][:4])

    record = {
        "tmdb_id": tmdb_id,
        "title": base["title"] or movie.get("title"),
        "year": year,
        "genres": normalize_genres(movie.get("genres", [])),
        "platforms": normalize_platforms(providers),
        "rating": round(movie.get("vote_average", 0), 1),
        "active": True,
    }

    return record


# =========================
# MAIN
# =========================

def main():
    require_env("TMDB_API_KEY")
    require_env("GOOGLE_SHEET_CSV_URL")

    movies = load_movies_from_sheet()
    enriched = []

    print("→ Enriching movies")

    for m in movies:
        try:
            record = build_movie_record(m)
            enriched.append(record)
            print(f"✓ {record['title']}")
        except Exception as e:
            print(f"✗ {m['title']} ({e})")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(enriched)} movies to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
