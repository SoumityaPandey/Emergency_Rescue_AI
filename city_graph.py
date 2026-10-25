import networkx as nx


def create_city_graph():

    graph = nx.Graph()

    locations = {
        "ISBT": (0, 0),
        "Railway Station": (2, 1),
        "Prem Nagar": (-3, 1),
        "Ballupur": (1, 3),
        "Clock Tower": (3, 3),
        "Paltan Bazaar": (4, 1),
        "Dalanwala": (5, 4),
        "Rajpur Road": (7, 3),
        "Hospital": (6, 6),
        "Fire Station": (2, 6),
        "Police Station": (0, 5),
        "Pacific Mall": (9, 1),
        "DIT University": (8, 5),
        "Golden Manor": (8, 6),
        "Imperial Heights": (8, 7)
    }

    for name, position in locations.items():

        graph.add_node(
            name,
            pos=position,
            kind=(
                "rescue"
                if name in [
                    "Hospital",
                    "Fire Station",
                    "Police Station"
                ]
                else "location"
            )
        )

    roads = [
        ("ISBT", "Railway Station", 3),
        ("ISBT", "Prem Nagar", 5),
        ("ISBT", "Police Station", 4),
        ("Railway Station", "Ballupur", 2),
        ("Railway Station", "Paltan Bazaar", 2),
        ("Ballupur", "Clock Tower", 2),
        ("Ballupur", "Fire Station", 4),
        ("Clock Tower", "Paltan Bazaar", 1),
        ("Clock Tower", "Dalanwala", 3),
        ("Clock Tower", "Hospital", 5),
        ("Paltan Bazaar", "Rajpur Road", 4),
        ("Dalanwala", "Rajpur Road", 2),
        ("Dalanwala", "Hospital", 3),
        ("Rajpur Road", "Pacific Mall", 4),
        ("Hospital", "Pacific Mall", 5),
        ("Prem Nagar", "Police Station", 5),
        ("Police Station", "Fire Station", 5),
        ("Fire Station", "Hospital", 3),
        ("Rajpur Road", "DIT University", 3),
        ("DIT University", "Golden Manor", 2),
        ("Golden Manor", "Imperial Heights", 2),
        ("Imperial Heights", "Hospital", 4)
    ]

    for a, b, distance in roads:

        graph.add_edge(
            a,
            b,
            distance=distance,
            traffic=1.0,
            blocked=False
        )

    return graph