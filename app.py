from pathlib import Path
import ast

app_code = r'''import streamlit as st
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

    .bf-eyebrow {
        color: var(--blue);
        font-size: 13px;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .bf-hero h1 {
        color: var(--navy);
        font-size: 46px;
        line-height: 1.08;
        letter-spacing: -.035em;
        margin: 12px 0 14px;
    }

    .bf-hero p {
        color: var(--muted);
        font-size: 17px;
        line-height: 1.65;
        margin: 0;
    }

    /* Panels */
    .bf-panel {
        background: var(--white);
        border: 1px solid var(--line);
        border-radius: 18px;
        box-shadow: var(--shadow);
        padding: 28px;
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

    /* Inputs */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-color: var(--line) !important;
        border-radius: 12px !important;
        background: #fff !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #9bb8f8 !important;
        box-shadow: 0 0 0 3px var(--blue-light) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 11px;
        min-height: 42px;
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
        color: #fff;
        border-color: var(--blue);
    }

    .primary-button .stButton > button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        color: #fff;
    }

    /* Choice cards */
    div[role="radiogroup"] {
        gap: 10px;
    }

    div[role="radiogroup"] label {
        border: 1px solid var(--line);
        border-radius: 13px;
        padding: 10px 13px;
        background: #fff;
    }

    /* Results */
    .bf-results-title {
        color: var(--navy);
        font-size: 29px;
        font-weight: 850;
        margin: 4px 0;
    }

    .bf-results-sub {
        color: var(--muted);
        font-size: 13px;
    }

    /* Branch cards */
    .branch-card {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0 12px;
        box-shadow: 0 4px 16px rgba(16,35,63,.035);
    }

    .branch-card.best {
        border-color: #9bd8bd;
    }

    .badge {
        display: inline-block;
        background: var(--green-light);
        color: var(--green);
        padding: 6px 9px;
        border-radius: 999px;
        font-size: 11px;
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

    .score {
        color: var(--navy);
        font-size: 25px;
        font-weight: 900;
    }

    .score-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
    }

    .distance {
        color: var(--blue);
        font-weight: 850;
    }

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

    .score-box {
        background: var(--green-light);
        border-radius: 15px;
        padding: 13px 17px;
        text-align: center;
        color: var(--green);
        width: 130px;
    }

    .score-box strong {
        display: block;
        font-size: 28px;
    }

    .score-box span {
        font-size: 10px;
        font-weight: 800;
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

    .footer-note {
        text-align: center;
        color: var(--muted);
        font-size: 11px;
        margin-top: 32px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .bf-header {
            margin-left: -1rem;
            margin-right: -1rem;
        }

        .bf-hero h1 {
            font-size: 34px;
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
    return pd.read_csv("final_bank_recommendation_data.csv")


data = load_data()


# ============================================================
# VALIDATE REQUIRED COLUMNS
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
    column for column in required_columns
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
    "location_mode": "Use My Current Location",
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

    # Customer-to-branch Haversine distance
    customer_location = np.radians(
        [[latitude, longitude]]
    )

    branch_locations = np.radians(
        df[["lattitude", "longitude"]].values
    )

    distances = (
        haversine_distances(
            customer_location,
            branch_locations,
        )[0]
        * 6371
    )

    df["customer_distance_km"] = distances

    # Bank filter
    if bank_preference == "Public":
        df = df[
            df["bank_group"] == "Public Sector Banks"
        ].copy()

    elif bank_preference == "Private":
        df = df[
            df["bank_group"] == "Private Sector Banks"
        ].copy()

    # Distance filter
    df = df[
        df["customer_distance_km"] <= max_distance
    ].copy()

    if df.empty:
        return df

    # Existing recommendation formula:
    # 70% suitability + 30% proximity
    df["distance_score"] = (
        1 / (1 + df["customer_distance_km"])
    )

    df["recommendation_score"] = (
        df["suitability_score"] * 0.7
        + df["distance_score"] * 30
    )

    # User-selected priority
    if priority == "Closest":
        df = df.sort_values(
            ["customer_distance_km", "suitability_score"],
            ascending=[True, False],
        )

    elif priority == "Public Transport":
        df["transport_distance"] = (
            df["nearest_bus_km"]
            + df["nearest_railway_km"]
            + df["nearest_metro_km"]
        )

        df = df.sort_values(
            ["transport_distance", "recommendation_score"],
            ascending=[True, False],
        )

    elif priority == "Easy Road Access":
        df = df.sort_values(
            ["nearest_major_road_km", "recommendation_score"],
            ascending=[True, False],
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
        reasons.append("Very close to you")
    elif row["customer_distance_km"] <= 5:
        reasons.append("Close to you")

    if row["nearest_metro_km"] <= 2:
        reasons.append("Metro access is nearby")

    if row["nearest_bus_km"] <= 2:
        reasons.append("Good bus accessibility")

    if row["nearest_railway_km"] <= 3:
        reasons.append("Good railway accessibility")

    if row["nearest_major_road_km"] <= 0.2:
        reasons.append("Good road accessibility")

    if row["suitability_score"] >= 80:
        reasons.append("Strong overall suitability")

    if not reasons:
        reasons.append(
            "Suitable based on overall accessibility"
        )

    return reasons[:4]


def build_map(latitude, longitude, recommendations):
    branch_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        control_scale=True,
    )

    # Customer location
    folium.Marker(
        [latitude, longitude],
        popup="Your Location",
        tooltip="Your Location",
        icon=folium.Icon(
            color="red",
            icon="user",
        ),
    ).add_to(branch_map)

    # Recommended branches
    for index, (_, row) in enumerate(
        recommendations.head(10).iterrows()
    ):
        is_best = index == 0

        popup_text = f"""
        <b>{row['bank']}</b><br>
        Branch: {row['branch']}<br>
        Distance: {row['customer_distance_km']:.2f} km<br>
        Suitability: {row['suitability']}<br>
        Suitability Score: {row['suitability_score']:.2f}<br>
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
                color="green" if is_best else "blue",
                icon="star" if is_best else "bank",
            ),
        ).add_to(branch_map)

    return branch_map


def google_maps_url(row):
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={row['lattitude']},{row['longitude']}"
    )


def render_branch_card(row, rank):
    is_best = rank == 1
    reasons = recommendation_reasons(row)

    reason_html = "".join(
        f'<span class="reason">✓ {reason}</span>'
        for reason in reasons[:3]
    )

    card_class = "branch-card best" if is_best else "branch-card"

    st.markdown(
        f"""
        <div class="{card_class}">
            <span class="badge">
                {"★ Best Match" if is_best else "Recommended"}
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
                margin:14px 0 10px;
            ">
                <div>
                    <span class="score">
                        {row["suitability_score"]:.2f}
                    </span>
                    <span class="score-label">
                        Suitability
                    </span>
                </div>

                <div class="distance">
                    {row["customer_distance_km"]:.2f} km
                </div>
            </div>

            <div>
                <span class="metric">
                    Metro <b>{row["nearest_metro_km"]:.2f} km</b>
                </span>

                <span class="metric">
                    Bus <b>{row["nearest_bus_km"]:.2f} km</b>
                </span>

                <span class="metric">
                    Railway <b>{row["nearest_railway_km"]:.2f} km</b>
                </span>

                <span class="metric">
                    Road <b>{row["nearest_major_road_km"]:.2f} km</b>
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
            <span class="bf-mark">⌖</span>
            Bank Branch Finder
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HOME / SEARCH
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="bf-hero">
            <div class="bf-eyebrow">
                Smart branch recommendation
            </div>

            <h1>
                Find a bank branch that's convenient for you.
            </h1>

            <p>
                We consider more than distance — including public
                transport and road accessibility — to help you choose
                a branch that fits your needs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bf-panel">',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    st.markdown(
        '<div class="bf-section-title">Where are you?</div>',
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

    st.session_state.location_mode = location_mode

    if location_mode == "Use My Current Location":

        location_col1, location_col2 = st.columns(
            [3, 1],
            gap="small",
        )

        with location_col1:
            if (
                st.session_state.latitude is not None
                and st.session_state.longitude is not None
            ):
                st.success(
                    "Current location detected and ready."
                )
            else:
                st.markdown(
                    """
                    <div class="bf-hint">
                        Allow location access in your browser,
                        then use the button to detect your location.
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
                "Use My Current Location",
                use_container_width=True,
            ):
                get_current_location()

            st.markdown("</div>", unsafe_allow_html=True)

    else:

        coordinate_col1, coordinate_col2 = st.columns(
            2,
            gap="small",
        )

        with coordinate_col1:
            latitude_input = st.text_input(
                "Latitude",
                placeholder="Example: 13.0827",
            )

        with coordinate_col2:
            longitude_input = st.text_input(
                "Longitude",
                placeholder="Example: 80.2707",
            )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Bank preference
    # --------------------------------------------------------

    st.markdown(
        '<div class="bf-section-title">'
        "Which bank do you prefer?"
        "</div>",
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

    st.session_state.bank_preference = bank_preference

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Priority
    # --------------------------------------------------------

    st.markdown(
        '<div class="bf-section-title">'
        "What matters most?"
        "</div>",
        unsafe_allow_html=True,
    )

    priority_options = [
        "Best Overall",
        "Closest",
        "Public Transport",
        "Easy Road Access",
    ]

    priority_labels = {
        "Best Overall": "⭐ Best Overall",
        "Closest": "🚶 Closest",
        "Public Transport": "🚌 Public Transport",
        "Easy Road Access": "🚗 Easy Road Access",
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
        if priority_labels[item] == priority_display
    )

    st.session_state.priority = selected_priority

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Maximum distance
    # --------------------------------------------------------

    distance_col1, distance_col2 = st.columns(
        [1, 3],
        gap="small",
    )

    with distance_col1:
        max_distance = st.number_input(
            "Maximum distance (km)",
            min_value=0.1,
            max_value=500.0,
            value=float(st.session_state.max_distance),
            step=1.0,
        )

    st.session_state.max_distance = max_distance

    with distance_col2:
        st.markdown(
            """
            <div class="bf-hint" style="padding-top:30px;">
                Only branches within this distance will be
                considered for the recommendation.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="height:8px"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Find button
    # --------------------------------------------------------

    button_col1, button_col2 = st.columns(
        [4, 1],
        gap="small",
    )

    with button_col2:
        st.markdown(
            '<div class="primary-button">',
            unsafe_allow_html=True,
        )

        find_clicked = st.button(
            "Find Best Branch →",
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Process search
    # --------------------------------------------------------

    if find_clicked:

        latitude = None
        longitude = None

        if location_mode == "Use My Current Location":

            latitude = st.session_state.latitude
            longitude = st.session_state.longitude

            if latitude is None or longitude is None:
                latitude, longitude = get_current_location()

            if latitude is None or longitude is None:
                st.error(
                    "Please allow location access first."
                )
                st.stop()

        else:

            try:
                latitude = float(latitude_input)
                longitude = float(longitude_input)

            except (ValueError, TypeError):
                st.error(
                    "Please enter valid latitude and longitude."
                )
                st.stop()

            if not -90 <= latitude <= 90:
                st.error(
                    "Latitude must be between -90 and 90."
                )
                st.stop()

            if not -180 <= longitude <= 180:
                st.error(
                    "Longitude must be between -180 and 180."
                )
                st.stop()

            st.session_state.latitude = latitude
            st.session_state.longitude = longitude

        recommendations = calculate_recommendations(
            data,
            latitude,
            longitude,
            bank_preference,
            selected_priority,
            max_distance,
        )

        st.session_state.recommendations = recommendations
        st.session_state.page = "results"

        st.rerun()


# ============================================================
# RESULTS
# ============================================================

elif st.session_state.page == "results":

    recommendations = st.session_state.recommendations

    if recommendations is None:
        reset_to_home()
        st.rerun()

    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div class="bf-eyebrow">
                Recommendations
            </div>

            <div class="bf-results-title">
                Recommended branches
            </div>

            <div class="bf-results-sub">
                Based on your location, bank preference,
                accessibility, and selected priority.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_col, action_col = st.columns(
        [5, 1],
        gap="small",
    )

    with top_col:
        if recommendations is not None:
            st.write(
                f"**{len(recommendations)} branches found** "
                f"within {st.session_state.max_distance:.1f} km"
            )

    with action_col:
        if st.button(
            "← Change preferences",
            use_container_width=True,
        ):
            st.session_state.page = "home"
            st.rerun()

    if recommendations.empty:

        st.warning(
            "No bank branches were found within the selected "
            "distance and bank preference."
        )

    else:

        left_col, right_col = st.columns(
            [1, 1.45],
            gap="large",
        )

        with left_col:

            display_count = min(
                10,
                len(recommendations),
            )

            for rank, (_, row) in enumerate(
                recommendations.head(display_count).iterrows(),
                start=1,
            ):

                render_branch_card(
                    row,
                    rank,
                )

                action1, action2 = st.columns(
                    2,
                    gap="small",
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
# DETAILS
# ============================================================

elif st.session_state.page == "detail":

    row = st.session_state.selected_branch

    if row is None:
        st.session_state.page = "results"
        st.rerun()

    back_col, empty_col = st.columns(
        [1, 5],
    )

    with back_col:
        if st.button("← Back to results"):
            st.session_state.page = "results"
            st.rerun()

    left_col, right_col = st.columns(
        [1.05, 0.95],
        gap="large",
    )

    with left_col:

        st.markdown(
            f"""
            <div class="bf-eyebrow">
                {row["bank"]}
            </div>

            <h1 style="
                color:#10233f;
                margin:5px 0;
                font-size:30px;
            ">
                {row["branch"]}
            </h1>

            <p style="color:#697386;">
                Recommended branch for your selected location.
            </p>

            <div class="score-box" style="margin:20px 0;">
                <strong>
                    {row["suitability_score"]:.2f}
                </strong>
                <span>SUITABILITY</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if row["suitability_score"] >= 85:
            match_text = "Excellent match"
        elif row["suitability_score"] >= 75:
            match_text = "Strong match"
        else:
            match_text = "Good match"

        st.info(
            f"{match_text}. "
            "This recommendation balances your location "
            "with accessibility around the branch."
        )

        st.markdown("### Why we recommend it")

        for reason in recommendation_reasons(row):
            st.markdown(f"✓ {reason}")

        st.markdown("### Accessibility")

        access_items = [
            (
                "Distance",
                f'{row["customer_distance_km"]:.2f} km',
            ),
            (
                "Metro",
                f'{row["nearest_metro_km"]:.2f} km',
            ),
            (
                "Bus",
                f'{row["nearest_bus_km"]:.2f} km',
            ),
            (
                "Railway",
                f'{row["nearest_railway_km"]:.2f} km',
            ),
            (
                "Major Road",
                f'{row["nearest_major_road_km"]:.2f} km',
            ),
            (
                "Nearby Branches",
                int(row["nearby_branch_count"]),
            ),
        ]

        access_columns = st.columns(2)

        for index, (label, value) in enumerate(
            access_items
        ):
            with access_columns[index % 2]:
                st.markdown(
                    f"""
                    <div class="access-box">
                        <span>{label}</span>
                        <strong>{value}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        action1, action2 = st.columns(2)

        with action1:
            st.link_button(
                "Get Directions →",
                google_maps_url(row),
                use_container_width=True,
            )

        with action2:
            if st.button(
                "← Back to Results",
                use_container_width=True,
            ):
                st.session_state.page = "results"
                st.rerun()

    with right_col:

        single_branch_df = pd.DataFrame([row])

        detail_map = build_map(
            st.session_state.latitude,
            st.session_state.longitude,
            single_branch_df,
        )

        st_folium(
            detail_map,
            width=None,
            height=500,
            returned_objects=[],
        )

        st.caption(
            "The map shows your location and the selected branch."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        Bank Branch Location Optimization using Spatial Analytics
        · Map data © OpenStreetMap contributors
    </div>
    """,
    unsafe_allow_html=True,
)
'''

requirements = """streamlit
pandas
numpy
scikit-learn
folium
streamlit-folium
streamlit-js-eval
"""

# Validate Python before saving.
ast.parse(app_code)

app_path = Path("/mnt/data/app.py")
req_path = Path("/mnt/data/requirements.txt")

app_path.write_text(app_code, encoding="utf-8")
req_path.write_text(requirements, encoding="utf-8")

print(f"Created: {app_path}")
print(f"Created: {req_path}")
print(f"app.py lines: {len(app_code.splitlines())}")
print("Syntax check: PASS")
