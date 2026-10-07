import streamlit as st
import pandas as pd
import numpy as np
import folium
import textwrap

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
# HELPER FOR CUSTOM HTML
# ============================================================

def render_html(html):
    """
    Render indented HTML safely without Streamlit
    interpreting it as a Markdown code block.
    """
    st.markdown(
        textwrap.dedent(html).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# CUSTOM CSS
# ============================================================

render_html(
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
        --background: #f6f8fb;
        --white: #ffffff;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1240px;
        padding: 1.5rem 2rem 4rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .bf-header {
        margin-top: 18px;
        margin-bottom: 32px;

        background: #ffffff;

        border: 1px solid var(--line);
        border-radius: 14px;

        padding: 13px 20px;

        box-shadow:
            0 8px 25px rgba(16, 35, 63, 0.05);
    }

    .bf-brand {
        display: flex;
        align-items: center;

        font-size: 21px;
        font-weight: 800;

        color: var(--navy);
    }

    .bf-mark {
        display: inline-flex;

        width: 34px;
        height: 34px;

        border-radius: 10px;

        background: var(--navy);
        color: #ffffff;

        align-items: center;
        justify-content: center;

        margin-right: 9px;

        font-size: 18px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .bf-hero {
        text-align: center;

        max-width: 790px;

        margin: 20px auto 32px;
    }

    .bf-eyebrow {
        color: var(--blue);

        font-size: 13px;
        font-weight: 800;

        letter-spacing: 0.08em;

        text-transform: uppercase;
    }

    .bf-hero h1 {
        color: var(--navy);

        font-size: 44px;
        line-height: 1.08;

        letter-spacing: -0.035em;

        margin: 10px 0 13px;
    }

    .bf-hero p {
        color: var(--muted);

        font-size: 16px;

        line-height: 1.65;

        margin: 0;
    }


    /* ========================================================
       SEARCH PANEL
       ======================================================== */

    .bf-panel {
        background: #ffffff;

        border: 1px solid var(--line);

        border-radius: 18px;

        padding: 27px;

        box-shadow:
            0 14px 35px rgba(16, 35, 63, 0.07);
    }

    .bf-section-title {
        color: var(--navy);

        font-size: 16px;

        font-weight: 800;

        margin-bottom: 10px;
    }

    .bf-hint {
        color: var(--muted);

        font-size: 12px;

        line-height: 1.5;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {

        border-color: var(--line) !important;

        border-radius: 12px !important;

        background: #ffffff !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        border-radius: 11px;

        min-height: 42px;

        font-weight: 750;

        border: 1px solid var(--line);

        background: #ffffff;

        color: var(--navy);
    }

    .stButton > button:hover {

        border-color: var(--blue);

        color: var(--blue);
    }

    .primary-button .stButton > button {

        background: var(--blue);

        color: #ffffff;

        border-color: var(--blue);
    }

    .primary-button .stButton > button:hover {

        background: #1d4ed8;

        border-color: #1d4ed8;

        color: #ffffff;
    }


    /* ========================================================
       RADIO OPTIONS
       ======================================================== */

    div[role="radiogroup"] {
        gap: 10px;
    }

    div[role="radiogroup"] label {

        border: 1px solid var(--line);

        border-radius: 13px;

        padding: 9px 13px;

        background: #ffffff;
    }


    /* ========================================================
       RESULTS
       ======================================================== */

    .bf-results-title {

        color: var(--navy);

        font-size: 29px;

        font-weight: 850;

        margin: 5px 0;
    }

    .bf-results-sub {

        color: var(--muted);

        font-size: 13px;
    }


    /* ========================================================
       RECOMMENDATION CARD
       ======================================================== */

    .bf-card {

        background: #ffffff;

        border: 1px solid var(--line);

        border-radius: 16px;

        padding: 18px;

        margin: 10px 0 12px;

        box-shadow:
            0 4px 16px rgba(16, 35, 63, 0.035);
    }

    .bf-card.best {

        border-color: #9bd8bd;
    }


    /* ========================================================
       BADGE
       ======================================================== */

    .bf-badge {

        display: inline-block;

        background: var(--green-light);

        color: var(--green);

        padding: 6px 9px;

        border-radius: 999px;

        font-size: 11px;

        font-weight: 850;

        text-transform: uppercase;

        letter-spacing: 0.04em;
    }


    /* ========================================================
       BANK / BRANCH
       ======================================================== */

    .bf-bank {

        font-size: 18px;

        font-weight: 850;

        color: var(--navy);

        margin-top: 9px;
    }

    .bf-branch {

        font-size: 13px;

        color: var(--muted);

        margin-top: 3px;
    }


    /* ========================================================
       SUITABILITY
       ======================================================== */

    .bf-suitability {

        font-size: 25px;

        font-weight: 900;

        color: var(--navy);
    }

    .bf-suitability-label {

        font-size: 11px;

        color: var(--muted);

        font-weight: 700;

        margin-left: 4px;
    }


    /* ========================================================
       DISTANCE
       ======================================================== */

    .bf-distance {

        font-weight: 850;

        color: var(--blue);

        font-size: 15px;
    }


    /* ========================================================
       TRANSPORT CHIPS
       ======================================================== */

    .bf-chip {

        display: inline-block;

        background: #f7f8fa;

        border: 1px solid #edf0f4;

        border-radius: 9px;

        padding: 7px 9px;

        margin: 3px 3px 0 0;

        font-size: 11px;

        color: #4f596b;
    }

    .bf-chip b {

        color: var(--navy);
    }


    /* ========================================================
       WHY RECOMMEND
       ======================================================== */

    .bf-why {

        margin-top: 13px;

        padding-top: 12px;

        border-top: 1px solid var(--line);
    }

    .bf-why-title {

        font-size: 12px;

        font-weight: 850;

        color: var(--navy);

        margin-bottom: 6px;
    }

    .bf-reason {

        display: inline-block;

        font-size: 11px;

        color: #42605a;

        background: #f4faf7;

        border-radius: 7px;

        padding: 5px 7px;

        margin: 2px;
    }


    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .bf-detail-card {

        background: #ffffff;

        border: 1px solid var(--line);

        border-radius: 18px;

        padding: 25px;

        box-shadow:
            0 10px 30px rgba(16, 35, 63, 0.05);
    }

    .bf-detail-bank {

        font-size: 30px;

        font-weight: 850;

        color: var(--navy);

        margin: 5px 0;
    }

    .bf-detail-branch {

        font-size: 15px;

        color: var(--muted);
    }

    .bf-detail-suitability {

        display: inline-block;

        margin-top: 20px;

        background: var(--green-light);

        color: var(--green);

        border-radius: 12px;

        padding: 13px 20px;
    }

    .bf-detail-suitability strong {

        display: block;

        font-size: 28px;
    }

    .bf-detail-suitability span {

        font-size: 10px;

        font-weight: 800;
    }


    /* ========================================================
       ACCESSIBILITY BOX
       ======================================================== */

    .bf-access {

        background: #f8f9fb;

        border-radius: 12px;

        padding: 13px;

        margin-bottom: 10px;
    }

    .bf-access-label {

        display: block;

        color: var(--muted);

        font-size: 11px;
    }

    .bf-access-value {

        display: block;

        color: var(--navy);

        font-weight: 800;

        margin-top: 4px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .bf-footer {

        text-align: center;

        color: var(--muted);

        font-size: 11px;

        margin-top: 30px;
    }

    </style>
    """
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "final_bank_recommendation_data.csv"
    )


data = load_data()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [

    "bank",
    "branch",
    "bank_group",

    "lattitude",
    "longitude",

    "suitability",
    "suitability_score",

    "nearest_bus_km",
    "nearest_railway_km",
    "nearest_metro_km",

    "nearest_major_road_km",

    "nearby_branch_count",
]


missing_columns = [

    column

    for column in required_columns

    if column not in data.columns
]


if missing_columns:

    st.error(
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "latitude" not in st.session_state:
    st.session_state.latitude = None

if "longitude" not in st.session_state:
    st.session_state.longitude = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_branch" not in st.session_state:
    st.session_state.selected_branch = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_recommendation_reasons(row):

    reasons = []


    if row["customer_distance_km"] <= 2:

        reasons.append(
            "Very close to you"
        )


    elif row["customer_distance_km"] <= 5:

        reasons.append(
            "Close to you"
        )


    if row["nearest_bus_km"] <= 2:

        reasons.append(
            "Good bus accessibility"
        )


    if row["nearest_railway_km"] <= 3:

        reasons.append(
            "Good railway accessibility"
        )


    if row["nearest_metro_km"] <= 2:

        reasons.append(
            "Metro access nearby"
        )


    if row["nearest_major_road_km"] <= 0.2:

        reasons.append(
            "Good road accessibility"
        )


    if row["suitability_score"] >= 80:

        reasons.append(
            "Strong overall accessibility"
        )


    if not reasons:

        reasons.append(
            "Suitable overall"
        )


    return reasons[:3]


def calculate_recommendations(
    source_data,
    latitude,
    longitude,
    bank_preference,
    priority,
    max_distance,
):

    df = source_data.copy()


    # --------------------------------------------------------
    # Customer distance
    # --------------------------------------------------------

    customer_location = np.radians(
        [[latitude, longitude]]
    )


    branch_locations = np.radians(
        df[
            [
                "lattitude",
                "longitude"
            ]
        ].values
    )


    distances = (

        haversine_distances(

            customer_location,

            branch_locations

        )[0]

        * 6371

    )


    df["customer_distance_km"] = distances


    # --------------------------------------------------------
    # Bank filter
    # --------------------------------------------------------

    if bank_preference == "Public":

        df = df[
            df["bank_group"]
            == "Public Sector Banks"
        ].copy()


    elif bank_preference == "Private":

        df = df[
            df["bank_group"]
            == "Private Sector Banks"
        ].copy()


    # --------------------------------------------------------
    # Distance filter
    # --------------------------------------------------------

    df = df[
        df["customer_distance_km"]
        <= max_distance
    ].copy()


    if df.empty:

        return df


    # --------------------------------------------------------
    # Existing recommendation formula
    #
    # Suitability = 70%
    # Proximity    = 30%
    # --------------------------------------------------------

    df["distance_score"] = (

        1
        /
        (
            1
            +
            df["customer_distance_km"]
        )

    )


    df["recommendation_score"] = (

        df["suitability_score"] * 0.7

        +

        df["distance_score"] * 30

    )


    # --------------------------------------------------------
    # Priority
    # --------------------------------------------------------

    if priority == "Closest":

        df = df.sort_values(

            [
                "customer_distance_km",
                "suitability_score",
            ],

            ascending=[
                True,
                False,
            ]

        )


    elif priority == "Public Transport":

        df["transport_distance"] = (

            df["nearest_bus_km"]

            +

            df["nearest_railway_km"]

            +

            df["nearest_metro_km"]

        )


        df = df.sort_values(

            [
                "transport_distance",
                "recommendation_score",
            ],

            ascending=[
                True,
                False,
            ]

        )


    elif priority == "Easy Road Access":

        df = df.sort_values(

            [
                "nearest_major_road_km",
                "recommendation_score",
            ],

            ascending=[
                True,
                False,
            ]

        )


    else:

        df = df.sort_values(

            "recommendation_score",

            ascending=False

        )


    return df


def build_map(
    latitude,
    longitude,
    recommendations,
):

    branch_map = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=12,

        control_scale=True,
    )


    # --------------------------------------------------------
    # Customer location
    # --------------------------------------------------------

    folium.Marker(

        [
            latitude,
            longitude
        ],

        popup="Your Location",

        tooltip="Your Location",

        icon=folium.Icon(

            color="red",

            icon="user"

        ),

    ).add_to(branch_map)


    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    for rank, (_, row) in enumerate(

        recommendations.head(10).iterrows(),

        start=1

    ):

        popup_html = f"""
        <div style="font-family:Arial; font-size:13px;">

            <b>{row["bank"]}</b><br>

            Branch: {row["branch"]}<br>

            Bank Type: {row["bank_group"]}<br>

            Distance:
            {row["customer_distance_km"]:.2f} km<br>

            Suitability:
            {row["suitability"]}<br>

            Nearest Bus:
            {row["nearest_bus_km"]:.2f} km<br>

            Nearest Railway:
            {row["nearest_railway_km"]:.2f} km<br>

            Nearest Metro:
            {row["nearest_metro_km"]:.2f} km<br>

            Nearest Major Road:
            {row["nearest_major_road_km"]:.2f} km

        </div>
        """


        folium.Marker(

            [
                row["lattitude"],
                row["longitude"]
            ],

            popup=folium.Popup(

                textwrap.dedent(
                    popup_html
                ),

                max_width=320

            ),

            tooltip=row["bank"],

            icon=folium.Icon(

                color=(
                    "green"
                    if rank == 1
                    else "blue"
                ),

                icon=(
                    "star"
                    if rank == 1
                    else "bank"
                )

            )

        ).add_to(branch_map)


    return branch_map


def google_maps_url(row):

    return (

        "https://www.google.com/maps/dir/?api=1"

        f"&destination="
        f"{row['lattitude']},"
        f"{row['longitude']}"

    )


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="bf-header">

        <div class="bf-brand">

            <span class="bf-mark">
                ⌖
            </span>

            Bank Branch Finder

        </div>

    </div>
    """
)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":


    # ========================================================
    # HERO
    # ========================================================

    render_html(
        """
        <div class="bf-hero">

            <div class="bf-eyebrow">
                Smart Branch Recommendation
            </div>

            <h1>
                Find a bank branch that's convenient for you.
            </h1>

            <p>
                We consider more than distance — including public
                transport and road accessibility — to help you
                choose a branch that fits your needs.
            </p>

        </div>
        """
    )


    # ========================================================
    # SEARCH PANEL
    # ========================================================

    render_html(
        """
        <div class="bf-panel">
        """
    )


    # ========================================================
    # LOCATION
    # ========================================================

    render_html(
        """
        <div class="bf-section-title">
            Where are you?
        </div>
        """
    )


    location_option = st.radio(

        "Location Method",

        [
            "Use My Current Location",
            "Enter Coordinates",
        ],

        horizontal=True,

        label_visibility="collapsed",

    )


    latitude_input = ""
    longitude_input = ""


    if location_option == "Use My Current Location":


        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            if (

                st.session_state.latitude
                is not None

                and

                st.session_state.longitude
                is not None

            ):

                st.success(
                    "Your current location was detected."
                )

            else:

                render_html(
                    """
                    <div class="bf-hint">

                        Allow location access in your browser,
                        then click "Use My Current Location".

                    </div>
                    """
                )


        with col2:

            st.markdown(
                '<div class="primary-button">',
                unsafe_allow_html=True
            )


            location_clicked = st.button(

                "Use My Current Location",

                use_container_width=True,

            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        if location_clicked:

            location = get_geolocation()


            if location:

                if "error" in location:

                    st.error(
                        "Unable to get your current location. "
                        "Please allow location access in "
                        "your browser."
                    )


                elif "coords" in location:

                    st.session_state.latitude = (
                        location["coords"]["latitude"]
                    )

                    st.session_state.longitude = (
                        location["coords"]["longitude"]
                    )

                    st.success(
                        "Current location detected."
                    )

                    st.rerun()


    else:


        col1, col2 = st.columns(
            2
        )


        with col1:

            latitude_input = st.text_input(

                "Latitude",

                placeholder="Example: 13.0827",

            )


        with col2:

            longitude_input = st.text_input(

                "Longitude",

                placeholder="Example: 80.2707",

            )


    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # BANK PREFERENCE
    # ========================================================

    render_html(
        """
        <div class="bf-section-title">
            Which bank do you prefer?
        </div>
        """
    )


    bank_preference = st.radio(

        "Bank Preference",

        [
            "Any",
            "Public",
            "Private",
        ],

        horizontal=True,

        label_visibility="collapsed",

    )


    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # WHAT MATTERS MOST
    # ========================================================

    render_html(
        """
        <div class="bf-section-title">
            What matters most?
        </div>
        """
    )


    priority_display = st.radio(

        "Priority",

        [
            "⭐ Best Overall",
            "🚶 Closest",
            "🚌 Public Transport",
            "🚗 Easy Road Access",
        ],

        horizontal=True,

        label_visibility="collapsed",

    )


    if priority_display == "⭐ Best Overall":

        priority = "Best Overall"


    elif priority_display == "🚶 Closest":

        priority = "Closest"


    elif priority_display == "🚌 Public Transport":

        priority = "Public Transport"


    else:

        priority = "Easy Road Access"


    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DISTANCE
    # ========================================================

    col1, col2 = st.columns(
        [1, 3]
    )


    with col1:

        max_distance = st.number_input(

            "Maximum Distance (km)",

            min_value=0.1,

            max_value=500.0,

            value=10.0,

            step=1.0,

        )


    with col2:

        render_html(
            """
            <div
                class="bf-hint"
                style="padding-top:30px;"
            >

                Only branches within this distance
                will be considered.

            </div>
            """
        )


    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FIND BUTTON
    # ========================================================

    col1, col2 = st.columns(
        [4, 1]
    )


    with col2:

        st.markdown(
            '<div class="primary-button">',
            unsafe_allow_html=True
        )


        find_clicked = st.button(

            "Find Best Branch →",

            use_container_width=True,

        )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # Close visual panel
    render_html(
        """
        </div>
        """
    )


    # ========================================================
    # FIND BEST BRANCH
    # ========================================================

    if find_clicked:


        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        if location_option == "Use My Current Location":


            latitude = (
                st.session_state.latitude
            )

            longitude = (
                st.session_state.longitude
            )


            if latitude is None or longitude is None:

                st.error(
                    "Please use your current location "
                    "button first."
                )

                st.stop()


        else:


            if not latitude_input.strip():

                st.error(
                    "Please enter your latitude."
                )

                st.stop()


            if not longitude_input.strip():

                st.error(
                    "Please enter your longitude."
                )

                st.stop()


            try:

                latitude = float(
                    latitude_input
                )

                longitude = float(
                    longitude_input
                )

            except ValueError:

                st.error(
                    "Please enter valid latitude "
                    "and longitude values."
                )

                st.stop()


            if latitude < -90 or latitude > 90:

                st.error(
                    "Latitude must be between -90 and 90."
                )

                st.stop()


            if longitude < -180 or longitude > 180:

                st.error(
                    "Longitude must be between -180 and 180."
                )

                st.stop()


            st.session_state.latitude = latitude
            st.session_state.longitude = longitude


        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        recommendations = calculate_recommendations(

            data,

            latitude,

            longitude,

            bank_preference,

            priority,

            max_distance,

        )


        st.session_state.recommendations = (
            recommendations
        )


        st.session_state.page = "results"


        st.rerun()


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.page == "results":


    recommendations = (
        st.session_state.recommendations
    )


    if recommendations is None:

        st.session_state.page = "home"

        st.rerun()


    # ========================================================
    # HEADER
    # ========================================================

    render_html(
        """
        <div style="margin-bottom:18px;">

            <div class="bf-eyebrow">
                Recommendations
            </div>

            <div class="bf-results-title">
                Recommended branches
            </div>

            <div class="bf-results-sub">
                Based on your location, preferences,
                accessibility, and selected priority.
            </div>

        </div>
        """
    )


    col1, col2 = st.columns(
        [4, 1]
    )


    with col1:

        st.write(

            f"**{len(recommendations)} branches found** "

            f"within "
            f"{st.session_state.get('max_distance', 10):.1f}"
            f" km"

        )


    with col2:

        if st.button(

            "← Change Search",

            use_container_width=True,

        ):

            st.session_state.page = "home"

            st.rerun()


    # ========================================================
    # NO RESULTS
    # ========================================================

    if recommendations.empty:

        st.warning(

            "No bank branches were found within "
            "the selected distance and bank preference."

        )


    else:


        left_col, right_col = st.columns(

            [1, 1.45],

            gap="large"

        )


        # ====================================================
        # CARDS
        # ====================================================

        with left_col:


            for rank, (_, row) in enumerate(

                recommendations.head(10).iterrows(),

                start=1

            ):


                reasons = get_recommendation_reasons(
                    row
                )


                reason_html = ""


                for reason in reasons:

                    reason_html += f"""

                    <span class="bf-reason">
                        ✓ {reason}
                    </span>

                    """


                if rank == 1:

                    badge = "★ Best Match"

                    card_class = (
                        "bf-card best"
                    )

                else:

                    badge = "Recommended"

                    card_class = "bf-card"


                card_html = f"""

                <div class="{card_class}">

                    <span class="bf-badge">
                        {badge}
                    </span>

                    <div class="bf-bank">
                        {row["bank"]}
                    </div>

                    <div class="bf-branch">
                        {row["branch"]}
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        margin:14px 0 10px;
                    ">

                        <div>

                            <span class="bf-suitability">
                                {row["suitability"]}
                            </span>

                            <span class="bf-suitability-label">
                                Suitability
                            </span>

                        </div>

                        <div class="bf-distance">
                            {row["customer_distance_km"]:.2f}
                            km
                        </div>

                    </div>

                    <div>

                        <span class="bf-chip">
                            Nearest Metro
                            <b>
                                {row["nearest_metro_km"]:.2f}
                                km
                            </b>
                        </span>

                        <span class="bf-chip">
                            Nearest Bus
                            <b>
                                {row["nearest_bus_km"]:.2f}
                                km
                            </b>
                        </span>

                        <span class="bf-chip">
                            Nearest Railway
                            <b>
                                {row["nearest_railway_km"]:.2f}
                                km
                            </b>
                        </span>

                        <span class="bf-chip">
                            Nearest Major Road
                            <b>
                                {row["nearest_major_road_km"]:.2f}
                                km
                            </b>
                        </span>

                    </div>

                    <div class="bf-why">

                        <div class="bf-why-title">
                            Why we recommend it
                        </div>

                        {reason_html}

                    </div>

                </div>

                """


                # Use st.html directly.
                # This prevents raw HTML from appearing.

                st.html(
                    textwrap.dedent(
                        card_html
                    ).strip()
                )


                # ------------------------------------------------
                # Actions
                # ------------------------------------------------

                action1, action2 = st.columns(
                    2
                )


                with action1:

                    if st.button(

                        "View Details",

                        key=f"details_{rank}",

                        use_container_width=True,

                    ):

                        st.session_state.selected_branch = (
                            row.to_dict()
                        )

                        st.session_state.page = "detail"

                        st.rerun()


                with action2:

                    st.link_button(

                        "Directions",

                        google_maps_url(row),

                        use_container_width=True,

                    )


        # ====================================================
        # MAP
        # ====================================================

        with right_col:


            st.subheader(
                "Branch Location Map"
            )


            branch_map = build_map(

                st.session_state.latitude,

                st.session_state.longitude,

                recommendations,

            )


            st_folium(

                branch_map,

                width=None,

                height=650,

                returned_objects=[],

            )


            st.caption(
                "Map data © OpenStreetMap contributors."
            )


# ============================================================
# DETAIL PAGE
# ============================================================

elif st.session_state.page == "detail":


    row = st.session_state.selected_branch


    if row is None:

        st.session_state.page = "results"

        st.rerun()


    # ========================================================
    # BACK
    # ========================================================

    if st.button(
        "← Back to Recommendations"
    ):

        st.session_state.page = "results"

        st.rerun()


    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DETAIL LAYOUT
    # ========================================================

    left_col, right_col = st.columns(

        [1, 1],

        gap="large"

    )


    # ========================================================
    # DETAILS
    # ========================================================

    with left_col:


        render_html(
            f"""
            <div class="bf-detail-card">

                <div class="bf-eyebrow">
                    {row["bank"]}
                </div>

                <div class="bf-detail-bank">
                    {row["branch"]}
                </div>

                <div class="bf-detail-branch">
                    {row.get("address", "")}
                </div>

                <div class="bf-detail-suitability">

                    <strong>
                        {row["suitability"]}
                    </strong>

                    <span>
                        SUITABILITY
                    </span>

                </div>

            </div>
            """
        )


        st.markdown(
            "<div style='height:20px'></div>",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Why
        # ----------------------------------------------------

        render_html(
            """
            <div class="bf-section-title">
                Why we recommend it
            </div>
            """
        )


        for reason in get_recommendation_reasons(
            row
        ):

            st.markdown(
                f"✓ {reason}"
            )


        st.markdown(
            "<div style='height:15px'></div>",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Accessibility
        # ----------------------------------------------------

        render_html(
            """
            <div class="bf-section-title">
                Accessibility
            </div>
            """
        )


        accessibility = [

            (
                "Distance from you",
                f'{row["customer_distance_km"]:.2f} km'
            ),

            (
                "Nearest Bus",
                f'{row["nearest_bus_km"]:.2f} km'
            ),

            (
                "Nearest Railway",
                f'{row["nearest_railway_km"]:.2f} km'
            ),

            (
                "Nearest Metro",
                f'{row["nearest_metro_km"]:.2f} km'
            ),

            (
                "Nearest Major Road",
                f'{row["nearest_major_road_km"]:.2f} km'
            ),

            (
                "Nearby Branches",
                str(int(row["nearby_branch_count"]))
            ),

        ]


        access_col1, access_col2 = st.columns(
            2
        )


        for index, (
            label,
            value
        ) in enumerate(accessibility):


            target_col = (

                access_col1

                if index % 2 == 0

                else access_col2

            )


            with target_col:

                render_html(
                    f"""
                    <div class="bf-access">

                        <span class="bf-access-label">
                            {label}
                        </span>

                        <span class="bf-access-value">
                            {value}
                        </span>

                    </div>
                    """
                )


        # ----------------------------------------------------
        # Directions
        # ----------------------------------------------------

        st.link_button(

            "Get Directions →",

            google_maps_url(row),

            use_container_width=True,

        )


    # ========================================================
    # DETAIL MAP
    # ========================================================

    with right_col:


        st.subheader(
            "Branch Location"
        )


        selected_df = pd.DataFrame(
            [row]
        )


        detail_map = build_map(

            st.session_state.latitude,

            st.session_state.longitude,

            selected_df,

        )


        st_folium(

            detail_map,

            width=None,

            height=550,

            returned_objects=[],

        )


        st.caption(
            "The map shows your location and the selected branch."
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="bf-footer">

        Bank Branch Location Optimization using
        Spatial Analytics

        ·

        Map data © OpenStreetMap contributors.

    </div>
    """
)
