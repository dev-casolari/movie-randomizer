import random

def get_random_movie(movies, filters=None, excluded_ids=None):
    excluded_ids = excluded_ids or set()
    filters = filters or {}

    candidates = []

    for m in movies:
        if not m.get("active", True):
            continue

        if m["tmdb_id"] in excluded_ids:
            continue

        # filtro genere
        if "genre" in filters:
            if filters["genre"] not in m["genres"]:
                continue

        # filtro piattaforma
        if "platform" in filters:
            if filters["platform"] not in m["platforms"]:
                continue

        # filtro anno minimo
        if "min_year" in filters:
            if not m["year"] or m["year"] < filters["min_year"]:
                continue

        candidates.append(m)

    if not candidates:
        return None

    return random.choice(candidates)
