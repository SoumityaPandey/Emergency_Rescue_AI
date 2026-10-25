def update_traffic(graph, a, b, traffic_factor):

    if graph.has_edge(a, b):
        graph[a][b]["traffic"] = traffic_factor
        return True

    return False


def close_road(graph, a, b):

    if graph.has_edge(a, b):
        graph[a][b]["blocked"] = True
        return True

    return False


def open_road(graph, a, b):

    if graph.has_edge(a, b):
        graph[a][b]["blocked"] = False
        return True

    return False


def get_road_status(graph):

    roads = []

    for a, b, data in graph.edges(data=True):

        roads.append({
            "Road": f"{a} - {b}",
            "Distance (km)": data["distance"],
            "Traffic Factor": data["traffic"],
            "Status": "Closed"
            if data["blocked"]
            else "Open"
        })

    return roads