import streamlit as st

import pandas as pd

import numpy as np



from sklearn.metrics.pairwise import haversine_distances

from streamlit_js_eval import get_geolocation



import folium

from streamlit_folium import st_folium





# -----------------------------------

# Load Dataset

# -----------------------------------



data = pd.read_csv("final_bank_recommendation_data.csv")







# ---------------- BranchFinder visual redesign ----------------

st.set_page_config(

    page_title="Bank Branch Finder",

    page_icon="⌖",

    layout="wide",

)



st.markdown("""

<style>

.stApp{background:#f6f8fb;color:#172033}

#MainMenu,footer{visibility:hidden}

.block-container{max-width:1240px;padding:1.5rem 2rem 4rem}



.bf-header{
    margin-top: 12px;

    background:#fff;border:1px solid #e4e8ef;border-radius:14px;

    padding:13px 20px;margin-bottom:25px;

    box-shadow:0 8px 25px rgba(16,35,63,.05)

}

.bf-brand{font-size:21px;font-weight:800;color:#10233f}

.bf-mark{

    display:inline-flex;width:34px;height:34px;border-radius:10px;

    background:#10233f;color:#fff;align-items:center;justify-content:center;

    margin-right:9px

}

.bf-hero{text-align:center;max-width:790px;margin:20px auto 32px}

.bf-eyebrow{

    color:#2563eb;font-size:13px;font-weight:800;

    letter-spacing:.08em;text-transform:uppercase

}
