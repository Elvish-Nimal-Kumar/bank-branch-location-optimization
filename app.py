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
# HTML RENDER HELPER
# ============================================================

def html(content):
    """Render HTML directly with Streamlit's HTML renderer."""
    st.html(content)


# ============================================================
# GLOBAL CSS
# ============================================================

html("""
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


/* ============================================================
   HEADER
   ============================================================ */

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
    width: 34px;
    height: 34px;

    border-radius: 10px;

    background: var(--navy);
    color: #ffffff;

    display: inline-flex;

    align-items: center;
    justify-content: center;

    margin-right: 9px;

    font-size: 18px;
}


/* ============================================================
   HERO
   ============================================================ */

.bf-hero {
    max-width: 790px;

    margin: 20px auto 32px;

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

    font-size: 44px;

    line-height: 1.08;

    letter-spacing: -.035em;

    margin: 10px 0 13px;
}

.bf-hero p {
    color: var(--muted);

    font-size: 16px;

    line-height: 1.65;

    margin: 0;
}


/* ============================================================
   PANEL
   ============================================================ */

.bf-panel {
    background: #ffffff;

    border: 1px solid var(--line);

    border-radius: 18px;

    padding: 27px;

    box-shadow:
        0 14px 35px rgba(16, 35, 63, .07);
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


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {

    border-color: var(--line) !important;

    border-radius: 12px !important;

    background: #ffffff !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

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


/* ============================================================
   RADIO
   ============================================================ */

div[role="radiogroup"] {
    gap: 10px;
}

div[role="radiogroup"] label {

    border: 1px solid var(--line);

    border-radius: 13px;

    padding: 9px 13px;

    background: #ffffff;
}


/* ============================================================
   RESULTS
   ============================================================ */

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


/* ============================================================
   RECOMMENDATION CARD
   ============================================================ */

.bf-card {

    background: #ffffff;

    border: 1px solid var(--line);

    border-radius: 16px;

    padding: 18px;

    margin: 10px 0 12px;

    box-shadow:
        0 4px 16px rgba(16, 35, 63, .035);
}

.bf-card.best {

    border-color: #9bd8bd;
}

.bf-badge {

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

.bf-distance {

    font-weight: 850;

    color: var(--blue);

    font-size: 15px;
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

    color: var(--navy);
}

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


/* ============================================================
   FOOTER
   ============================================================ */

.bf-footer {

    text-align: center;

    color: var(--muted);

    font-size: 11px;

    margin-top: 30px;
}

</style>
""")


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


missing = [

    c

    for c in required_columns

    if c not in data.columns

]


if missing:

    st.error(

        "The dataset is missing required columns: "

        + ", ".join(missing)

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

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# CALCULATE RECOMMENDATIONS
# ============================================================

def calculate_recommendations(

    df,

    latitude,

    longitude,

    bank_preference,

    priority,

    max_distance,

):

    result = df.copy()


    # --------------------------------------------------------
    # Customer location
    # --------------------------------------------------------

    customer_location = np.radians(

        [[
            latitude,
            longitude
        ]]

    )


    branch_locations = np.radians(

        result[
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


    result[
        "customer_distance_km"
    ] = distances


    # --------------------------------------------------------
    # Bank preference
    # --------------------------------------------------------

    if bank_preference == "Public":

        result = result[

            result["bank_group"]

            ==

            "Public Sector Banks"

        ].copy()


    elif bank_preference == "Private":

        result = result[

            result["bank_group"]

            ==

            "Private Sector Banks"

        ].copy()


    # --------------------------------------------------------
    # Distance filter
    # --------------------------------------------------------

    result = result[

        result[
            "customer_distance_km"
        ]

        <=

        max_distance

    ].copy()


    if result.empty:

        return result


    # --------------------------------------------------------
    # Existing recommendation logic
    #
    # Suitability = 70%
    # Proximity    = 30%
    # --------------------------------------------------------

    result[
        "distance_score"
    ] = (

        1

        /

        (

            1

            +

            result[
                "customer_distance_km"
            ]

        )

    )


    result[
        "recommendation_score"
    ] = (

        result[
            "suitability_score"
        ]

        * 0.70

        +

        result[
            "distance_score"
        ]

        * 30

    )


    # --------------------------------------------------------
    # Priority
    # --------------------------------------------------------

    if priority == "Closest":

        result = result.sort_values(

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

        result[
            "transport_distance"
        ] = (

            result[
                "nearest_bus_km"
            ]

            +

            result[
                "nearest_railway_km"
            ]

            +

            result[
                "nearest_metro_km"
            ]

        )


        result = result.sort_values(

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

        result = result.sort_values(

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

        result = result.sort_values(

            "recommendation_score",

            ascending=False,

        )


    return result


# ============================================================
# RECOMMENDATION REASONS
# ============================================================

def get_reasons(row):

    reasons = []


    if row[
        "customer_distance_km"
    ] <= 2:

        reasons.append(
            "Very close to you"
        )

    elif row[
        "customer_distance_km"
    ] <= 5:

        reasons.append(
            "Close to you"
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


    return reasons[:3]


# ============================================================
# BUILD MAP
# ============================================================

def build_map(

    latitude,

    longitude,

    recommendations,

):

    m = folium.Map(

        location=[

            latitude,

            longitude

        ],

        zoom_start=12,

        control_scale=True,

    )


    # --------------------------------------------------------
    # User location
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

            icon="user",

        ),

    ).add_to(m)


    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    for rank, (_, row) in enumerate(

        recommendations.head(10).iterrows(),

        start=1,

    ):


        popup = f"""

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

        """


        folium.Marker(

            [

                row["lattitude"],

                row["longitude"]

            ],

            popup=folium.Popup(

                popup,

                max_width=320,

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

                ),

            ),

        ).add_to(m)


    return m


# ============================================================
# DIRECTIONS
# ============================================================

def directions_url(row):

    return (

        "https://www.google.com/maps/dir/?api=1"

        f"&destination="

        f"{row['lattitude']},"

        f"{row['longitude']}"

    )


# ============================================================
# HEADER
# ============================================================

html("""
<div class="bf-header">

    <div class="bf-brand">

        <span class="bf-mark">
            ⌖
        </span>

        Bank Branch Finder

    </div>

</div>
""")


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":


    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    html("""
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
    """)


    # --------------------------------------------------------
    # Search panel
    # --------------------------------------------------------

    html("""
    <div class="bf-panel">

        <div class="bf-section-title">
            Where are you?
        </div>

    </div>
    """)


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


    # --------------------------------------------------------
    # Current location
    # --------------------------------------------------------

    if (

        location_option

        ==

        "Use My Current Location"

    ):


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

                html("""
                <div class="bf-hint">

                    Click "Use My Current Location"
                    and allow location access when
                    your browser asks.

                </div>
                """)


        with col2:


            st.markdown(

                '<div class="primary-button">',

                unsafe_allow_html=True,

            )


            location_clicked = st.button(

                "Use My Current Location",

                use_container_width=True,

            )


            st.markdown(

                "</div>",

                unsafe_allow_html=True,

            )


        if location_clicked:


            location = get_geolocation()


            if (

                location

                and

                "coords"

                in

                location

            ):


                st.session_state.latitude = (

                    location[
                        "coords"
                    ][
                        "latitude"
                    ]

                )


                st.session_state.longitude = (

                    location[
                        "coords"
                    ][
                        "longitude"
                    ]

                )


                st.success(

                    "Current location detected."

                )


                st.rerun()


            elif (

                location

                and

                "error"

                in

                location

            ):

                st.error(

                    "Unable to get your location. "
                    "Please allow location access "
                    "in your browser."

                )


    # --------------------------------------------------------
    # Manual coordinates
    # --------------------------------------------------------

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

        unsafe_allow_html=True,

    )


    # --------------------------------------------------------
    # Bank preference
    # --------------------------------------------------------

    html("""
    <div class="bf-section-title">

        Which bank do you prefer?

    </div>
    """)


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

        unsafe_allow_html=True,

    )


    # --------------------------------------------------------
    # Priority
    # --------------------------------------------------------

    html("""
    <div class="bf-section-title">

        What matters most?

    </div>
    """)


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


    priority_map = {

        "⭐ Best Overall":
            "Best Overall",

        "🚶 Closest":
            "Closest",

        "🚌 Public Transport":
            "Public Transport",

        "🚗 Easy Road Access":
            "Easy Road Access",

    }


    priority = priority_map[
        priority_display
    ]


    st.markdown(

        "<div style='height:18px'></div>",

        unsafe_allow_html=True,

    )


    # --------------------------------------------------------
    # Maximum distance
    # --------------------------------------------------------

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


        html("""
        <div
            class="bf-hint"
            style="padding-top:30px;"
        >

            Only branches within this distance
            will be considered for the recommendation.

        </div>
        """)


    st.markdown(

        "<div style='height:8px'></div>",

        unsafe_allow_html=True,

    )


    # --------------------------------------------------------
    # Find button
    # --------------------------------------------------------

    col1, col2 = st.columns(

        [4, 1]

    )


    with col2:


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


    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    if find_clicked:


        # --------------------------------------------
        # Location
        # --------------------------------------------

        if (

            location_option

            ==

            "Use My Current Location"

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


        # --------------------------------------------
        # Calculate recommendations
        # --------------------------------------------

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


    html("""
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
    """)


    col1, col2 = st.columns(

        [4, 1]

    )


    with col1:

        st.write(

            f"**{len(recommendations)} branches found**"

        )


    with col2:

        if st.button(

            "← Change Search",

            use_container_width=True,

        ):

            st.session_state.page = "home"

            st.rerun()


    if recommendations.empty:


        st.warning(

            "No bank branches were found within "
            "the selected distance and bank preference."

        )


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

                recommendations.head(10).iterrows(),

                start=1,

            ):


                reasons = get_reasons(

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


                card = f"""

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


                # IMPORTANT:
                # Direct HTML renderer.
                st.html(card)


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

                        directions_url(row),

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


    if st.button(

        "← Back to Recommendations"

    ):

        st.session_state.page = "results"

        st.rerun()


    left_col, right_col = st.columns(

        [1, 1],

        gap="large",

    )


    # ========================================================
    # DETAILS
    # ========================================================

    with left_col:


        address = row.get(

            "address",

            ""

        )


        html(

            f"""

            <div class="bf-card">


                <div class="bf-eyebrow">

                    {row["bank"]}

                </div>


                <div style="
                    font-size:30px;
                    font-weight:850;
                    color:#10233f;
                    margin:6px 0;
                ">

                    {row["branch"]}

                </div>


                <div class="bf-branch">

                    {address}

                </div>


                <div style="
                    display:inline-block;
                    margin-top:20px;
                    background:#eaf8f2;
                    color:#16835b;
                    border-radius:12px;
                    padding:13px 20px;
                ">


                    <strong style="
                        display:block;
                        font-size:28px;
                    ">

                        {row["suitability"]}

                    </strong>


                    <span style="
                        font-size:10px;
                        font-weight:800;
                    ">

                        SUITABILITY

                    </span>


                </div>


            </div>

            """

        )


        html("""

        <div class="bf-section-title"
             style="margin-top:22px;">

            Why we recommend it

        </div>

        """)


        for reason in get_reasons(row):

            st.markdown(

                f"✓ {reason}"

            )


        html("""

        <div class="bf-section-title"
             style="margin-top:22px;">

            Accessibility

        </div>

        """)


        access_items = [

            (

                "Distance from you",

                f'{row["customer_distance_km"]:.2f} km',

            ),

            (

                "Nearest Bus",

                f'{row["nearest_bus_km"]:.2f} km',

            ),

            (

                "Nearest Railway",

                f'{row["nearest_railway_km"]:.2f} km',

            ),

            (

                "Nearest Metro",

                f'{row["nearest_metro_km"]:.2f} km',

            ),

            (

                "Nearest Major Road",

                f'{row["nearest_major_road_km"]:.2f} km',

            ),

            (

                "Nearby Branches",

                str(

                    int(

                        row[
                            "nearby_branch_count"
                        ]

                    )

                ),

            ),

        ]


        c1, c2 = st.columns(

            2

        )


        for index, (

            label,

            value

        ) in enumerate(access_items):


            target = (

                c1

                if index % 2 == 0

                else c2

            )


            with target:


                html(

                    f"""

                    <div class="bf-card"
                         style="
                            padding:13px;
                            margin:4px 0;
                            background:#f8f9fb;
                            box-shadow:none;
                         ">


                        <div style="
                            color:#697386;
                            font-size:11px;
                        ">

                            {label}

                        </div>


                        <div style="
                            color:#10233f;
                            font-weight:800;
                            margin-top:4px;
                        ">

                            {value}

                        </div>


                    </div>

                    """

                )


        st.link_button(

            "Get Directions →",

            directions_url(row),

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

html("""

<div class="bf-footer">

    Bank Branch Location Optimization using
    Spatial Analytics

    ·

    Map data © OpenStreetMap contributors.

</div>

""")
