from city_graph import create_city_graph
from algorithms import find_route


city = create_city_graph()

start = "ISBT"
goal = "Hospital"
mode = "distance"

algorithms = [
    "BFS",
    "DFS",
    "Dijkstra",
    "A*"
]

print("Algorithm Comparison")

for algorithm in algorithms:

    path, cost, explored = find_route(
        city,
        start,
        goal,
        algorithm,
        mode
    )

    print("\nAlgorithm:", algorithm)

    if path:

        print(
            "Route:",
            " -> ".join(path)
        )

        print(
            "Distance:",
            round(cost, 2),
            "km"
        )

        print(
            "Nodes Explored:",
            len(explored)
        )

    else:

        print("No route available")