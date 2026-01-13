import streamlit as st
import streamlit.components.v1 as components

from services.curated_movies import load_curated_movies
from services.movie_service import get_random_movie
from services.tmdb_client import get_movie_details
from services.tmdb_client import get_movie_trailer
from services.tmdb_client import get_watch_providers


# -----------------------
# Page config
# -----------------------
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
# Session state
# -----------------------
if "shown_ids" not in st.session_state:
    st.session_state.shown_ids = set()

if "current_movie" not in st.session_state:
    st.session_state.current_movie = None

# -----------------------
# Load curated list
# -----------------------
curated_movies = load_curated_movies()

# -----------------------
# Action button (UNICO)
# -----------------------
if st.button("🎲 Suggerisci un film"):
    movie = get_random_movie(curated_movies, st.session_state.shown_ids)

    if movie is None:
        st.warning("Hai visto tutti i film della lista 🎉")
    else:
        details = get_movie_details(movie["tmdb_id"])
        st.session_state.current_movie = details
        st.session_state.shown_ids.add(movie["tmdb_id"])

# -----------------------
# Render movie
# -----------------------
if st.session_state.current_movie:
    m = st.session_state.current_movie

    st.markdown("---")

    col_poster, col_info, col_stream = st.columns([1, 2, 1])

    # Poster
    with col_poster:
        if m.get("poster_path"):
            poster_url = f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
            st.image(poster_url, width=280)

    # Info film
    with col_info:
        st.subheader(m["title"])

        year = m.get("release_date", "")[:4]
        rating = round(m.get("vote_average", 0), 1)
        st.caption(f"{year} · ⭐ {rating}/10")

        st.write(m.get("overview", "Trama non disponibile."))

    # Streaming
    with col_stream:
        st.markdown("### 📺 Dove guardarlo")

        providers = get_watch_providers(m["id"])

        if providers:
            cols = st.columns(len(providers[:5]))

            for col, p in zip(cols, providers[:5]):
                with col:
                    if p["logo_path"]:
                        logo_url = f"https://image.tmdb.org/t/p/w45{p['logo_path']}"
                        st.image(logo_url)
        else:
            st.caption("Non disponibile in streaming.")

    
    ### --- TRAILER
    trailer_url = get_movie_trailer(m["id"])

    if trailer_url:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎬 Trailer")
        st.markdown(f"[Guarda il trailer su YouTube]({trailer_url})")



    

