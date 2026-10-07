import streamlit as st
import pandas as pd
import numpy as np
import textwrap

from sklearn.metrics.pairwise import haversine_distances
from streamlit_js_eval import get_geolocation

import folium
from streamlit_folium import st_folium


# -----------------------------------
# Load Dataset
# -----------------------------------

data = pd.read_csv(
    "final_bank_recommendation_data.csv"
)


# -----------------------------------
# BranchFinder visual redesign
# -----------------------------------

st.set_page_config(
    page_title="Bank Branch Finder",
    page_icon="⌖",
    layout="wide",
)


st.markdown(
    """
    <style>

    .stApp {
        background: #f6f8fb;
        color: #172033;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1240px;
        padding: 1.5rem 2rem 4rem;
    }

    .bf-header {
        margin-top: 12px;
        background: #fff;
        border: 1px solid #e4e8ef;
        border-radius: 14px;
        padding: 13px 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(16,35,63,.05);
    }

    .bf-brand {
        font-size: 21px;
        font-weight: 800;
        color: #10233f;
    }

    .bf-mark {
        display: inline-flex;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #10233f;
        color: #fff;
        align-items: center;
        justify-content: center;
        margin-right: 9px;
    }

    .bf-hero {
        text-align: center;
        max-width: 790px;
        margin: 20px auto 32px;
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
        margin: 10px 0 13px;
    }

    .bf-hero p {
        color: #697386;
        font-size: 16px;
        line-height: 1.65;
    }

    .bf-panel {
        background: #fff;
        border: 1px solid #e4e8ef;
        border-radius: 18px;
        padding: 27px;
        box-shadow: 0 14px 35px rgba(16,35,63,.07);
    }

    .bf-section-title {
        color: #10233f;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-color: #e4e8ef !important;
        border-radius: 12px !important;
        background: #fff !important;
    }

    .stButton > button {
        border-radius: 11px;
        min-height: 42px;
        font-weight: 750;
        border: 1px solid #e4e8ef;
        background: #fff;
        color: #10233f;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
    }

    .bf-primary .stButton > button {
        background: #2563eb;
        color: #fff;
        border-color: #2563eb;
    }

    .bf-primary .stButton > button:hover {
        background: #1d4ed8;
        color: #fff;
        border-color: #1d4ed8;
    }

    div[role="radiogroup"] {
        gap: 10px;
    }

    .bf-results-title {
        color: #10233f;
        font-size: 29px;
        font-weight: 850;
        margin: 5px 0;
    }

    .bf-results-sub {
        color: #697386;
        font-size: 13px;
    }

    .bf-card {
        background: #fff;
        border: 1px solid #e4e8ef;
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
        box-shadow: 0 4px 16px rgba(16,35,63,.035);
    }

    .bf-card:first-child {
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
    }

    .bf-bank {
        font-size: 18px;
        font-weight: 850;
        color: #10233f;
        margin-top: 9px;
    }

    .bf-branch {
        font-size: 13px;
        color: #697386;
        margin-top: 3px;
    }

    .bf-score {
        font-size: 15px;
        font-weight: 800;
        color: #16835b;
        background: #eaf8f2;
        padding: 6px 10px;
        border-radius: 8px;
    }

    .bf-score-label {
        font-size: 11px;
        color: #697386;
        font-weight: 700;
    }

    .bf-distance {
        font-weight: 850;
        color: #2563eb;
    }

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
        color: #10233f;
    }

    .bf-why {
        margin-top: 13px;
        padding-top: 12px;
        border-top: 1px solid #e4e8ef;
    }

    .bf-why-title {
        font-size: 12px;
        font-weight: 850;
        color: #10233f;
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

    .bf-footer {
        text-align: center;
        color: #697386;
        font-size: 11px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Header
# -----------------------------------

st.markdown(
    """
    <div class="bf-header">
        <div class="bf-brand">
            <span class="bf-mark">⌖</span>
            Bank Branch Finder
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Session State
# -----------------------------------

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "current_latitude" not in st.session_state:
    st.session_state.current_latitude = None

if "current_longitude" not in st.session_state:
    st.session_state.current_longitude = None


# -----------------------------------
# Hero
# -----------------------------------

if not st.session_state.show_results:

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
        unsafe_allow_html=True
    )


# -----------------------------------
# Main Panel
# -----------------------------------

if not st.session_state.show_results:

    st.markdown(
        '<div class="bf-panel">',
        unsafe_allow_html=True
    )


# -----------------------------------
# Customer Location
# -----------------------------------

if not st.session_state.show_results:

    st.subheader("Where are you?")

    location_option = st.radio(
        "Choose your location method",
        [
            "Use My Current Location",
            "Enter Coordinates"
        ],
        horizontal=True
    )


    # -----------------------------------
    # Current Location
    # -----------------------------------

    if location_option == "Use My Current Location":

        st.write(
            "Click below and allow location access "
            "when your browser asks for permission."
        )

        location_button_col, location_status_col = st.columns(
            [1, 3]
        )

        with location_button_col:

            if st.button(
                "Use My Current Location",
                use_container_width=True
            ):

                location = get_geolocation()

                if location:

                    if "error" in location:

                        st.error(
                            "Unable to get your location. "
                            "Please allow location access "
                            "in your browser."
                        )

                    elif "coords" in location:

                        st.session_state.current_latitude = (
                            location["coords"]["latitude"]
                        )

                        st.session_state.current_longitude = (
                            location["coords"]["longitude"]
                        )

                        st.success(
                            "Your current location was detected."
                        )


        with location_status_col:

            if (
                st.session_state.current_latitude is not None
                and
                st.session_state.current_longitude is not None
            ):

                st.success(
                    "Location ready."
                )


    # -----------------------------------
    # Enter Coordinates
    # -----------------------------------

    else:

        latitude_col, longitude_col = st.columns(2)

        with latitude_col:

            latitude_input = st.text_input(
                "Latitude",
                placeholder="Example: 13.0827"
            )

        with longitude_col:

            longitude_input = st.text_input(
                "Longitude",
                placeholder="Example: 80.2707"
            )


    # -----------------------------------
    # Bank Preferences
    # -----------------------------------

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True
    )

    st.subheader("Which bank do you prefer?")

    bank_preference = st.radio(
        "Bank Preference",
        [
            "Any",
            "Public",
            "Private"
        ],
        horizontal=True
    )


    # -----------------------------------
    # Maximum Distance
    # -----------------------------------

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True
    )

    max_distance = st.text_input(
        "Maximum Distance (km)",
        value="10"
    )


    # -----------------------------------
    # Find Banks Button
    # -----------------------------------

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="bf-primary">',
        unsafe_allow_html=True
    )

    if st.button(
        "Find Recommended Banks",
        use_container_width=True
    ):

        st.session_state.show_results = True

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# -----------------------------------
# Recommendation Process
# -----------------------------------

if st.session_state.show_results:

    latitude = None
    longitude = None


    # -----------------------------------
    # Use Current Location
    # -----------------------------------

    if location_option == "Use My Current Location":

        latitude = (
            st.session_state.current_latitude
        )

        longitude = (
            st.session_state.current_longitude
        )

        if (
            latitude is None
            or
            longitude is None
        ):

            st.error(
                "Please allow location access first."
            )

            st.session_state.show_results = False

            st.stop()


    # -----------------------------------
    # Use Entered Coordinates
    # -----------------------------------

    else:

        if latitude_input.strip() == "":

            st.error(
                "Please enter your latitude."
            )

            st.session_state.show_results = False

            st.stop()


        if longitude_input.strip() == "":

            st.error(
                "Please enter your longitude."
            )

            st.session_state.show_results = False

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

            st.session_state.show_results = False

            st.stop()


        # Validate latitude

        if latitude < -90 or latitude > 90:

            st.error(
                "Latitude must be between "
                "-90 and 90."
            )

            st.session_state.show_results = False

            st.stop()


        # Validate longitude

        if longitude < -180 or longitude > 180:

            st.error(
                "Longitude must be between "
                "-180 and 180."
            )

            st.session_state.show_results = False

            st.stop()


    # -----------------------------------
    # Validate Maximum Distance
    # -----------------------------------

    try:

        max_distance = float(
            max_distance
        )

    except ValueError:

        st.error(
            "Please enter a valid maximum distance."
        )

        st.session_state.show_results = False

        st.stop()


    if max_distance <= 0:

        st.error(
            "Maximum distance must be greater than 0."
        )

        st.session_state.show_results = False

        st.stop()


    # -----------------------------------
    # Calculate Distance
    # -----------------------------------

    recommendation_data = data.copy()

    customer_location = np.radians(
        [[latitude, longitude]]
    )

    branch_locations = np.radians(
        recommendation_data[
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
        )
        * 6371
    )

    recommendation_data[
        "customer_distance_km"
    ] = distances[0]


    # -----------------------------------
    # Apply Bank Preference
    # -----------------------------------

    if bank_preference == "Public":

        recommendation_data = recommendation_data[
            recommendation_data["bank_group"]
            == "Public Sector Banks"
        ].copy()


    elif bank_preference == "Private":

        recommendation_data = recommendation_data[
            recommendation_data["bank_group"]
            == "Private Sector Banks"
        ].copy()


    # -----------------------------------
    # Apply Maximum Distance
    # -----------------------------------

    recommendation_data = recommendation_data[
        recommendation_data["customer_distance_km"]
        <= max_distance
    ].copy()


    # -----------------------------------
    # Recommendation Score
    # -----------------------------------

    recommendation_data[
        "distance_score"
    ] = (
        1
        /
        (
            1
            +
            recommendation_data[
                "customer_distance_km"
            ]
        )
    )


    recommendation_data[
        "recommendation_score"
    ] = (
        recommendation_data[
            "suitability_score"
        ] * 0.7

        +

        recommendation_data[
            "distance_score"
        ] * 30
    )


    # -----------------------------------
    # Sort Recommendations
    # -----------------------------------

    recommendations = (
        recommendation_data
        .sort_values(
            "recommendation_score",
            ascending=False
        )
    )


    # -----------------------------------
    # Recommendation Results
    # -----------------------------------

    st.markdown(
        """
        <div class="bf-eyebrow">
            Recommendations
        </div>

        <div class="bf-results-title">
            Recommended branches
        </div>

        <div class="bf-results-sub">
            Based on your location, preferences,
            accessibility, and branch suitability.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write(
        f"{len(recommendations)} branches found "
        f"within {max_distance} km"
    )


    # -----------------------------------
    # No Results
    # -----------------------------------

    if len(recommendations) == 0:

        st.warning(
            "No bank branches found within "
            "the selected distance."
        )

        if st.button("← Change Search"):

            st.session_state.show_results = False

            st.rerun()


    # -----------------------------------
    # Recommendation + Map Layout
    # -----------------------------------

    else:

        left_col, right_col = st.columns(
            [1, 1.35],
            gap="large"
        )


        # -----------------------------------
        # Recommendation Cards
        # -----------------------------------

        with left_col:

            for index, (_, row) in enumerate(
                recommendations.head(10).iterrows()
            ):

                reasons = []


                if row[
                    "customer_distance_km"
                ] <= 2:

                    reasons.append(
                        "Very close to you"
                    )


                if row[
                    "nearest_bus_km"
                ] <= 2:

                    reasons.append(
                        "Good bus access"
                    )


                if row[
                    "nearest_railway_km"
                ] <= 3:

                    reasons.append(
                        "Good railway access"
                    )


                if row[
                    "nearest_metro_km"
                ] <= 2:

                    reasons.append(
                        "Metro access nearby"
                    )


                if row[
                    "nearest_major_road_km"
                ] <= 0.2:

                    reasons.append(
                        "Good road accessibility"
                    )


                if row[
                    "suitability_score"
                ] >= 80:

                    reasons.append(
                        "Strong overall accessibility"
                    )


                if not reasons:

                    reasons.append(
                        "Suitable overall"
                    )


                reason_html = "".join(
                    f"""
                    <span class="bf-reason">
                        ✓ {r}
                    </span>
                    """
                    for r in reasons[:3]
                )


                is_best = (
                    index == 0
                )


                st.markdown(
                    textwrap.dedent(
                        f"""
                        <div class="bf-card">

                            <span class="bf-badge">

                                {
                                    "★ Best match"
                                    if is_best
                                    else "Recommended"
                                }

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
                                margin:14px 0 10px
                            ">


                                <div>

                                    <span class="bf-score">

                                        {row["suitability"]}

                                    </span>

                                    <span class="bf-score-label">

                                        Suitability

                                    </span>

                                </div>


                                <div class="bf-distance">

                                    {
                                        row[
                                            "customer_distance_km"
                                        ]:.2f
                                    }

                                    km

                                </div>


                            </div>


                            <div>

                                <span class="bf-chip">

                                    Nearest Bus

                                    <b>
                                        {
                                            row[
                                                "nearest_bus_km"
                                            ]:.2f
                                        }
                                        km
                                    </b>

                                </span>


                                <span class="bf-chip">

                                    Nearest Railway

                                    <b>
                                        {
                                            row[
                                                "nearest_railway_km"
                                            ]:.2f
                                        }
                                        km
                                    </b>

                                </span>


                                <span class="bf-chip">

                                    Nearest Metro

                                    <b>
                                        {
                                            row[
                                                "nearest_metro_km"
                                            ]:.2f
                                        }
                                        km
                                    </b>

                                </span>


                                <span class="bf-chip">

                                    Nearest Major Road

                                    <b>
                                        {
                                            row[
                                                "nearest_major_road_km"
                                            ]:.2f
                                        }
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
                    ),
                    unsafe_allow_html=True
                )


        # -----------------------------------
        # Interactive Map
        # -----------------------------------

        with right_col:

            st.subheader(
                "Branch Location Map"
            )


            branch_map = folium.Map(
                location=[
                    latitude,
                    longitude
                ],
                zoom_start=12
            )


            # -----------------------------------
            # Customer Marker
            # -----------------------------------

            folium.Marker(
                [
                    latitude,
                    longitude
                ],

                popup="Customer Location",

                tooltip="Your Location",

                icon=folium.Icon(
                    color="red",
                    icon="user"
                )
            ).add_to(branch_map)


            # -----------------------------------
            # Recommended Branch Markers
            # -----------------------------------

            for index, (_, row) in enumerate(
                recommendations
                .head(10)
                .iterrows()
            ):

                popup_text = f"""
                <b>{row['bank']}</b><br>
                Branch: {row['branch']}<br>
                Bank Type: {row['bank_group']}<br>
                Distance: {
                    row['customer_distance_km']:.2f
                } km<br>
                Suitability: {row['suitability']}<br>
                Nearest Bus: {
                    row['nearest_bus_km']:.2f
                } km<br>
                Nearest Railway: {
                    row['nearest_railway_km']:.2f
                } km<br>
                Nearest Metro: {
                    row['nearest_metro_km']:.2f
                } km<br>
                Nearest Major Road: {
                    row['nearest_major_road_km']:.2f
                } km
                """


                folium.Marker(
                    [
                        row["lattitude"],
                        row["longitude"]
                    ],

                    popup=folium.Popup(
                        popup_text,
                        max_width=300
                    ),

                    tooltip=row["bank"],

                    icon=folium.Icon(
                        color=(
                            "green"
                            if index == 0
                            else "blue"
                        ),

                        icon=(
                            "star"
                            if index == 0
                            else "bank"
                        )
                    )
                ).add_to(branch_map)


            # -----------------------------------
            # Display Map
            # -----------------------------------

            st_folium(
                branch_map,
                width=None,
                height=600
            )


# -----------------------------------
# Attribution
# -----------------------------------

st.caption(
    "Map data © OpenStreetMap contributors."
)


st.markdown(
    """
    <div class="bf-footer">

        Bank Branch Location Optimization using
        Spatial Analytics ·

        Map data © OpenStreetMap contributors.

    </div>
    """,
    unsafe_allow_html=True
)
