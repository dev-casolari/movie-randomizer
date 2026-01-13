import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def get_movie_details(tmdb_id):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY non configurata")

    url = f"{BASE_URL}/movie/{tmdb_id}"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "Content-Type": "application/json",
    }

    params = {
        "language": "it-IT"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_movie_trailer(tmdb_id):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY non configurata")

    url = f"{BASE_URL}/movie/{tmdb_id}/videos"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "Content-Type": "application/json",
    }

    params = {"language": "it-IT"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # cerca un trailer YouTube ufficiale
    for video in data.get("results", []):
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None

def get_watch_providers(tmdb_id, region="IT"):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY non configurata")

    url = f"{BASE_URL}/movie/{tmdb_id}/watch/providers"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    country = data.get("results", {}).get(region)
    if not country:
        return []

    providers = []

    for p in country.get("flatrate", []):
        providers.append({
            "name": p["provider_name"],
            "logo_path": p.get("logo_path"),
        })

    return providers
