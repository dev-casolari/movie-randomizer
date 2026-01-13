import streamlit as st

from services.enriched_movies import load_enriched_movies
from services.movie_service import get_random_movie
from services.tmdb_client import (
    get_movie_details,
    get_movie_trailer,
    get_watch_providers,
)

# -----------------------
# Config
# -----------------------

GENRE_OPTIONS = {
    "Qualsiasi": None,
    "Crime": "crime",
    "Thriller": "thriller",
    "Drama": "drama",
    "Comedy": "comedy",
    "Action": "action",
    "Sci-Fi": "scifi",
    "Horror": "horror",
}

st.set_page_config(
    page_title="Movie Randomizer",
    page_icon="🎬",
    layout="wide",
)

# -----------------------
# Header
# -----------------------

st.markdown("## 🎬 Movie Randomizer")
st.caption("Un suggerimento alla volta. Solo film curati.")
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------
# State
# -----------------------

st.session_state.setdefault("shown_ids", set())
st.session_state.setdefault("current_movie", None)
st.session_state.setdefault("last_genre", None)
st.session_state.setdefault("no_more_movies", False)

# -----------------------
# Data
# -----------------------

movies = load_enriched_movies()

# -----------------------
# Filter (single, light)
# -----------------------

label = st.selectbox(
    "Che tipo di film?",
    options=list(GENRE_OPTIONS.keys()),
    index=0,
)

selected_genre = GENRE_OPTIONS[label]

# reset history if filter changes
if st.session_state.last_genre != selected_genre:
    st.session_state.shown_ids.clear()
    st.session_state.no_more_movies = False   # 👈 aggiungi
    st.session_state.last_genre = selected_genre

# -----------------------
# Action
# -----------------------

if not st.session_state.no_more_movies:
    if st.button("🎲 Suggerisci un film"):
        filters = {"genre": selected_genre} if selected_genre else {}

        movie = get_random_movie(
            movies,
            filters=filters,
            excluded_ids=st.session_state.shown_ids,
        )

        if movie:
            st.session_state.current_movie = get_movie_details(movie["tmdb_id"])
            st.session_state.shown_ids.add(movie["tmdb_id"])
        else:
            st.session_state.no_more_movies = True
else:
    st.info("Non ci sono altri film disponibili 🎬")

    if st.button("🔄 Ricomincia"):
        st.session_state.shown_ids.clear()
        st.session_state.current_movie = None
        st.session_state.no_more_movies = False

# -----------------------
# Render
# -----------------------

if st.session_state.current_movie:
    m = st.session_state.current_movie

    col_poster, col_info, col_stream = st.columns([1, 2, 1])

    with col_poster:
        if m.get("poster_path"):
            st.image(
                f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
                width=280,
            )

    with col_info:
        st.subheader(m["title"])
        year = m.get("release_date", "")[:4]
        rating = round(m.get("vote_average", 0), 1)
        st.caption(f"{year} · ⭐ {rating}/10")
        st.write(m.get("overview", "Trama non disponibile."))

    with col_stream:
        st.markdown("### 📺 Dove guardarlo")
        providers = get_watch_providers(m["id"])

        if providers:
            cols = st.columns(min(len(providers), 5))
            for col, p in zip(cols, providers[:5]):
                with col:
                    if p.get("logo_path"):
                        st.image(
                            f"https://image.tmdb.org/t/p/w45{p['logo_path']}"
                        )
        else:
            st.caption("Non disponibile in streaming.")

    trailer = get_movie_trailer(m["id"])
    if trailer:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎬 Trailer")
        st.markdown(f"[Guarda il trailer su YouTube]({trailer})")
