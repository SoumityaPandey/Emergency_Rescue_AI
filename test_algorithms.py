from city_graph import create_city_graph
from algorithms import find_route


city = create_city_graph()

start = "ISBT"
goal = "Hospital"

path, cost, explored = find_route(
    city,
    start,
    goal,
    "Dijkstra",
    "distance"
)

print("Starting Location:", start)
print("Destination:", goal)

if path:

    print("Selected Route:")
    print(" -> ".join(path))

    print("Total Distance:", round(cost, 2), "km")

else:

    print("No route available")

print("Nodes Explored:", len(explored))