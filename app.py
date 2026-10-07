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
        --background: #f6f8fb;
        --white: #ffffff;
    }

    /* Page */

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


    /* Header */

    .bf-header {
        margin-top: 18px;
        margin-bottom: 30px;

        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 14px;

        padding: 13px 20px;

        box-shadow: 0 8px 25px rgba(16, 35, 63, 0.05);
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
    }


    /* Hero */

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
    }


    /* Search panel */

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


    /* Inputs */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {

        border-color: var(--line) !important;

        border-radius: 12px !important;

        background: #ffffff !important;
    }


    /* Buttons */

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


    /* Primary button */

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


    /* Radio options */

    div[role="radiogroup"] {
        gap: 10px;
    }

    div[role="radiogroup"] label {

        border: 1px solid var(--line);

        border-radius: 13px;

        padding: 9px 13px;

        background: #ffffff;
    }


    /* Results */

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


    /* Recommendation card */

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


    /* Badge */

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


    /* Bank */

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


    /* Suitability */

    .bf-suitability {

        font-size: 25px;

        font-weight: 900;

        color: var(--navy);
    }

    .bf-suitability-label {

        font-size: 11px;

        color: var(--muted);

        font-weight: 700;
    }


    /* Distance */

    .bf-distance {

        font-weight: 850;

        color: var(--blue);

        font-size: 15px;
    }


    /* Transport chips */

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


    /* Why recommendation */

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


    /* Footer */

    .bf-footer {

        text-align: center;

        color: var(--muted);

        font-size: 11px;

        margin-top: 30px;
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
# REQUIRED COLUMN CHECK
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

if "show_results" not in st.session_state:

    st.session_state.show_results = False


if "current_latitude" not in st.session_state:

    st.session_state.current_latitude = None


if "current_longitude" not in st.session_state:

    st.session_state.current_longitude = None


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
# HERO
# ============================================================

if not st.session_state.show_results:

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SEARCH PANEL
# ============================================================

if not st.session_state.show_results:

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


    location_option = st.radio(

        "Choose your location method",

        [
            "Use My Current Location",
            "Enter Coordinates",
        ],

        horizontal=True,

        label_visibility="collapsed",
    )


    # ========================================================
    # CURRENT LOCATION
    # ========================================================

    if location_option == "Use My Current Location":

        location_col1, location_col2 = st.columns(
            [3, 1]
        )


        with location_col1:

            if (

                st.session_state.current_latitude
                is not None

                and

                st.session_state.current_longitude
                is not None

            ):

                st.success(
                    "Your current location was detected."
                )

            else:

                st.markdown(
                    """
                    <div class="bf-hint">

                        Click "Use My Current Location"
                        and allow location access when
                        your browser asks for permission.

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


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


    # ========================================================
    # ENTER COORDINATES
    # ========================================================

    else:

        coordinate_col1, coordinate_col2 = st.columns(
            2
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
        '<div style="height:18px;"></div>',
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
        '<div style="height:18px;"></div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # WHAT MATTERS MOST
    # ========================================================

    st.markdown(
        """
        <div class="bf-section-title">
            What matters most?
        </div>
        """,
        unsafe_allow_html=True,
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
        '<div style="height:18px;"></div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # MAXIMUM DISTANCE
    # ========================================================

    distance_col1, distance_col2 = st.columns(
        [1, 3]
    )


    with distance_col1:

        max_distance = st.number_input(

            "Maximum Distance (km)",

            min_value=0.1,

            max_value=500.0,

            value=10.0,

            step=1.0,
        )


    with distance_col2:

        st.markdown(
            """
            <div
                class="bf-hint"
                style="padding-top:30px;"
            >

                Only branches within this distance
                will be considered.

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown(
        '<div style="height:8px;"></div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # FIND BUTTON
    # ========================================================

    button_col1, button_col2 = st.columns(
        [4, 1]
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


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# RECOMMENDATION PROCESS
# ============================================================

if find_clicked if "find_clicked" in locals() else False:

    latitude = None

    longitude = None


    # ========================================================
    # CURRENT LOCATION
    # ========================================================

    if location_option == "Use My Current Location":

        latitude = (
            st.session_state.current_latitude
        )

        longitude = (
            st.session_state.current_longitude
        )


        if latitude is None or longitude is None:

            st.error(
                "Please allow location access first."
            )

            st.stop()


    # ========================================================
    # ENTERED COORDINATES
    # ========================================================

    else:

        if latitude_input.strip() == "":

            st.error(
                "Please enter your latitude."
            )

            st.stop()


        if longitude_input.strip() == "":

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


    # ========================================================
    # CALCULATE CUSTOMER DISTANCE
    # ========================================================

    customer_location = np.radians(
        [[latitude, longitude]]
    )


    branch_locations = np.radians(
        data[
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


    recommendation_data = data.copy()


    recommendation_data[
        "customer_distance_km"
    ] = distances


    # ========================================================
    # BANK FILTER
    # ========================================================

    if bank_preference == "Public":

        recommendation_data = (

            recommendation_data[

                recommendation_data["bank_group"]

                ==

                "Public Sector Banks"

            ]

            .copy()

        )


    elif bank_preference == "Private":

        recommendation_data = (

            recommendation_data[

                recommendation_data["bank_group"]

                ==

                "Private Sector Banks"

            ]

            .copy()

        )


    # ========================================================
    # DISTANCE FILTER
    # ========================================================

    recommendation_data = (

        recommendation_data[

            recommendation_data[
                "customer_distance_km"
            ]

            <=

            max_distance

        ]

        .copy()

    )


    # ========================================================
    # RECOMMENDATION SCORE
    # ========================================================

    if len(recommendation_data) > 0:

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
            ]

            * 0.7

            +

            recommendation_data[
                "distance_score"
            ]

            * 30

        )


    # ========================================================
    # PRIORITY SORTING
    # ========================================================

    if len(recommendation_data) > 0:


        if priority == "Closest":

            recommendation_data = (

                recommendation_data.sort_values(

                    [
                        "customer_distance_km",
                        "suitability_score",
                    ],

                    ascending=[
                        True,
                        False,
                    ]

                )

            )


        elif priority == "Public Transport":

            recommendation_data[
                "transport_distance"
            ] = (

                recommendation_data[
                    "nearest_bus_km"
                ]

                +

                recommendation_data[
                    "nearest_railway_km"
                ]

                +

                recommendation_data[
                    "nearest_metro_km"
                ]

            )


            recommendation_data = (

                recommendation_data.sort_values(

                    [
                        "transport_distance",
                        "recommendation_score",
                    ],

                    ascending=[
                        True,
                        False,
                    ]

                )

            )


        elif priority == "Easy Road Access":

            recommendation_data = (

                recommendation_data.sort_values(

                    [
                        "nearest_major_road_km",
                        "recommendation_score",
                    ],

                    ascending=[
                        True,
                        False,
                    ]

                )

            )


        else:

            recommendation_data = (

                recommendation_data.sort_values(

                    "recommendation_score",

                    ascending=False

                )

            )


    # ========================================================
    # SHOW RESULTS
    # ========================================================

    st.session_state.show_results = True


    # ========================================================
    # RESULTS HEADER
    # ========================================================

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


    st.write(

        f"**{len(recommendation_data)} branches found** "
        f"within {max_distance:.1f} km"

    )


    # ========================================================
    # NO RESULTS
    # ========================================================

    if len(recommendation_data) == 0:

        st.warning(

            "No bank branches were found within "
            "the selected distance and bank preference."

        )


    # ========================================================
    # RESULTS
    # ========================================================

    else:

        left_col, right_col = st.columns(
            [1, 1.45],
            gap="large",
        )


        # ====================================================
        # CARDS
        # ====================================================

        with left_col:


            for rank, (_, row) in enumerate(

                recommendation_data.head(10).iterrows(),

                start=1

            ):


                # --------------------------------------------
                # Recommendation reasons
                # --------------------------------------------

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
                        "Good bus accessibility"
                    )


                if row[
                    "nearest_railway_km"
                ] <= 3:

                    reasons.append(
                        "Good railway accessibility"
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
                        ✓ {reason}
                    </span>
                    """

                    for reason in reasons[:3]

                )


                # --------------------------------------------
                # Best match
                # --------------------------------------------

                if rank == 1:

                    badge = "★ Best Match"

                    card_class = (
                        "bf-card best"
                    )

                else:

                    badge = "Recommended"

                    card_class = "bf-card"


                # --------------------------------------------
                # Recommendation card
                # --------------------------------------------

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

                            {row["customer_distance_km"]:.2f} km

                        </div>


                    </div>


                    <div>


                        <span class="bf-chip">

                            Nearest Metro

                            <b>
                                {row["nearest_metro_km"]:.2f} km
                            </b>

                        </span>


                        <span class="bf-chip">

                            Nearest Bus

                            <b>
                                {row["nearest_bus_km"]:.2f} km
                            </b>

                        </span>


                        <span class="bf-chip">

                            Nearest Railway

                            <b>
                                {row["nearest_railway_km"]:.2f} km
                            </b>

                        </span>


                        <span class="bf-chip">

                            Nearest Major Road

                            <b>
                                {row["nearest_major_road_km"]:.2f} km
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


                # IMPORTANT:
                # st.html() is used here so Streamlit
                # renders the HTML instead of showing it
                # as text.

                st.html(card_html)


                # --------------------------------------------
                # Card actions
                # --------------------------------------------

                action_col1, action_col2 = st.columns(
                    2
                )


                with action_col1:

                    if st.button(

                        "View Details",

                        key=f"details_{rank}",

                        use_container_width=True,

                    ):

                        st.session_state[
                            "selected_branch"
                        ] = row.to_dict()

                        st.session_state[
                            "show_details"
                        ] = True


                        st.rerun()


                with action_col2:

                    maps_url = (

                        "https://www.google.com/maps/dir/?api=1"

                        f"&destination="
                        f"{row['lattitude']},"
                        f"{row['longitude']}"

                    )


                    st.link_button(

                        "Directions",

                        maps_url,

                        use_container_width=True,

                    )


        # ====================================================
        # MAP
        # ====================================================

        with right_col:


            st.subheader(
                "Branch Location Map"
            )


            branch_map = folium.Map(

                location=[
                    latitude,
                    longitude
                ],

                zoom_start=12,

                control_scale=True,

            )


            # --------------------------------------------
            # Customer marker
            # --------------------------------------------

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


            # --------------------------------------------
            # Branch markers
            # --------------------------------------------

            for marker_rank, (_, row) in enumerate(

                recommendation_data.head(10).iterrows(),

                start=1

            ):


                popup_text = f"""

                <b>{row['bank']}</b><br>

                Branch: {row['branch']}<br>

                Bank Type: {row['bank_group']}<br>

                Distance:
                {row['customer_distance_km']:.2f} km<br>

                Suitability:
                {row['suitability']}<br>

                Nearest Bus:
                {row['nearest_bus_km']:.2f} km<br>

                Nearest Railway:
                {row['nearest_railway_km']:.2f} km<br>

                Nearest Metro:
                {row['nearest_metro_km']:.2f} km<br>

                Nearest Major Road:
                {row['nearest_major_road_km']:.2f} km

                """


                folium.Marker(

                    [
                        row["lattitude"],
                        row["longitude"]
                    ],

                    popup=folium.Popup(

                        popup_text,

                        max_width=320

                    ),

                    tooltip=row["bank"],

                    icon=folium.Icon(

                        color=(
                            "green"
                            if marker_rank == 1
                            else "blue"
                        ),

                        icon=(
                            "star"
                            if marker_rank == 1
                            else "bank"
                        )

                    )

                ).add_to(branch_map)


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
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="bf-footer">

        Bank Branch Location Optimization using
        Spatial Analytics

        ·

        Map data © OpenStreetMap contributors.

    </div>
    """,
    unsafe_allow_html=True,
)
