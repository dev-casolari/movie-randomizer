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

PLATFORM_OPTIONS = {
    "Qualsiasi": None,
    "Netflix": "netflix",
    "Amazon Prime": "prime",
    "Disney+": "disney",
    "Now TV": "now",
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
st.session_state.setdefault("last_platform", None)
st.session_state.setdefault("no_more_movies", False)

# -----------------------
# Data
# -----------------------

movies = load_enriched_movies()

# -----------------------
# Filters
# -----------------------

cols = st.columns([0.1, 0.1, 0.1, 0.1, 0.1, 0.6])

with cols[0]:
    label = st.selectbox(
        "Che tipo di film?",
        options=list(GENRE_OPTIONS.keys()),
        index=0,
    )

    selected_genre = GENRE_OPTIONS[label]

with cols[1]:
    platform = st.selectbox(
        "Piattaforma",
        options=list(PLATFORM_OPTIONS.keys()),
        index=0,
    )

    selected_platform = PLATFORM_OPTIONS[platform]

# reset history if filter changes
if st.session_state.last_genre != selected_genre or st.session_state.last_platform != selected_platform:
    st.session_state.shown_ids.clear()
    st.session_state.no_more_movies = False
    st.session_state.last_genre = selected_genre
    st.session_state.last_platform = selected_platform

# -----------------------
# Action
# -----------------------

if not st.session_state.no_more_movies:
    if st.button("🎲 Suggerisci un film"):
        filters = {}
        if selected_genre:
            filters["genre"] = selected_genre
        if selected_platform:
            filters["platform"] = selected_platform

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

    col_poster, col_info, col_trailer = st.columns([0.2, 0.4, 0.4])

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

        st.markdown("### 📺 Dove guardarlo")
        providers = get_watch_providers(m["id"])
        if providers:
            cols = st.columns(10)
            for i, col in enumerate(cols):
                if i < len(providers):
                    p = providers[i]
                    with col:
                        if p.get("logo_path"):
                            st.image(
                                f"https://image.tmdb.org/t/p/w45{p['logo_path']}"
                            )
        else:
            st.caption("Non disponibile in streaming.")

    with col_trailer:
        trailer = get_movie_trailer(m["id"])
        if trailer:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🎬 Trailer")
            # st.markdown(f"[Guarda il trailer su YouTube]({trailer})")
            st.video(trailer)
