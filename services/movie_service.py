
import random


def get_random_movie(curated_movies, excluded_ids):
    available = [
        m for m in curated_movies
        if m["tmdb_id"] not in excluded_ids
    ]

    if not available:
        return None

    return random.choice(available)
