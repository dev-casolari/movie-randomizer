
import streamlit as st
from services.tmdb_client import get_genres
from ui.components import genre_filter_sidebar


st.set_page_config(
    page_title="Movie Randomizer",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Movie Randomizer")

try:
    genres = get_genres()
except Exception as e:
    st.error(str(e))
    st.stop()

filters = genre_filter_sidebar(genres)

st.write("Filtri selezionati:")
st.json(filters)
