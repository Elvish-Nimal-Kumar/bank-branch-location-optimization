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
        --orange: #c76b00;
        --orange-light: #fff5e8;
        --red: #c53b3b;
        --red-light: #fff0f0;

        --text: #172033;
        --muted: #697386;
        --line: #e4e8ef;
        --bg: #f6f8fb;
        --white: #ffffff;

        --shadow: 0 12px 30px rgba(16,35,63,.07);
    }


    /* ========================================================
       APP
       ======================================================== */

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1180px;
        padding: 0 2rem 4rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .bf-header {
        background: #ffffff;
        border-bottom: 1px solid var(--line);

        margin: 0 -2rem 0;

        padding: 14px 28px;

        display: flex;
        align-items: center;
    }

    .bf-brand {
        display: flex;
        align-items: center;
        gap: 10px;

        color: var(--navy);

        font-size: 20px;
        font-weight: 800;
    }

    .bf-mark {
        width: 32px;
        height: 32px;

        display: inline-flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: var(--navy);
        color: white;

        font-size: 17px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .bf-hero {
        max-width: 720px;

        margin: 62px auto 42px;

        text-align: center;
    }

    .bf-eyebrow {
        color: var(--blue);

        font-size: 12px;
        font-weight: 800;

        letter-spacing: .1em;
        text-transform: uppercase;
    }

    .bf-hero h1 {
        color: var(--navy);

        font-size: 43px;
        line-height: 1.12;

        letter-spacing: -.035em;

        margin: 12px 0 14px;
    }

    .bf-hero p {
        color: var(--muted);

        font-size: 16px;
        line-height: 1.65;

        margin: 0 auto;

        max-width: 650px;
    }


    /* ========================================================
       MAIN PANEL
       ======================================================== */

    .bf-panel {
        background: var(--white);

        border: 1px solid var(--line);
        border-radius: 18px;

        box-shadow: var(--shadow);

        padding: 30px;
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

        border-radius: 11px !important;

        background: #fff !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {

        border-color: #9bb8f8 !important;

        box-shadow:
            0 0 0 3px var(--blue-light) !important;
    }


    /* ========================================================
       RADIO OPTIONS
       ======================================================== */

    div[role="radiogroup"] {
        gap: 8px;
    }

    div[role="radiogroup"] label {
        border: 1px solid var(--line);

        border-radius: 11px;

        padding: 9px 13px;

        background: #fff;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 42px;

        border-radius: 10px;

        font-weight: 750;

        border: 1px solid var(--line);

        background: #fff;

        color: var(--navy);
    }

    .stButton > button:hover {
        border-color: var(--blue);

        color: var(--blue);
    }

    .primary-button .stButton > button {
        background: var(--blue);

        border-color: var(--blue);

        color: white;
    }

    .primary-button .stButton > button:hover {
        background: #1d4ed8;

        border-color: #1d4ed8;

        color: white;
    }


    /* ========================================================
       RESULTS
       ======================================================== */

    .bf-results-title {
        color: var(--navy);

        font-size: 30px;

        font-weight: 850;

        margin: 4px 0;
    }

    .bf-results-sub {
        color: var(--muted);

        font-size: 13px;
    }


    /* ========================================================
       BRANCH CARD
       ======================================================== */

    .branch-card {
        background: #fff;

        border: 1px solid var(--line);

        border-radius: 16px;

        padding: 18px;

        margin-bottom: 10px;

        box-shadow:
            0 4px 15px rgba(16,35,63,.035);
    }

    .branch-card.best {
        border-color: #9bd8bd;
    }

    .recommendation-badge {
        display: inline-block;

        padding: 5px 9px;

        border-radius: 999px;

        background: var(--green-light);

        color: var(--green);

        font-size: 10px;

        font-weight: 850;

        text-transform: uppercase;

        letter-spacing: .04em;
    }

    .bank-name {
        color: var(--navy);

        font-size: 18px;

        font-weight: 850;

        margin-top: 9px;
    }

    .branch-name {
        color: var(--muted);

        font-size: 13px;

        margin-top: 3px;
    }


    /* ========================================================
       SUITABILITY BADGE
       ======================================================== */

    .suitability-high {
        display: inline-block;

        background: var(--green-light);

        color: var(--green);

        padding: 7px 12px;

        border-radius: 8px;

        font-size: 12px;

        font-weight: 850;
    }

    .suitability-medium {
        display: inline-block;

        background: var(--orange-light);

        color: var(--orange);

        padding: 7px 12px;

        border-radius: 8px;

        font-size: 12px;

        font-weight: 850;
    }

    .suitability-low {
        display: inline-block;

        background: var(--red-light);

        color: var(--red);

        padding: 7px 12px;

        border-radius: 8px;

        font-size: 12px;

        font-weight: 850;
    }


    /* ========================================================
       DISTANCE
       ======================================================== */

    .distance {
        color: var(--blue);

        font-size: 17px;

        font-weight: 850;
    }

    .distance-label {
        color: var(--muted);

        font-size: 10px;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    .metric {
        display: inline-block;

        background: #f7f8fa;

        border: 1px solid #edf0f4;

        border-radius: 9px;

        padding: 7px 9px;

        margin: 3px 3px 0 0;

        color: #4f596b;

        font-size: 11px;
    }

    .metric b {
        color: var(--navy);
    }


    /* ========================================================
       REASONS
       ======================================================== */

    .why {
        margin-top: 13px;

        padding-top: 12px;

        border-top: 1px solid var(--line);
    }

    .why-title {
        color: var(--navy);

        font-size: 12px;

        font-weight: 850;

        margin-bottom: 6px;
    }

    .reason {
        display: inline-block;

        color: #42605a;

        background: #f4faf7;

        border-radius: 7px;

        padding: 5px 7px;

        margin: 2px 3px 2px 0;

        font-size: 11px;
    }


    /* ========================================================
       DETAIL PAGE
       ======================================================== */

    .detail-title {
        color: var(--navy);

        font-size: 31px;

        font-weight: 850;

        margin: 5px 0;
    }

    .detail-subtitle {
        color: var(--muted);

        font-size: 14px;
    }

    .match-box {
        background: var(--green-light);

        border-radius: 14px;

        padding: 16px;

        margin: 20px 0;

        color: var(--green);
    }

    .match-box strong {
        display: block;

        font-size: 16px;

        margin-bottom: 4px;
    }

    .access-box {
        background: #f8f9fb;

        border-radius: 12px;

        padding: 13px;

        margin-bottom: 9px;
    }

    .access-box span {
        display: block;

        color: var(--muted);

        font-size: 11px;
    }

    .access-box strong {
        display: block;

        color: var(--navy);

        margin-top: 4px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-note {
        text-align: center;

        color: var(--muted);

        font-size: 11px;

        margin-top: 35px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .bf-header {
            margin-left: -1rem;
            margin-right: -1rem;
        }

        .bf-hero {
            margin-top: 42px;
        }

        .bf-hero h1 {
            font-size: 34px;
        }

        .bf-panel {
            padding: 20px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
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
        "The dataset is missing required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "home",
    "latitude": None,
    "longitude": None,
    "recommendations": None,
    "selected_branch": None,
    "bank_preference": "Any",
    "priority": "Best Overall",
    "max_distance": 10.0,
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_to_home():

    st.session_state.page = "home"

    st.session_state.recommendations = None

    st.session_state.selected_branch = None


def get_current_location():

    location = get_geolocation()

    if not location:

        return None, None

    if "error" in location:

        st.error(
            "Unable to get your current location. "
            "Please allow location access in your browser."
        )

        return None, None

    if "coords" not in location:

        return None, None

    latitude = location["coords"]["latitude"]

    longitude = location["coords"]["longitude"]

    st.session_state.latitude = latitude

    st.session_state.longitude = longitude

    return latitude, longitude


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
    # Customer → Branch distance
    # --------------------------------------------------------

    customer_location = np.radians(
        [[latitude, longitude]]
    )

    branch_locations = np.radians(
        df[
            [
                "lattitude",
                "longitude",
            ]
        ].values
    )

    distances = (
        haversine_distances(
            customer_location,
            branch_locations,
        )[0]
        * 6371
    )

    df["customer_distance_km"] = distances


    # --------------------------------------------------------
    # Bank preference
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
    # Recommendation score
    #
    # Existing project logic:
    #
    # 70% suitability
    # 30% proximity
    # --------------------------------------------------------

    df["distance_score"] = (
        1
        / (
            1
            + df["customer_distance_km"]
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
            ],
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
            ],
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
            ],
        )


    else:

        df = df.sort_values(
            "recommendation_score",
            ascending=False,
        )


    return df


def recommendation_reasons(row):

    reasons = []


    if row["customer_distance_km"] <= 2:

        reasons.append(
            "Very close to you"
        )

    elif row["customer_distance_km"] <= 5:

        reasons.append(
            "Close to you"
        )


    if row["nearest_metro_km"] <= 2:

        reasons.append(
            "Metro access is nearby"
        )


    if row["nearest_bus_km"] <= 2:

        reasons.append(
            "Good bus accessibility"
        )


    if row["nearest_railway_km"] <= 3:

        reasons.append(
            "Good railway accessibility"
        )


    if row["nearest_major_road_km"] <= 0.2:

        reasons.append(
            "Good road accessibility"
        )


    if row["suitability_score"] >= 80:

        reasons.append(
            "Strong overall suitability"
        )


    if not reasons:

        reasons.append(
            "Suitable based on overall accessibility"
        )


    return reasons[:4]


def get_suitability_class(value):

    value = str(value).strip().lower()


    if value == "high":

        return (
            "suitability-high",
            "High",
        )


    if value == "medium":

        return (
            "suitability-medium",
            "Medium",
        )


    return (
        "suitability-low",
        "Low",
    )


def build_map(
    latitude,
    longitude,
    recommendations,
):

    branch_map = folium.Map(
        location=[
            latitude,
            longitude,
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
            longitude,
        ],

        popup="Your Location",

        tooltip="Your Location",

        icon=folium.Icon(
            color="red",
            icon="user",
        ),
    ).add_to(branch_map)


    # --------------------------------------------------------
    # Recommended branches
    # --------------------------------------------------------

    for index, (_, row) in enumerate(
        recommendations
        .head(10)
        .iterrows()
    ):

        is_best = index == 0


        popup_text = f"""
        <b>{row['bank']}</b><br>
        Branch: {row['branch']}<br>
        Distance: {row['customer_distance_km']:.2f} km<br>
        Suitability: {row['suitability']}<br>
        Bus: {row['nearest_bus_km']:.2f} km<br>
        Railway: {row['nearest_railway_km']:.2f} km<br>
        Metro: {row['nearest_metro_km']:.2f} km<br>
        Major Road: {row['nearest_major_road_km']:.2f} km
        """


        folium.Marker(
            [
                row["lattitude"],
                row["longitude"],
            ],

            popup=folium.Popup(
                popup_text,
                max_width=320,
            ),

            tooltip=row["bank"],

            icon=folium.Icon(
                color=(
                    "green"
                    if is_best
                    else "blue"
                ),

                icon=(
                    "star"
                    if is_best
                    else "bank"
                ),
            ),
        ).add_to(branch_map)


    return branch_map


def google_maps_url(row):

    return (
        "https://www.google.com/maps/dir/"
        "?api=1"
        f"&destination="
        f"{row['lattitude']},"
        f"{row['longitude']}"
    )


def render_branch_card(
    row,
    rank,
):

    is_best = rank == 1

    reasons = recommendation_reasons(
        row
    )

    suitability_class, suitability_text = (
        get_suitability_class(
            row["suitability"]
        )
    )


    reason_html = "".join(
        f"""
        <span class="reason">
            ✓ {reason}
        </span>
        """
        for reason in reasons[:3]
    )


    card_class = (
        "branch-card best"
        if is_best
        else "branch-card"
    )


    st.markdown(
        f"""
        <div class="{card_class}">

            <span class="recommendation-badge">

                {
                    "★ Best Match"
                    if is_best
                    else "Recommended"
                }

            </span>


            <div class="bank-name">

                {row["bank"]}

            </div>


            <div class="branch-name">

                {row["branch"]}

            </div>


            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin:15px 0 12px;
            ">

                <div>

                    <span class="{suitability_class}">

                        {suitability_text}

                    </span>

                </div>


                <div style="text-align:right;">

                    <div class="distance">

                        {
                            row["customer_distance_km"]
                            :.2f
                        }
                        km

                    </div>

                    <div class="distance-label">

                        from your location

                    </div>

                </div>

            </div>


            <div>

                <span class="metric">

                    Nearest Bus

                    <b>
                        {
                            row["nearest_bus_km"]
                            :.2f
                        } km
                    </b>

                </span>


                <span class="metric">

                    Nearest Railway

                    <b>
                        {
                            row["nearest_railway_km"]
                            :.2f
                        } km
                    </b>

                </span>


                <span class="metric">

                    Nearest Metro

                    <b>
                        {
                            row["nearest_metro_km"]
                            :.2f
                        } km
                    </b>

                </span>


                <span class="metric">

                    Nearest Major Road

                    <b>
                        {
                            row["nearest_major_road_km"]
                            :.2f
                        } km
                    </b>

                </span>

            </div>


            <div class="why">

                <div class="why-title">

                    Why we recommend it

                </div>

                {reason_html}

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="bf-header">

        <div class="bf-brand">

            <span class="bf-mark">
                ⌖
            </span>

            Bank Branch Finder

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="bf-hero">

            <div class="bf-eyebrow">

                Smart Branch Recommendation

            </div>


            <h1>

                Find a bank branch that's convenient
                for you.

            </h1>


            <p>

                We consider more than distance —
                including public transport and road
                accessibility — to help you choose
                a branch that fits your needs.

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # MAIN SEARCH PANEL
    # --------------------------------------------------------

    st.markdown(
        '<div class="bf-panel">',
        unsafe_allow_html=True,
    )


    # ========================================================
    # LOCATION
    # ========================================================

    st.markdown(
        """
        <div class="bf-section-title">
            Where are you?
        </div>
        """,
        unsafe_allow_html=True,
    )


    location_mode = st.radio(
        "Location method",

        [
            "Use My Current Location",
            "Enter Coordinates",
        ],

        horizontal=True,

        label_visibility="collapsed",
    )


    # --------------------------------------------------------
    # CURRENT LOCATION
    # --------------------------------------------------------

    if (
        location_mode
        == "Use My Current Location"
    ):

        location_col1, location_col2 = (
            st.columns(
                [3, 1]
            )
        )


        with location_col1:

            if (
                st.session_state.latitude
                is not None
                and
                st.session_state.longitude
                is not None
            ):

                st.success(
                    "Current location detected."
                )

            else:

                st.markdown(
                    """
                    <div class="bf-hint"
                         style="padding-top:10px;">

                        Allow location access in your
                        browser to automatically use
                        your current position.

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        with location_col2:

            st.markdown(
                '<div class="primary-button">',
                unsafe_allow_html=True,
            )


            if st.button(
                "Detect Location",
                use_container_width=True,
            ):

                get_current_location()


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


    # --------------------------------------------------------
    # ENTER COORDINATES
    # --------------------------------------------------------

    else:

        latitude_input, longitude_input = (
            st.columns(2)
        )


        with latitude_input:

            latitude_value = st.text_input(
                "Latitude",
                placeholder="Example: 13.0827",
            )


        with longitude_input:

            longitude_value = st.text_input(
                "Longitude",
                placeholder="Example: 80.2707",
            )


    st.markdown(
        '<div style="height:22px"></div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # BANK PREFERENCE
    # ========================================================

    st.markdown(
        """
        <div class="bf-section-title">

            Which bank do you prefer?

        </div>
        """,
        unsafe_allow_html=True,
    )


    bank_preference = st.radio(
        "Bank preference",

        [
            "Any",
            "Public",
            "Private",
        ],

        horizontal=True,

        label_visibility="collapsed",
    )


    st.markdown(
        '<div style="height:22px"></div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # PRIORITY
    # ========================================================

    st.markdown(
        """
        <div class="bf-section-title">

            What matters most?

        </div>
        """,
        unsafe_allow_html=True,
    )


    priority_options = [
        "Best Overall",
        "Closest",
        "Public Transport",
        "Easy Road Access",
    ]


    priority_labels = {

        "Best Overall":
            "⭐ Best Overall",

        "Closest":
            "🚶 Closest",

        "Public Transport":
            "🚌 Public Transport",

        "Easy Road Access":
            "🚗 Easy Road Access",
    }


    priority_display = st.radio(
        "Priority",

        [
            priority_labels[item]
            for item in priority_options
        ],

        horizontal=True,

        label_visibility="collapsed",
    )


    selected_priority = next(
        item
        for item in priority_options
        if priority_labels[item]
        == priority_display
    )


    # ========================================================
    # DISTANCE
    # ========================================================

    st.markdown(
        '<div style="height:22px"></div>',
        unsafe_allow_html=True,
    )


    distance_col1, distance_col2 = (
        st.columns(
            [1, 3]
        )
    )


    with distance_col1:

        max_distance = st.number_input(
            "Maximum distance (km)",

            min_value=0.5,

            max_value=500.0,

            value=10.0,

            step=0.5,
        )


    with distance_col2:

        st.markdown(
            """
            <div class="bf-hint"
                 style="padding-top:30px;">

                Only branches within this distance
                will be considered.

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # FIND BUTTON
    # ========================================================

    st.markdown(
        '<div style="height:15px"></div>',
        unsafe_allow_html=True,
    )


    find_col1, find_col2 = (
        st.columns(
            [3, 1]
        )
    )


    with find_col2:

        st.markdown(
            '<div class="primary-button">',
            unsafe_allow_html=True,
        )


        find_clicked = st.button(
            "Find Best Branch →",
            use_container_width=True,
        )


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # PROCESS SEARCH
    # ========================================================

    if find_clicked:


        latitude = None
        longitude = None


        # ----------------------------------------------------
        # CURRENT LOCATION
        # ----------------------------------------------------

        if (
            location_mode
            == "Use My Current Location"
        ):

            latitude = (
                st.session_state.latitude
            )

            longitude = (
                st.session_state.longitude
            )


            if (
                latitude is None
                or
                longitude is None
            ):

                latitude, longitude = (
                    get_current_location()
                )


            if (
                latitude is None
                or
                longitude is None
            ):

                st.error(
                    "Please allow location access "
                    "before finding a branch."
                )

                st.stop()


        # ----------------------------------------------------
        # ENTERED COORDINATES
        # ----------------------------------------------------

        else:

            try:

                latitude = float(
                    latitude_value
                )

                longitude = float(
                    longitude_value
                )

            except (
                ValueError,
                TypeError,
            ):

                st.error(
                    "Please enter valid latitude "
                    "and longitude values."
                )

                st.stop()


            if not -90 <= latitude <= 90:

                st.error(
                    "Latitude must be between "
                    "-90 and 90."
                )

                st.stop()


            if not -180 <= longitude <= 180:

                st.error(
                    "Longitude must be between "
                    "-180 and 180."
                )

                st.stop()


            st.session_state.latitude = (
                latitude
            )

            st.session_state.longitude = (
                longitude
            )


        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        recommendations = (
            calculate_recommendations(
                data,
                latitude,
                longitude,
                bank_preference,
                selected_priority,
                max_distance,
            )
        )


        st.session_state.recommendations = (
            recommendations
        )

        st.session_state.bank_preference = (
            bank_preference
        )

        st.session_state.priority = (
            selected_priority
        )

        st.session_state.max_distance = (
            max_distance
        )

        st.session_state.page = (
            "results"
        )


        st.rerun()


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.page == "results":


    recommendations = (
        st.session_state.recommendations
    )


    if recommendations is None:

        reset_to_home()

        st.rerun()


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="margin-top:38px;">

            <div class="bf-eyebrow">

                Recommendations

            </div>


            <div class="bf-results-title">

                Recommended branches

            </div>


            <div class="bf-results-sub">

                Based on your location, bank preference,
                accessibility and selected priority.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # TOP ACTIONS
    # --------------------------------------------------------

    top_col1, top_col2 = (
        st.columns(
            [4, 1]
        )
    )


    with top_col1:

        if not recommendations.empty:

            st.write(
                f"**{len(recommendations)} "
                f"branches found** within "
                f"{st.session_state.max_distance:.1f} km"
            )


    with top_col2:

        if st.button(
            "← Change Search",
            use_container_width=True,
        ):

            st.session_state.page = (
                "home"
            )

            st.rerun()


    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if recommendations.empty:

        st.warning(
            "No bank branches were found "
            "within your selected distance "
            "and bank preference."
        )


    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    else:

        left_col, right_col = (
            st.columns(
                [1, 1.45],
                gap="large",
            )
        )


        # ====================================================
        # BRANCH LIST
        # ====================================================

        with left_col:

            display_count = min(
                10,
                len(recommendations),
            )


            for rank, (_, row) in enumerate(
                recommendations
                .head(display_count)
                .iterrows(),

                start=1,
            ):


                render_branch_card(
                    row,
                    rank,
                )


                action_col1, action_col2 = (
                    st.columns(2)
                )


                with action_col1:

                    if st.button(
                        "View Details",
                        key=f"details_{rank}",
                        use_container_width=True,
                    ):

                        st.session_state.selected_branch = (
                            row.to_dict()
                        )

                        st.session_state.page = (
                            "detail"
                        )

                        st.rerun()


                with action_col2:

                    st.link_button(
                        "Directions",
                        google_maps_url(row),
                        use_container_width=True,
                    )


        # ====================================================
        # MAP
        # ====================================================

        with right_col:

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


    row = (
        st.session_state.selected_branch
    )


    if row is None:

        st.session_state.page = (
            "results"
        )

        st.rerun()


    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button(
        "← Back to Results"
    ):

        st.session_state.page = (
            "results"
        )

        st.rerun()


    st.markdown(
        '<div style="height:15px"></div>',
        unsafe_allow_html=True,
    )


    left_col, right_col = (
        st.columns(
            [1.05, 0.95],
            gap="large",
        )
    )


    # ========================================================
    # DETAILS LEFT
    # ========================================================

    with left_col:


        st.markdown(
            f"""
            <div class="bf-eyebrow">

                {row["bank"]}

            </div>


            <div class="detail-title">

                {row["branch"]}

            </div>


            <div class="detail-subtitle">

                Recommended branch for your
                selected location.

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # SUITABILITY
        # ----------------------------------------------------

        suitability_class, suitability_text = (
            get_suitability_class(
                row["suitability"]
            )
        )


        st.markdown(
            f"""
            <div style="margin-top:20px;">

                <span class="{suitability_class}">

                    {suitability_text} Suitability

                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # MATCH EXPLANATION
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="match-box">

                <strong>
                    Why this branch?
                </strong>

                This recommendation balances
                branch suitability with your distance
                and accessibility preferences.

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # REASONS
        # ----------------------------------------------------

        st.markdown(
            "### Why we recommend it"
        )


        for reason in recommendation_reasons(
            row
        ):

            st.markdown(
                f"✓ {reason}"
            )


        # ----------------------------------------------------
        # ACCESSIBILITY
        # ----------------------------------------------------

        st.markdown(
            "### Accessibility"
        )


        access_items = [

            (
                "Distance",
                f"""
                {
                    row["customer_distance_km"]
                    :.2f
                } km
                """,
            ),

            (
                "Nearest Bus",
                f"""
                {
                    row["nearest_bus_km"]
                    :.2f
                } km
                """,
            ),

            (
                "Nearest Railway",
                f"""
                {
                    row["nearest_railway_km"]
                    :.2f
                } km
                """,
            ),

            (
                "Nearest Metro",
                f"""
                {
                    row["nearest_metro_km"]
                    :.2f
                } km
                """,
            ),

            (
                "Nearest Major Road",
                f"""
                {
                    row["nearest_major_road_km"]
                    :.2f
                } km
                """,
            ),

            (
                "Nearby Branches",
                int(
                    row["nearby_branch_count"]
                ),
            ),
        ]


        access_columns = (
            st.columns(2)
        )


        for index, (
            label,
            value,
        ) in enumerate(
            access_items
        ):

            with access_columns[
                index % 2
            ]:

                st.markdown(
                    f"""
                    <div class="access-box">

                        <span>
                            {label}
                        </span>

                        <strong>
                            {value}
                        </strong>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        # ----------------------------------------------------
        # DIRECTIONS
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

        single_branch_df = (
            pd.DataFrame([row])
        )


        detail_map = build_map(
            st.session_state.latitude,
            st.session_state.longitude,
            single_branch_df,
        )


        st_folium(
            detail_map,

            width=None,

            height=520,

            returned_objects=[],
        )


        st.caption(
            "The map shows your location and "
            "the selected branch."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">

        Bank Branch Location Optimization using
        Spatial Analytics

        ·

        Map data © OpenStreetMap contributors

    </div>
    """,
    unsafe_allow_html=True,
)
