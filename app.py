import streamlit as st
import pandas as pd
import numpy as np
import folium

from sklearn.metrics.pairwise import haversine_distances
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Bank Branch Finder",
    page_icon="⌖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --navy: #10233f;
        --blue: #2563eb;
        --blue-light: #eaf2ff;
        --green: #16835b;
        --green-light: #eaf8f2;
        --text: #172033;
        --muted: #697386;
        --line: #e4e8ef;
        --bg: #f6f8fb;
        --white: #ffffff;
        --shadow: 0 14px 35px rgba(16,35,63,.09);
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1240px;
        padding: 1.5rem 2rem 4rem;
    }

    /* Header */
    .bf-header {
        background: #fff;
        border-bottom: 1px solid var(--line);
        margin: -1.5rem -2rem 2rem;
        padding: 14px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .bf-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--navy);
        font-size: 21px;
        font-weight: 800;
    }

    .bf-mark {
        width: 35px;
        height: 35px;
        border-radius: 10px;
        background: var(--navy);
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    /* Hero */
    .bf-hero {
        max-width: 790px;
        margin: 28px auto 34px;
        text-align: center;
    }
