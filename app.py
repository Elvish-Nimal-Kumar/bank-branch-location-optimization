from pathlib import Path

app = r'''import streamlit as st
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import haversine_distances
from streamlit_js_eval import get_geolocation

import folium
from streamlit_folium import st_folium


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="BranchFinder — Smart Bank Branch Recommendation",
    page_icon="⌖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Custom styling — inspired by the supplied BranchFinder HTML
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --navy: #10233f;
        --blue: #2563eb;
        --blue2: #eaf2ff;
        --green: #16835b;
        --green2: #eaf8f2;
        --text: #172033;
        --muted: #697386;
        --line: #e4e8ef;
        --bg: #f6f8fb;
        --white: #ffffff;
        --shadow: 0 14px 35px rgba(16,35,63,.09);
    }

    .stApp {
        background: #f6f8fb;
        color: #172033;
    }

    [data-testid="stHeader"] {
        background: rgba(246,248,251,0.95);
    }

    .block-container {
        max-width: 1240px;
        padding: 1.5rem 2rem 4rem;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* Header */
    .bf-header {
        background: #ffffff;
        border-bottom: 1px solid #e4e8ef;
        padding: 12px 22px;
        margin: -1.5rem -2rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .bf-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #10233f;
        font-size: 21px;
        font-weight: 800;
    }

    .bf-mark {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #10233f;
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
    }

    /* Hero */
    .bf-hero {
        max-width: 790px;
        margin: 25px auto 30px;
        text-align: center;
    }

    .bf-eyebrow {
        color: #2563eb;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .bf-hero h1 {
        color: #10233f;
        font-size: 44px;
        line-height: 1.08;
        letter-spacing: -.035em;
        margin: 10px 0 12px;
    }

    .bf-hero p {
        color: #697386;
        font-size: 16px;
        line-height: 1.65;
        margin: 0;
    }

    /* Panels */
    .bf-panel {
        background: #ffffff;
        border: 1px solid #e4e8ef;
        border-radius: 18px;
        box-shadow: 0 14px 35px rgba(16,35,63,.07);
        padding: 26px;
    }

    .bf-section-title {
        color: #10233f;
        font-size: 16px;
        font-weight: 800;
        margin: 0 0 10px;
    }

    .bf-hint {
        color: #697386;
        font-size: 12px;
        margin-top: 5px;
    }

    /* Streamlit input styling */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-color: #e4e8ef !important;
        border-radius: 12px !important;
        background: #ffffff !important;
    }

    input {
        color: #172033 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 11px;
        min-height: 42px;
        font-weight: 750;
        border: 1px solid #e4e8ef;
    }

    .primary-button .stButton > button {
        background: #2563eb;
        color: white;
        border-color: #2563eb;
    }

    .primary-button .stButton > button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        color: white;
    }

    /* Radio */
    div[role="radiogroup"] {
        gap: 10px;
    }

    /* Cards */
    .branch-card {
        background: #ffffff;
        border: 1px solid #e4e8ef;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(16,35,63,.035);
    }

    .branch-card.best {
        border-color: #9bd8bd;
    }

    .bf-badge {
        display: inline-block;
        background: #eaf8f2;
        color: #16835b;
        padding: 6px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: .04em;
    }

    .bf-bank {
        color: #10233f;
        font-size: 18px;
        font-weight: 850;
        margin-top: 9px;
    }

    .bf-branch {
        color: #697386;
        font-size: 13px;
        margin-top: 3px;
    }

    .bf-score {
        color: #10233f;
        font-size: 25px;
        font-weight: 900;
    }

    .bf-score-label {
        color: #697386;
        font-size: 11px;
        font-weight: 700;
    }

    .bf-distance {
        color: #2563eb;
        font-weight: 850;
        font-size: 15px;
    }

    .metric-chip {
        display: inline-block;
        background: #f7f8fa;
        border: 1px solid #edf0f4;
        border-radius: 9px;
        padding: 7px 9px;
        margin: 3px 3px 0 0;
        color: #4f596b;
        font-size: 11px;
    }

    .metric-chip b {
        color: #10233f;
    }

    .why-box {
        margin-top: 13px;
        padding-top: 12px;
        border-top: 1px solid #e4e8ef;
    }

    .why-title {
        color: #10233f;
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

    /* Results heading */
    .results-title {
        color: #10233f;
        font-size: 29px;
        font-weight: 850;
        margin: 0;
    }

    .results-sub {
        color: #697386;
        margin-top: 5px;
        font-size: 13px;
    }

    /* Score detail */
    .score-box {
        background: #eaf8f2;
        border-radius: 15px;
        padding: 13px 17px;
        text-align: center;
        color: #16835b;
    }

    .score-box strong {
        display: block;
        font-size: 27px;
    }

    .score-box span {
        font-size: 10px;
        font-weight: 800;
    }

    .access-box {
        background: #f8f9fb;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }

    .access-label {
        display: block;
        color: #697386;
        font-size: 11px;
    }

    .access-value {
        display: block;
        color: #10233f;
        font-weight: 800;
        margin-top: 4px;
    }

    /* Mobile */
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


# =========================================================
# Load dataset
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("final_bank_recommendation_data.csv")


data = load_data()


# =========================================================
# Session state
# =========================================================

defaults = {
    "current_latitude": None,
    "current_longitude": None,
    "recommendations": None,
    "selected_branch_index": None,
    "page": "home",
    "location_mode": "Current Location",
    "bank_preference": "Any bank",
    "priority": "Best Overall",
    "max_distance": 10.0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# Helper functions
# =========================================================

def reset_app():
    st.session_state.recommendations = None
    st.session_state.selected_branch_index = None
    st.session_state.page = "home"


def get_current_coordinates():
    location = get_geolocation()

    if location:
        if "error" in location:
            st.error(
                "Unable to get your location. "
                "Please allow location access in your browser."
            )
            return None, None

        if "coords" in location:
            lat = location["coords"]["latitude"]
            lon = location["coords"]["longitude"]

            st.session_state.current_latitude = lat
            st.session_state.current_longitude = lon

            return lat, lon

    return None, None


def calculate_recommendations(
    source_data,
    latitude,
    longitude,
    bank_preference,
    max_distance,
):
    df = source_data.copy()

    customer_location = np.radians([[latitude, longitude]])

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

    if bank_preference == "Public Sector Banks":
        df = df[
            df["bank_group"] == "Public Sector Banks"
        ].copy()

    elif bank_preference == "Private Sector Banks":
        df = df[
            df["bank_group"] == "Private Sector Banks"
        ].copy()

    df = df[
        df["customer_distance_km"] <= max_distance
    ].copy()

    df["distance_score"] = (
        1 / (1 + df["customer_distance_km"])
    )

    df["recommendation_score"] = (
        df["suitability_score"] * 0.7
        + df["distance_score"] * 30
    )

    # Keep the original recommendation logic as the
    # default ranking.
    if st.session_state.priority == "Closest":
        df = df.sort_values(
            ["customer_distance_km", "suitability_score"],
            ascending=[True, False],
        )

    elif st.session_state.priority == "Public Transport":
        df["transport_score"] = (
            df["nearest_bus_km"]
            + df["nearest_railway_km"]
            + df["nearest_metro_km"]
        )
        df = df.sort_values(
            ["transport_score", "recommendation_score"],
            ascending=[True, False],
        )

    elif st.session_state.priority == "Easy Road Access":
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


def format_bank_filter():
    if st.session_state.bank_preference == "Any bank":
        return "Any"

    return st.session_state.bank_preference


def render_branch_card(row, rank):
    best = rank == 1

    badge = "★ Best match" if best else "Recommended"

    score = float(row["suitability_score"])
    distance = float(row["customer_distance_km"])

    reasons = []

    if distance <= 2:
        reasons.append("Very close to you")
    elif distance <= 5:
        reasons.append("Close to you")

    if row["nearest_bus_km"] <= 2:
        reasons.append("Good bus access")

    if row["nearest_railway_km"] <= 3:
        reasons.append("Good railway access")

    if row["nearest_metro_km"] <= 2:
        reasons.append("Metro access nearby")

    if row["nearest_major_road_km"] <= 0.2:
        reasons.append("Good road accessibility")

    if score >= 80:
        reasons.append("Strong overall accessibility")

    if not reasons:
        reasons.append("Suitable based on overall accessibility")

    reason_html = "".join(
        f'<span class="reason">✓ {r}</span>'
        for r in reasons[:3]
    )

    card_class = "branch-card best" if best else "branch-card"

    st.markdown(
        f"""
        <div class="{card_class}">
            <span class="bf-badge">{badge}</span>

            <div class="bf-bank">{row["bank"]}</div>
            <div class="bf-branch">{row["branch"]}</div>

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin:14px 0 10px;
            ">
                <div>
                    <span class="bf-score">{score:.2f}</span>
                    <span class="bf-score-label"> Suitability</span>
                </div>
                <div class="bf-distance">{distance:.2f} km</div>
            </div>

            <div>
                <span class="metric-chip">
                    Metro <b>{row["nearest_metro_km"]:.2f} km</b>
                </span>
                <span class="metric-chip">
                    Bus <b>{row["nearest_bus_km"]:.2f} km</b>
                </span>
                <span class="metric-chip">
                    Railway <b>{row["nearest_railway_km"]:.2f} km</b>
                </span>
                <span class="metric-chip">
                    Road <b>{row["nearest_major_road_km"]:.2f} km</b>
                </span>
            </div>

            <div class="why-box">
                <div class="why-title">Why we recommend it</div>
                {reason_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_map(latitude, longitude, recommendations, focus_index=None):
    branch_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        control_scale=True,
    )

    folium.Marker(
        [latitude, longitude],
        popup="Your Location",
        tooltip="Your Location",
        icon=folium.Icon(
            color="red",
            icon="user",
        ),
    ).add_to(branch_map)

    for idx, (_, row) in enumerate(
        recommendations.head(10).iterrows()
    ):
        is_best = idx == 0

        popup_text = f"""
        <b>{row['bank']}</b><br>
        Branch: {row['branch']}<br>
        Bank Type: {row['bank_group']}<br>
        Distance: {row['customer_distance_km']:.2f} km<br>
        Suitability: {row['suitability']}<br>
        Suitability Score: {row['suitability_score']:.2f}<br>
        Nearest Bus: {row['nearest_bus_km']:.2f} km<br>
        Nearest Railway: {row['nearest_railway_km']:.2f} km<br>
        Nearest Metro: {row['nearest_metro_km']:.2f} km<br>
        Nearest Major Road: {row['nearest_major_road_km']:.2f} km
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


# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="bf-header">
        <div class="bf-brand">
            <span class="bf-mark">⌖</span>
            BranchFinder
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HOME / SEARCH SCREEN
# =========================================================

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

    st.markdown(
        '<div class="bf-section-title">Where are you?</div>',
        unsafe_allow_html=True,
    )

    location_mode = st.radio(
        "Location method",
        [
            "Current Location",
            "Enter Coordinates",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="location_mode_radio",
    )

    if location_mode == "Current Location":

        location_col1, location_col2 = st.columns(
            [3, 1],
            gap="small",
        )

        with location_col1:
            if (
                st.session_state.current_latitude
                is not None
            ):
                st.success(
                    "Location detected and ready."
                )
            else:
                st.markdown(
                    '<div class="bf-hint">'
                    'Click "Use My Current Location" and allow '
                    'location access in your browser.'
                    '</div>',
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
                get_current_coordinates()

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
        '<div style="height:20px"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bf-section-title">'
        'Which bank do you prefer?'
        '</div>',
        unsafe_allow_html=True,
    )

    bank_options = [
        "Any bank",
        "Public Sector Banks",
        "Private Sector Banks",
    ]

    st.session_state.bank_preference = st.radio(
        "Bank preference",
        bank_options,
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bf-section-title">'
        'What matters most?'
        '</div>',
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
            priority_labels[x]
            for x in priority_options
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.session_state.priority = next(
        x for x in priority_options
        if priority_labels[x] == priority_display
    )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    distance_col1, distance_col2 = st.columns(
        [1, 3],
        gap="small",
    )

    with distance_col1:
        max_distance_input = st.number_input(
            "Maximum distance (km)",
            min_value=0.1,
            max_value=500.0,
            value=float(st.session_state.max_distance),
            step=1.0,
        )

    st.session_state.max_distance = max_distance_input

    with distance_col2:
        st.markdown(
            '<div class="bf-hint" style="padding-top:30px;">'
            'Only branches within this distance will be considered.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True,
    )

    button_col1, button_col2 = st.columns(
        [3, 1],
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

    # Process search
    if find_clicked:

        latitude = None
        longitude = None

        if location_mode == "Current Location":

            latitude = st.session_state.current_latitude
            longitude = st.session_state.current_longitude

            if latitude is None or longitude is None:
                latitude, longitude = get_current_coordinates()

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
                    "Please enter valid latitude and longitude values."
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

        recommendations = calculate_recommendations(
            data,
            latitude,
            longitude,
            st.session_state.bank_preference,
            st.session_state.max_distance,
        )

        st.session_state.recommendations = recommendations
        st.session_state.current_latitude = latitude
        st.session_state.current_longitude = longitude
        st.session_state.page = "results"

        st.rerun()


# =========================================================
# RESULTS SCREEN
# =========================================================

elif st.session_state.page == "results":

    recommendations = st.session_state.recommendations

    if recommendations is None:
        st.session_state.page = "home"
        st.rerun()

    top_count = len(recommendations)

    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div class="bf-eyebrow">Recommendations</div>
            <div class="results-title">
                Recommended branches
            </div>
            <div class="results-sub">
                Based on your location, preferences, accessibility,
                and branch suitability.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_col1, action_col2 = st.columns(
        [5, 1],
    )

    with action_col2:
        if st.button(
            "← Change preferences",
            use_container_width=True,
        ):
            st.session_state.page = "home"
            st.rerun()

    if top_count == 0:

        st.warning(
            "No bank branches found within the selected distance."
        )

    else:

        st.write(
            f"**{top_count} branches found** within "
            f"{st.session_state.max_distance:.1f} km"
        )

        left_col, right_col = st.columns(
            [1, 1.45],
            gap="large",
        )

        with left_col:

            for rank, (_, row) in enumerate(
                recommendations.head(10).iterrows(),
                start=1,
            ):

                render_branch_card(row, rank)

                if st.button(
                    "View Details",
                    key=f"details_{rank}",
                    use_container_width=True,
                ):
                    st.session_state.selected_branch_index = (
                        row.name
                    )
                    st.session_state.page = "detail"
                    st.rerun()

        with right_col:

            branch_map = build_map(
                st.session_state.current_latitude,
                st.session_state.current_longitude,
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


# =========================================================
# DETAIL SCREEN
# =========================================================

elif st.session_state.page == "detail":

    recommendations = st.session_state.recommendations

    if recommendations is None:
        st.session_state.page = "home"
        st.rerun()

    selected_index = st.session_state.selected_branch_index

    if selected_index not in recommendations.index:
        selected_index = recommendations.index[0]

    row = recommendations.loc[selected_index]

    if st.button("← Back to recommendations"):
        st.session_state.page = "results"
        st.rerun()

    detail_left, detail_right = st.columns(
        [1.1, 0.9],
        gap="large",
    )

    with detail_left:

        st.markdown(
            f"""
            <div class="bf-eyebrow">{row["bank"]}</div>
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
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="score-box" style="width:140px;margin:18px 0;">
                <strong>{row["suitability_score"]:.2f}</strong>
                <span>SUITABILITY</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "### Why we recommend it"
        )

        reasons = []

        if row["customer_distance_km"] <= 2:
            reasons.append("Very close to your location")

        if row["nearest_bus_km"] <= 2:
            reasons.append("Good bus accessibility")

        if row["nearest_railway_km"] <= 3:
            reasons.append("Good railway accessibility")

        if row["nearest_metro_km"] <= 2:
            reasons.append("Metro access is nearby")

        if row["nearest_major_road_km"] <= 0.2:
            reasons.append("Good major-road accessibility")

        if row["suitability_score"] >= 80:
            reasons.append("Strong overall suitability")

        if not reasons:
            reasons.append(
                "Suitable based on the overall accessibility score"
            )

        for reason in reasons:
            st.markdown(
                f"✓ {reason}"
            )

        st.markdown("### Accessibility")

        access_items = [
            ("Distance", f'{row["customer_distance_km"]:.2f} km'),
            ("Metro", f'{row["nearest_metro_km"]:.2f} km'),
            ("Bus", f'{row["nearest_bus_km"]:.2f} km'),
            ("Railway", f'{row["nearest_railway_km"]:.2f} km'),
            ("Major Road", f'{row["nearest_major_road_km"]:.2f} km'),
            ("Nearby Branches", int(row["nearby_branch_count"])),
        ]

        cols = st.columns(2)

        for i, (label, value) in enumerate(access_items):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="access-box">
                        <span class="access-label">{label}</span>
                        <span class="access-value">{value}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with detail_right:

        detail_map = build_map(
            st.session_state.current_latitude,
            st.session_state.current_longitude,
            recommendations,
            focus_index=selected_index,
        )

        st_folium(
            detail_map,
            width=None,
            height=470,
            returned_objects=[],
        )


# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#697386;
        font-size:11px;
        padding:30px 0 5px;
    ">
        Bank Branch Location Optimization using Spatial Analytics
        · Map data © OpenStreetMap contributors
    </div>
    """,
    unsafe_allow_html=True,
)
'''

path = Path("/mnt/data/app_branchfinder.py")
path.write_text(app, encoding="utf-8")
print(f"Created: {path}")
