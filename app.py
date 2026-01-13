import streamlit as st

from services.curated_movies import load_curated_movies
from services.movie_service import get_random_movie


st.set_page_config(page_title="Movie Randomizer", page_icon="🎬")
st.title("🎬 Movie Randomizer")

# stato sessione
if "shown_ids" not in st.session_state:
    st.session_state.shown_ids = set()

curated_movies = load_curated_movies()

if st.button("🎲 Suggerisci un film"):
    movie = get_random_movie(curated_movies, st.session_state.shown_ids)

    if movie is None:
        st.warning("Hai visto tutti i film della lista 🎉")
    else:
        st.session_state.current_movie = movie
        st.session_state.shown_ids.add(movie["tmdb_id"])

# render
if "current_movie" in st.session_state:
    st.subheader(st.session_state.current_movie["title"])
    st.write(f"TMDB ID: {st.session_state.current_movie['tmdb_id']}")
