
import json
from pathlib import Path

DATA_PATH = Path("data/curated_movies.json")


def load_curated_movies():
    if not DATA_PATH.exists():
        raise RuntimeError("File curated_movies.json non trovato")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
