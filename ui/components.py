
import streamlit as st


def genre_filter_sidebar(genres):
    st.sidebar.header("🎛 Filtri")

    genre_map = {g["name"]: g["id"] for g in genres}

    include = st.sidebar.multiselect(
        "Includi generi",
        options=list(genre_map.keys()),
    )

    exclude = st.sidebar.multiselect(
        "Escludi generi",
        options=list(genre_map.keys()),
    )

    return {
        "include": [genre_map[g] for g in include],
        "exclude": [genre_map[g] for g in exclude],
    }
