import heapq
import math
from collections import deque


def get_neighbors(graph, node):
    return [
        neighbor
        for neighbor in graph.neighbors(node)
        if not graph[node][neighbor]["blocked"]
    ]


def road_cost(graph, a, b, mode="distance"):
    road = graph[a][b]

    if road["blocked"]:
        return float("inf")

    if mode == "time":
        return road["distance"] * road["traffic"]

    return road["distance"]


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    explored = []

    while queue:
        node, path = queue.popleft()
        explored.append(node)

        if node == goal:
            cost = sum(
                road_cost(graph, path[i], path[i + 1], "distance")
                for i in range(len(path) - 1)
            )
            return path, cost, explored

        for neighbor in get_neighbors(graph, node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(
                    (neighbor, path + [neighbor])
                )

    return [], 0, explored


def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    explored = []

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        explored.append(node)

        if node == goal:
            cost = sum(
                road_cost(graph, path[i], path[i + 1], "distance")
                for i in range(len(path) - 1)
            )
            return path, cost, explored

        for neighbor in reversed(get_neighbors(graph, node)):
            if neighbor not in visited:
                stack.append(
                    (neighbor, path + [neighbor])
                )

    return [], 0, explored


def dijkstra(graph, start, goal, mode="distance"):
    priority_queue = [(0, start, [start])]
    best_cost = {start: 0}
    explored = []

    while priority_queue:

        cost, node, path = heapq.heappop(
            priority_queue
        )

        if cost > best_cost.get(
            node,
            float("inf")
        ):
            continue

        explored.append(node)

        if node == goal:
            return path, cost, explored

        for neighbor in get_neighbors(graph, node):

            new_cost = (
                cost
                + road_cost(
                    graph,
                    node,
                    neighbor,
                    mode
                )
            )

            if new_cost < best_cost.get(
                neighbor,
                float("inf")
            ):

                best_cost[neighbor] = new_cost

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return [], 0, explored


def heuristic(graph, a, b):
    """
    Calculate Euclidean distance between
    two graph nodes.

    Uses the node's 'pos' attribute.
    """

    if "pos" not in graph.nodes[a] or "pos" not in graph.nodes[b]:
        return 0

    x1, y1 = graph.nodes[a]["pos"]
    x2, y2 = graph.nodes[b]["pos"]

    return math.sqrt(
        (x1 - x2) ** 2
        + (y1 - y2) ** 2
    )


def astar(graph, start, goal, mode="distance"):
    priority_queue = [
        (
            heuristic(graph, start, goal),
            0,
            start,
            [start]
        )
    ]

    best_cost = {start: 0}
    explored = []

    while priority_queue:

        _, cost, node, path = heapq.heappop(
            priority_queue
        )

        if cost > best_cost.get(
            node,
            float("inf")
        ):
            continue

        explored.append(node)

        if node == goal:
            return path, cost, explored

        for neighbor in get_neighbors(graph, node):

            new_cost = (
                cost
                + road_cost(
                    graph,
                    node,
                    neighbor,
                    mode
                )
            )

            if new_cost < best_cost.get(
                neighbor,
                float("inf")
            ):

                best_cost[neighbor] = new_cost

                priority = (
                    new_cost
                    + heuristic(
                        graph,
                        neighbor,
                        goal
                    )
                )

                heapq.heappush(
                    priority_queue,
                    (
                        priority,
                        new_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return [], 0, explored


def find_route(
    graph,
    start,
    goal,
    algorithm,
    mode="distance"
):

    if algorithm == "BFS":
        return bfs(graph, start, goal)

    if algorithm == "DFS":
        return dfs(graph, start, goal)

    if algorithm == "Dijkstra":
        return dijkstra(
            graph,
            start,
            goal,
            mode
        )

    if algorithm == "A*":
        return astar(
            graph,
            start,
            goal,
            mode
        )

    return [], 0, []