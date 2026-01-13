import streamlit as st
import json
from pathlib import Path

DATA_PATH = Path("data/movies_enriched.json")

@st.cache_data(ttl=300)  # 🔁 ricarica ogni 5 minuti
def load_enriched_movies():
    if not DATA_PATH.exists():
        raise RuntimeError("movies_enriched.json non trovato")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
