
import requests
from utils.config import TMDB_BASE_URL, TMDB_API_KEY, DEFAULT_REGION


def _get(url, params=None):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY non configurata")

    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_genres():
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    data = _get(url, params={"language": "it-IT"})
    return data["genres"]
