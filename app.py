import streamlit as st
import pydeck as pdk
import requests

from city_graph import create_city_graph
from algorithms import find_route
from emergency import EmergencyManager
from traffic import (
    update_traffic,
    close_road,
    open_road,
    get_road_status
)

st.set_page_config(
    page_title="ResQ AI | Dehradun Emergency Command Center",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html("""
<style>
.stApp {
    background:
        radial-gradient(circle at 75% 0%, rgba(14,116,144,.18), transparent 32%),
        linear-gradient(135deg, #030914, #071321 55%, #091726);
    color: #f8fafc;
}

header[data-testid="stHeader"] {
    background: rgba(3,9,20,.9);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071321, #091a2b);
    border-right: 1px solid #1b344c;
}

h1,h2,h3,h4 {
    color:#f8fafc !important;
}

p,label {
    color:#d8e4ef;
}

.hero {
    padding:24px 28px;
    border-radius:20px;
    margin-bottom:20px;
    background:linear-gradient(
        115deg,
        rgba(8,47,73,.98),
        rgba(6,78,59,.92)
    );
    border:1px solid rgba(34,211,238,.30);
}

.hero-top {
    display:flex;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}

.hero-title {
    font-size:38px;
    font-weight:850;
    line-height:1;
}

.hero-sub {
    margin-top:9px;
    color:#d9fbff;
    font-size:15px;
}

.live {
    display:inline-flex;
    align-items:center;
    gap:7px;
    padding:5px 10px;
    border-radius:999px;
    background:rgba(34,211,238,.12);
    border:1px solid rgba(34,211,238,.28);
    color:#67e8f9;
    font-size:11px;
    font-weight:800;
}

.live-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:#34d399;
}

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(13,31,49,.95),
            rgba(9,23,38,.95)
        );
    border:1px solid #1c3a53;
    border-radius:15px;
    padding:12px;
}

div[data-testid="stMetricLabel"] {
    color:#9fb2c7 !important;
}

div[data-testid="stMetricValue"] {
    color:#f8fafc !important;
}

div.stButton > button {
    border-radius:11px;
    border:1px solid #16728a;
    background:
        linear-gradient(
            90deg,
            #075985,
            #0891b2
        );
    color:white;
    font-weight:750;
    min-height:42px;
}

div.stButton > button:hover {
    border-color:#67e8f9;
    background:
        linear-gradient(
            90deg,
            #036b88,
            #0e7490
        );
}

.map-card {
    background:rgba(7,18,31,.88);
    border:1px solid #1d3b54;
    border-radius:16px;
    padding:10px 12px;
    margin-top:8px;
}

.map-title {
    font-size:14px;
    font-weight:800;
    color:#dff9ff;
}

.map-subtitle {
    font-size:11px;
    color:#8298ad;
    margin-top:3px;
}

.location-card {
    background:
        linear-gradient(
            145deg,
            rgba(13,31,49,.94),
            rgba(8,20,34,.94)
        );
    border:1px solid #1d3b54;
    border-radius:13px;
    padding:12px 14px;
    margin:5px 0;
}

.location-name {
    color:#f8fafc;
    font-weight:800;
}

.location-meta {
    color:#8ea4b8;
    font-size:11px;
    margin-top:3px;
}

.legend-row {
    display:flex;
    align-items:center;
    gap:9px;
    margin:8px 0;
    color:#cbd5e1;
    font-size:13px;
}

.legend-dot {
    width:11px;
    height:11px;
    border-radius:50%;
    flex:0 0 auto;
}

.small-note {
    color:#7f95aa;
    font-size:11px;
    line-height:1.45;
}

.route-live {
    padding:8px 12px;
    border-radius:9px;
    margin:7px 0;
    background:rgba(6,78,59,.30);
    border:1px solid rgba(52,211,153,.35);
    color:#6ee7b7;
    font-size:12px;
    font-weight:750;
}

.route-fallback {
    padding:8px 12px;
    border-radius:9px;
    margin:7px 0;
    background:rgba(124,45,18,.30);
    border:1px solid rgba(251,146,60,.35);
    color:#fdba74;
    font-size:12px;
    font-weight:750;
}

.status-pill {
    display:inline-block;
    padding:3px 8px;
    border-radius:999px;
    font-size:10px;
    font-weight:800;
}

.status-open {
    background:rgba(52,211,153,.13);
    color:#6ee7b7;
}

.status-blocked {
    background:rgba(251,146,60,.14);
    color:#fdba74;
}
</style>
""")

# ============================================================
# SESSION STATE
# ============================================================

if "city" not in st.session_state:
    st.session_state.city = create_city_graph()

city = st.session_state.city

if "emergency_manager" not in st.session_state:
    st.session_state.emergency_manager = EmergencyManager()

emergency_manager = st.session_state.emergency_manager

if "route_result" not in st.session_state:
    st.session_state.route_result = None


# ============================================================
# REAL MAP COORDINATES
# ============================================================

LOCATION_COORDS = {
    "ISBT": [78.0436, 30.2850],
    "Railway Station": [78.0322, 30.3165],
    "Prem Nagar": [77.9570, 30.3540],
    "Ballupur": [78.0210, 30.3250],
    "Clock Tower": [78.0413, 30.3250],
    "Paltan Bazaar": [78.0340, 30.3180],
    "Dalanwala": [78.0570, 30.3300],
    "Rajpur Road": [78.0600, 30.3500],
    "Hospital": [78.0575, 30.3305],
    "Fire Station": [78.0180, 30.3280],
    "Police Station": [78.0350, 30.3200],
    "Pacific Mall": [78.0750, 30.3700],

    "DIT University": [78.07535, 30.39834],
    "Golden Manor": [78.07720, 30.39970],
    "Imperial Heights": [78.07973, 30.40142],
}


# ============================================================
# ENSURE NEW LOCATIONS EXIST IN GRAPH
# ============================================================

GRAPH_POSITIONS = {
    "DIT University": (8, 5),
    "Golden Manor": (8, 6),
    "Imperial Heights": (8, 7),
}

for name, position in GRAPH_POSITIONS.items():

    if name not in city:
        city.add_node(
            name,
            pos=position,
            kind="location"
        )

    elif "pos" not in city.nodes[name]:
        city.nodes[name]["pos"] = position


SIMULATED_LINKS = [
    ("Rajpur Road", "DIT University", 3.0),
    ("Pacific Mall", "DIT University", 3.15),
    ("DIT University", "Golden Manor", 2.0),
    ("Golden Manor", "Imperial Heights", 2.0),
    ("Imperial Heights", "Hospital", 4.0),
]

for a, b, distance in SIMULATED_LINKS:

    if not city.has_edge(a, b):

        city.add_edge(
            a,
            b,
            distance=distance,
            traffic=1.0,
            blocked=False
        )


# ============================================================
# LOCATION COLORS
# ============================================================

LOCATION_COLORS = {
    "Hospital": [239, 68, 68],
    "Fire Station": [249, 115, 22],
    "Police Station": [59, 130, 246],
    "Pacific Mall": [168, 85, 247],
    "Railway Station": [14, 165, 233],
    "ISBT": [20, 184, 166],
    "Clock Tower": [250, 204, 21],
    "DIT University": [99, 102, 241],
    "Golden Manor": [245, 158, 11],
    "Imperial Heights": [236, 72, 153],
}


# ============================================================
# SATELLITE TILES
# ============================================================

SATELLITE_TILES = (
    "https://server.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)


# ============================================================
# REAL ROAD ROUTING
# ============================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_road_geometry(route):

    if not route or len(route) < 2:
        return []

    geometry = []

    for start, end in zip(
        route[:-1],
        route[1:]
    ):

        if (
            start not in LOCATION_COORDS
            or end not in LOCATION_COORDS
        ):
            continue

        start_lon, start_lat = (
            LOCATION_COORDS[start]
        )

        end_lon, end_lat = (
            LOCATION_COORDS[end]
        )

        url = (
            "https://router.project-osrm.org/"
            "route/v1/driving/"
            f"{start_lon},{start_lat};"
            f"{end_lon},{end_lat}"
            "?overview=full"
            "&geometries=geojson"
            "&steps=false"
        )

        try:

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent":
                        "ResQ-AI-Emergency-Project"
                }
            )

            response.raise_for_status()

            data = response.json()

            if data.get("code") != "Ok":
                raise ValueError(
                    "OSRM returned no valid route"
                )

            routes = data.get(
                "routes",
                []
            )

            if not routes:
                raise ValueError(
                    "No road route returned"
                )

            segment = (
                routes[0]
                ["geometry"]
                ["coordinates"]
            )

            if geometry and segment:
                segment = segment[1:]

            geometry.extend(segment)

        except Exception as error:

            print(
                f"OSRM error: "
                f"{start} -> {end}: {error}"
            )

            # Fallback
            segment = [
                [start_lon, start_lat],
                [end_lon, end_lat]
            ]

            if geometry:
                segment = segment[1:]

            geometry.extend(segment)

    return geometry


# ============================================================
# MAP HELPERS
# ============================================================

def route_center(route):

    points = [
        LOCATION_COORDS[p]
        for p in route
        if p in LOCATION_COORDS
    ]

    if not points:
        return 78.0550, 30.3520, 12.0

    lon = sum(
        p[0] for p in points
    ) / len(points)

    lat = sum(
        p[1] for p in points
    ) / len(points)

    spread = max(
        max(p[0] for p in points)
        - min(p[0] for p in points),

        max(p[1] for p in points)
        - min(p[1] for p in points),
    )

    if spread > 0.07:
        zoom = 11.3

    elif spread > 0.04:
        zoom = 11.8

    elif spread > 0.02:
        zoom = 12.3

    else:
        zoom = 13.0

    return lon, lat, zoom


def location_rows():

    rows = []

    for name, coords in LOCATION_COORDS.items():

        rows.append(
            {
                "name": name,
                "longitude": coords[0],
                "latitude": coords[1],
                "color":
                    LOCATION_COLORS.get(
                        name,
                        [56, 189, 248]
                    ),
            }
        )

    return rows


# ============================================================
# SUBTLE 3D BUILDINGS
# ============================================================

BUILDINGS = [

    {
        "polygon": [
            [78.0378, 30.3282],
            [78.0390, 30.3282],
            [78.0390, 30.3294],
            [78.0378, 30.3294],
        ],
        "height": 28,
    },

    {
        "polygon": [
            [78.0438, 30.3312],
            [78.0450, 30.3312],
            [78.0450, 30.3324],
            [78.0438, 30.3324],
        ],
        "height": 42,
    },

    {
        "polygon": [
            [78.0500, 30.3270],
            [78.0513, 30.3270],
            [78.0513, 30.3283],
            [78.0500, 30.3283],
        ],
        "height": 24,
    },

    {
        "polygon": [
            [78.0550, 30.3340],
            [78.0565, 30.3340],
            [78.0565, 30.3354],
            [78.0550, 30.3354],
        ],
        "height": 36,
    },
]


# ============================================================
# MAP RENDERER
# ============================================================

def render_city_map(
    route=None,
    emergency_location=None,
    start_location=None,
    focus_location=None,
    map_mode="Satellite",
    show_3d=False,
):

    route = route or []

    route_points = [
        LOCATION_COORDS[p]
        for p in route
        if p in LOCATION_COORDS
    ]

    road_geometry = (
        get_road_geometry(route)
        if len(route_points) >= 2
        else []
    )

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    if focus_location in LOCATION_COORDS:

        center_lon, center_lat = (
            LOCATION_COORDS[
                focus_location
            ]
        )

        zoom = 13.3

    elif len(route_points) >= 2:

        center_lon, center_lat, zoom = (
            route_center(route)
        )

    else:

        center_lon = 78.0550
        center_lat = 30.3520
        zoom = 11.85


    layers = []


    # --------------------------------------------------------
    # SATELLITE BACKGROUND
    # --------------------------------------------------------

    if map_mode == "Satellite":

        layers.append(
            pdk.Layer(
                "TileLayer",
                data=SATELLITE_TILES,
                min_zoom=8,
                max_zoom=19,
                tile_size=256,
                opacity=0.94,
            )
        )


    # --------------------------------------------------------
    # 3D BUILDINGS
    # --------------------------------------------------------

    if show_3d:

        layers.append(
            pdk.Layer(
                "PolygonLayer",
                data=BUILDINGS,
                get_polygon="polygon",
                get_fill_color=[
                    24, 74, 96, 180
                ],
                get_line_color=[
                    102, 225, 245, 150
                ],
                get_elevation="height",
                extruded=True,
                wireframe=True,
                pickable=False,
            )
        )


    # --------------------------------------------------------
    # IMPORTANT LOCATIONS
    # --------------------------------------------------------

    points = location_rows()

    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=points,
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=110,
            radius_min_pixels=5,
            radius_max_pixels=11,
            stroked=True,
            get_line_color=[
                255, 255, 255, 245
            ],
            line_width_min_pixels=2,
            pickable=True,
            auto_highlight=True,
        )
    )


    # --------------------------------------------------------
    # LOCATION LABELS
    # --------------------------------------------------------

    layers.append(
        pdk.Layer(
            "TextLayer",
            data=points,
            get_position="[longitude, latitude]",
            get_text="name",
            get_size=15,
            get_color=[
                255, 255, 255, 255
            ],
            get_pixel_offset=[
                0, -18
            ],
            billboard=True,
            background=True,
            get_background_color=[
                3, 12, 22, 220
            ],
            background_padding=[
                5, 3
            ],
            pickable=True,
        )
    )


    # --------------------------------------------------------
    # SELECTED LOCATION
    # --------------------------------------------------------

    if focus_location in LOCATION_COORDS:

        lon, lat = (
            LOCATION_COORDS[
                focus_location
            ]
        )

        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=[
                    {
                        "longitude": lon,
                        "latitude": lat
                    }
                ],
                get_position=[
                    "longitude",
                    "latitude"
                ],
                get_radius=230,
                radius_min_pixels=12,
                radius_max_pixels=22,
                get_fill_color=[
                    255, 255, 255, 30
                ],
                get_line_color=[
                    255, 255, 255, 255
                ],
                line_width_min_pixels=3,
            )
        )


    # --------------------------------------------------------
    # ROAD-FOLLOWING RESCUE ROUTE
    # --------------------------------------------------------

    if len(route_points) >= 2:

        using_real_roads = (
            len(road_geometry) >= 2
        )

        visible_path = (
            road_geometry
            if using_real_roads
            else route_points
        )


        # Black outline
        layers.append(
            pdk.Layer(
                "PathLayer",
                data=[
                    {
                        "path":
                            visible_path
                    }
                ],
                get_path="path",
                get_color=[
                    3, 12, 22, 235
                ],
                width_min_pixels=10,
                pickable=False,
            )
        )


        # Cyan route
        layers.append(
            pdk.Layer(
                "PathLayer",
                data=[
                    {
                        "path":
                            visible_path
                    }
                ],
                get_path="path",
                get_color=[
                    34, 211, 238, 255
                ],
                width_min_pixels=5,
                pickable=True,
            )
        )


        # Route numbers
        route_rows = []

        for index, place in enumerate(
            route
        ):

            if place not in LOCATION_COORDS:
                continue

            route_rows.append(
                {
                    "step":
                        str(index + 1),

                    "longitude":
                        LOCATION_COORDS[
                            place
                        ][0],

                    "latitude":
                        LOCATION_COORDS[
                            place
                        ][1],
                }
            )


        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=route_rows,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_radius=75,
                radius_min_pixels=5,
                radius_max_pixels=9,
                get_fill_color=[
                    34, 211, 238, 255
                ],
                get_line_color=[
                    255, 255, 255, 255
                ],
                line_width_min_pixels=2,
            )
        )


        layers.append(
            pdk.Layer(
                "TextLayer",
                data=route_rows,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_text="step",
                get_size=12,
                get_color=[
                    0, 20, 30, 255
                ],
                billboard=True,
            )
        )


        if using_real_roads:

            st.html(
                """
                <div class="route-live">
                    🛣️ LIVE ROAD ROUTE —
                    The rescue path follows
                    the actual road network.
                </div>
                """
            )

        else:

            st.html(
                """
                <div class="route-fallback">
                    ⚠️ ROAD ROUTING UNAVAILABLE —
                    Showing the project graph route.
                </div>
                """
            )


    # --------------------------------------------------------
    # EMERGENCY MARKER
    # --------------------------------------------------------

    if (
        emergency_location
        in LOCATION_COORDS
    ):

        lon, lat = (
            LOCATION_COORDS[
                emergency_location
            ]
        )

        row = [
            {
                "longitude": lon,
                "latitude": lat,
                "name":
                    "🚨 EMERGENCY",
            }
        ]

        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=row,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_radius=240,
                radius_min_pixels=13,
                radius_max_pixels=23,
                get_fill_color=[
                    251, 75, 95, 255
                ],
                get_line_color=[
                    255, 255, 255, 255
                ],
                line_width_min_pixels=3,
                pickable=True,
            )
        )

        layers.append(
            pdk.Layer(
                "TextLayer",
                data=row,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_text="name",
                get_size=15,
                get_color=[
                    255, 255, 255, 255
                ],
                get_pixel_offset=[
                    0, -31
                ],
                billboard=True,
                background=True,
                get_background_color=[
                    111, 18, 31, 230
                ],
                background_padding=[
                    5, 3
                ],
            )
        )


    # --------------------------------------------------------
    # RESCUE VEHICLE
    # --------------------------------------------------------

    if start_location in LOCATION_COORDS:

        lon, lat = (
            LOCATION_COORDS[
                start_location
            ]
        )

        row = [
            {
                "longitude": lon,
                "latitude": lat,
                "name":
                    "🚑 RESCUE",
            }
        ]

        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=row,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_radius=200,
                radius_min_pixels=11,
                radius_max_pixels=19,
                get_fill_color=[
                    52, 211, 153, 255
                ],
                get_line_color=[
                    255, 255, 255, 255
                ],
                line_width_min_pixels=3,
                pickable=True,
            )
        )

        layers.append(
            pdk.Layer(
                "TextLayer",
                data=row,
                get_position=(
                    "[longitude, latitude]"
                ),
                get_text="name",
                get_size=14,
                get_color=[
                    255, 255, 255, 255
                ],
                get_pixel_offset=[
                    0, -28
                ],
                billboard=True,
                background=True,
                get_background_color=[
                    6, 78, 59, 230
                ],
                background_padding=[
                    5, 3
                ],
            )
        )


    # --------------------------------------------------------
    # MAP STYLE
    # --------------------------------------------------------

    if map_mode == "Clean Dark":

        map_style = (
            "https://basemaps.cartocdn.com/"
            "gl/dark-matter-nolabels-gl-style/"
            "style.json"
        )

    else:

        map_style = None


    # --------------------------------------------------------
    # DECK
    # --------------------------------------------------------

    deck = pdk.Deck(
        layers=layers,

        initial_view_state=pdk.ViewState(
            longitude=center_lon,
            latitude=center_lat,
            zoom=zoom,
            pitch=18 if show_3d else 0,
            bearing=0,
            min_zoom=11,
            max_zoom=17,
        ),

        map_style=map_style,

        tooltip={
            "html":
                "<b>{name}</b>",
            "style": {
                "backgroundColor":
                    "#071321",
                "color":
                    "#ffffff",
                "fontSize":
                    "13px",
            },
        },
    )


    # --------------------------------------------------------
    # MAP HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="map-card">

            <div class="map-title">
                📍 Dehradun Location Map
            </div>

            <div class="map-subtitle">
                Clean Dehradun view •
                important locations only •
                rescue routes follow real roads
                when available
            </div>

        </div>
        """
    )


    st.pydeck_chart(
        deck,
        use_container_width=True,
        height=500,
    )


    if map_mode == "Satellite":

        st.caption(
            "🛰️ Satellite imagery © Esri, "
            "Maxar, Earthstar Geographics, "
            "and the GIS community."
        )

    else:

        st.caption(
            "🗺️ Clean dark map • "
            "important project locations "
            "are highlighted."
        )


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-top">

            <div class="hero-title">
                🚑 ResQ AI
            </div>

            <div class="live">

                <span class="live-dot"></span>

                DEHRADUN LIVE COMMAND CENTER

            </div>

        </div>

        <div class="hero-sub">

            Intelligent Emergency Response •
            AI Pathfinding •
            Traffic Management •
            Rescue Dispatch

        </div>

    </div>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.html(
    """
    <div style="
        font-size:20px;
        font-weight:850;
        color:#f8fafc;
    ">
        🚨 ResQ AI
    </div>
    """
)

st.sidebar.html(
    """
    <div style="
        color:#8ea4b8;
        font-size:12px;
    ">
        Emergency Response & Rescue System
    </div>
    """
)

st.sidebar.divider()

module = st.sidebar.radio(
    "Navigation",
    [
        "3D City Dashboard",
        "Report Emergency",
        "Rescue Operations",
        "Traffic & Roads",
        "Emergency Records",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()

st.sidebar.markdown(
    "### 🗺️ Map View"
)

map_mode = st.sidebar.radio(
    "Map style",
    [
        "Satellite",
        "Clean Dark"
    ],
    label_visibility="collapsed",
)

show_3d = st.sidebar.toggle(
    "🏙️ Subtle 3D buildings",
    value=False,
)

st.sidebar.divider()

st.sidebar.markdown(
    "### 📍 Location Legend"
)

for color, label in [
    ("#38bdf8", "Important place"),
    ("#34d399", "Rescue vehicle"),
    ("#fb4b5f", "Emergency"),
    ("#22d3ee", "Active rescue route"),
]:

    st.sidebar.html(
        f"""
        <div class="legend-row">

            <span
                class="legend-dot"
                style="background:{color}">
            </span>

            {label}

        </div>
        """
    )

st.sidebar.html(
    """
    <div class="small-note">

        The full graph network is hidden
        from the map so Dehradun stays
        easy to read on a laptop.

    </div>
    """
)


# ============================================================
# DASHBOARD
# ============================================================

if module == "3D City Dashboard":

    st.title(
        "Dehradun Emergency Command Center"
    )

    st.caption(
        "A clean city view designed to make "
        "every important location easy to identify."
    )

    emergencies = (
        emergency_manager
        .get_all_emergencies()
    )

    total = len(emergencies)

    reported = sum(
        1
        for e in emergencies
        if e["status"] == "Reported"
    )

    assigned = sum(
        1
        for e in emergencies
        if e["status"] == "Assigned"
    )

    completed = sum(
        1
        for e in emergencies
        if e["status"] == "Completed"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🚨 Total",
        total
    )

    c2.metric(
        "⏳ Pending",
        reported
    )

    c3.metric(
        "🚑 Assigned",
        assigned
    )

    c4.metric(
        "✅ Completed",
        completed
    )

    dashboard_route = None
    dashboard_start = None
    dashboard_emergency = None

    if st.session_state.route_result:

        dashboard_route = (
            st.session_state
            .route_result
            .get("route")
        )

        if dashboard_route:

            dashboard_start = (
                dashboard_route[0]
            )

            dashboard_emergency = (
                dashboard_route[-1]
            )

    render_city_map(
        route=dashboard_route,
        emergency_location=
            dashboard_emergency,
        start_location=
            dashboard_start,
        map_mode=map_mode,
        show_3d=show_3d,
    )

    st.subheader(
        "📍 Dehradun Locations"
    )

    location_cols = st.columns(4)

    for index, name in enumerate(
        LOCATION_COORDS
    ):

        color = LOCATION_COLORS.get(
            name,
            [56, 189, 248]
        )

        color_hex = (
            "#%02x%02x%02x"
            % tuple(color)
        )

        with location_cols[
            index % 4
        ]:

            st.html(
                f"""
                <div class="location-card">

                    <div class="location-name">

                        <span
                            style="
                            color:{color_hex};
                            "
                        >
                            ●
                        </span>

                        {name}

                    </div>

                    <div class="location-meta">

                        Available for emergency
                        reporting and rescue
                        operations.

                    </div>

                </div>
                """
            )

    st.subheader(
        "Recent Emergency Reports"
    )

    if emergencies:

        for emergency in reversed(
            emergencies[-5:]
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"""
                    **{emergency['id']}
                    | {emergency['type']}**
                    """
                )

                st.write(
                    f"📍 {emergency['location']} | "
                    f"⚠️ {emergency['severity']} | "
                    f"Status: "
                    f"{emergency['status']}"
                )

                st.caption(
                    f"Reported at: "
                    f"{emergency['reported_at']}"
                )

    else:

        st.info(
            "No emergencies reported yet."
        )


# ============================================================
# REPORT EMERGENCY
# ============================================================

elif module == "Report Emergency":

    st.title(
        "🚨 Report Emergency"
    )

    st.caption(
        "Choose a Dehradun location. "
        "The map will automatically focus on it."
    )

    with st.form(
        "emergency_form"
    ):

        c1, c2 = st.columns(2)

        with c1:

            emergency_type = (
                st.selectbox(
                    "Emergency Type",
                    [
                        "Medical",
                        "Fire",
                        "Accident",
                        "Flood",
                        "Other",
                    ],
                )
            )

            location = (
                st.selectbox(
                    "Emergency Location",
                    list(city.nodes),
                )
            )

        with c2:

            severity = (
                st.selectbox(
                    "Severity",
                    [
                        "Critical",
                        "High",
                        "Medium",
                        "Low",
                    ],
                )
            )

            description = (
                st.text_area(
                    "Emergency Description",
                    placeholder=
                        "Describe what happened...",
                )
            )

        submitted = (
            st.form_submit_button(
                "🚨 Submit Emergency",
                use_container_width=True,
            )
        )

    if submitted:

        emergency_id = (
            emergency_manager
            .report_emergency(
                location,
                emergency_type,
                severity,
            )
        )

        emergency_manager.emergencies[
            emergency_id
        ]["description"] = description

        st.session_state.route_result = None

        st.success(
            f"Emergency {emergency_id} "
            "successfully reported!"
        )

    st.subheader(
        "📍 Selected Location"
    )

    render_city_map(
        emergency_location=location,
        focus_location=location,
        map_mode=map_mode,
        show_3d=show_3d,
    )


# ============================================================
# RESCUE OPERATIONS
# ============================================================

elif module == "Rescue Operations":

    st.title(
        "🚑 Rescue Dispatch & Pathfinding"
    )

    st.caption(
        "Calculate a route with your AI "
        "algorithm, then display it along "
        "the real road network."
    )

    emergencies = (
        emergency_manager
        .get_all_emergencies()
    )

    if not emergencies:

        st.warning(
            "No emergency available for rescue."
        )

        st.stop()

    emergency_ids = [
        e["id"]
        for e in emergencies
    ]

    selected_id = st.selectbox(
        "Select Emergency",
        emergency_ids,
    )

    emergency = next(
        e
        for e in emergencies
        if e["id"] == selected_id
    )

    destination = (
        emergency["location"]
    )

    st.markdown(
        f"""
        **Emergency:** {emergency['type']}
        &nbsp; | &nbsp;
        **Location:** {destination}
        &nbsp; | &nbsp;
        **Severity:** {emergency['severity']}
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        algorithm = st.selectbox(
            "Pathfinding Algorithm",
            [
                "A*",
                "Dijkstra",
                "BFS",
                "DFS",
            ],
        )

    with c2:

        mode = st.selectbox(
            "Route Optimization",
            [
                "distance",
                "time",
            ],
        )

    with c3:

        nodes = list(city.nodes)

        default_index = (
            nodes.index("Hospital")
            if "Hospital" in nodes
            else 0
        )

        start_location = (
            st.selectbox(
                "Rescue Vehicle Starting Location",
                nodes,
                index=default_index,
            )
        )

    if st.button(
        "🚑 Find Rescue Route",
        use_container_width=True,
    ):

        if start_location == destination:

            st.warning(
                "The rescue vehicle is already "
                "at the emergency location."
            )

        else:

            route, cost, explored = (
                find_route(
                    city,
                    start_location,
                    destination,
                    algorithm,
                    mode,
                )
            )

            if route:

                st.session_state.route_result = {

                    "emergency_id":
                        selected_id,

                    "algorithm":
                        algorithm,

                    "mode":
                        mode,

                    "route":
                        route,

                    "cost":
                        cost,

                    "explored":
                        explored,
                }

                emergency_manager.assign_emergency(
                    selected_id,
                    route,
                    destination,
                )

                st.success(
                    "Rescue route assigned. "
                    "The map now follows the "
                    "real road network when "
                    "routing data is available."
                )

            else:

                st.error(
                    "No available route. "
                    "Check whether roads are blocked."
                )

    result = (
        st.session_state
        .route_result
    )

    if (
        result
        and result["emergency_id"]
        == selected_id
    ):

        route = result["route"]

        a, b, c = st.columns(3)

        a.metric(
            "Algorithm",
            result["algorithm"]
        )

        b.metric(
            "Route Cost",
            f"{result['cost']:.2f}"
        )

        c.metric(
            "Nodes Explored",
            len(result["explored"])
        )

        st.markdown(
            f"""
            **🚑 Route:**
            {' → '.join(route)}
            """
        )

        render_city_map(
            route=route,
            emergency_location=
                destination,
            start_location=
                start_location,
            map_mode=map_mode,
            show_3d=show_3d,
        )

        st.subheader(
            "📍 Route Steps"
        )

        for index, place in enumerate(
            route
        ):

            if index == 0:

                st.write(
                    f"🚑 **START:** {place}"
                )

            elif index == len(route) - 1:

                st.write(
                    f"🚨 **EMERGENCY:** {place}"
                )

            else:

                st.write(
                    f"➡️ {index}. "
                    f"Continue to **{place}**"
                )

        if st.button(
            "✅ Mark Emergency as Completed",
            use_container_width=True,
        ):

            emergency_manager.update_status(
                selected_id,
                "Completed",
            )

            st.session_state.route_result = None

            st.success(
                "Emergency marked as completed."
            )

            st.rerun()

    else:

        render_city_map(
            emergency_location=
                destination,
            focus_location=
                destination,
            map_mode=map_mode,
            show_3d=show_3d,
        )


# ============================================================
# TRAFFIC & ROADS
# ============================================================

elif module == "Traffic & Roads":

    st.title(
        "🚦 Traffic & Road Management"
    )

    st.caption(
        "Traffic controls remain part of "
        "the project graph while the map "
        "stays visually clean."
    )

    roads = list(
        city.edges()
    )

    road_options = [
        f"{a} - {b}"
        for a, b in roads
    ]

    if not road_options:

        st.warning(
            "No roads available."
        )

        st.stop()

    selected_road = st.selectbox(
        "Select Road",
        road_options,
    )

    place1, place2 = (
        selected_road.split(
            " - "
        )
    )

    road_data = (
        city[place1][place2]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Distance",
        f"{road_data['distance']} km"
    )

    c2.metric(
        "Traffic Factor",
        road_data["traffic"]
    )

    c3.metric(
        "Status",
        (
            "BLOCKED"
            if road_data["blocked"]
            else "OPEN"
        )
    )

    traffic_factor = st.slider(
        "Set Traffic Factor",
        1.0,
        5.0,
        float(
            road_data["traffic"]
        ),
        0.5,
    )

    b1, b2 = st.columns(2)

    with b1:

        if st.button(
            "🔄 Update Traffic",
            use_container_width=True,
        ):

            update_traffic(
                city,
                place1,
                place2,
                traffic_factor,
            )

            st.success(
                "Traffic updated successfully."
            )

            st.rerun()

    with b2:

        if st.button(
            "🚧 Block / Open Road",
            use_container_width=True,
        ):

            if road_data["blocked"]:

                open_road(
                    city,
                    place1,
                    place2,
                )

                st.success(
                    "Road reopened."
                )

            else:

                close_road(
                    city,
                    place1,
                    place2,
                )

                st.success(
                    "Road blocked."
                )

            st.rerun()

    st.subheader(
        "🗺️ Location Overview"
    )

    render_city_map(
        map_mode=map_mode,
        show_3d=show_3d,
    )

    st.subheader(
        "All Road Conditions"
    )

    for road in get_road_status(
        city
    ):

        status_class = (
            "status-blocked"
            if road["Status"] != "Open"
            else "status-open"
        )

        st.html(
            f"""
            <div class="location-card">

                <div class="location-name">
                    {road["Road"]}
                </div>

                <div class="location-meta">

                    {road["Distance (km)"]} km
                    &nbsp; • &nbsp;

                    Traffic
                    {road["Traffic Factor"]}

                    &nbsp; • &nbsp;

                    <span
                        class="status-pill
                        {status_class}"
                    >
                        {road["Status"]}
                    </span>

                </div>

            </div>
            """
        )


# ============================================================
# EMERGENCY RECORDS
# ============================================================

elif module == "Emergency Records":

    st.title(
        "📋 Emergency Records"
    )

    st.caption(
        "Complete history of reported "
        "and dispatched emergencies."
    )

    emergencies = (
        emergency_manager
        .get_all_emergencies()
    )

    if not emergencies:

        st.info(
            "No emergency records available."
        )

    else:

        for emergency in reversed(
            emergencies
        ):

            with st.container(
                border=True
            ):

                st.subheader(
                    f"{emergency['id']} — "
                    f"{emergency['type']}"
                )

                st.write(
                    f"📍 **Location:** "
                    f"{emergency['location']}"
                )

                st.write(
                    f"⚠️ **Severity:** "
                    f"{emergency['severity']}"
                )

                st.write(
                    f"**Status:** "
                    f"{emergency['status']}"
                )

                st.caption(
                    f"Reported at: "
                    f"{emergency['reported_at']}"
                )

                if emergency.get(
                    "description"
                ):

                    st.write(
                        f"**Description:** "
                        f"{emergency['description']}"
                    )

                if emergency.get(
                    "route"
                ):

                    st.write(
                        "**Route:** "
                        + " → ".join(
                            emergency["route"]
                        )
                    )

                if emergency.get(
                    "rescue_center"
                ):

                    st.write(
                        f"**Rescue Centre:** "
                        f"{emergency['rescue_center']}"
                    )