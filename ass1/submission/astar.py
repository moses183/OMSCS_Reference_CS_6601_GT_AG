#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# astar.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math
from submission.priority_queue import PriorityQueue

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def null_heuristic(graph, u, v):
    """
    Null heuristic used as a base line.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        u: Key for the first node to calculate from.
        v: Key for the second node to calculate to.

    Returns:
        0
    """

    return 0


def euclidean_dist_heuristic(graph, u, v):
    """
    Warm-up exercise: Implement the euclidean distance heuristic.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        u: Key for the first node to calculate from.
        v: Key for the second node to calculate to.

    Returns:
        Euclidean distance between the u node and the v node
        Round the result to 3 decimal places (if applicable)
    """
    ux, uy = graph.nodes[u]['pos']
    vx, vy = graph.nodes[v]['pos']
    return round(math.hypot(vx - ux, vy - uy), 3)

def path_cost(graph, path):
    total_cost = 0
    for index in range(len(path) - 1):
        total_cost += graph.get_edge_weight(path[index], path[index + 1])
    return total_cost


def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic) -> list:
    """
    Warm-up exercise: Implement A* algorithm.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path via A* as a list from the start to the goal node (including both).
    """
    if start == goal:
        return []

    frontier = PriorityQueue()
    frontier.append((heuristic(graph, start, goal), (start, [start], 0)))

    best_cost = {start: 0}
    explored = set()

    while frontier.size() > 0:
        _, (current_node, current_path, path_cost_so_far) = frontier.pop()

        if current_node in explored:
            continue
        if path_cost_so_far > best_cost.get(current_node, float('inf')):
            continue

        if current_node == goal:
            return current_path

        explored.add(current_node)

        for neighbor in sorted(graph.neighbors(current_node)):
            if neighbor in explored:
                continue

            new_cost = path_cost_so_far + graph.get_edge_weight(current_node, neighbor)
            if new_cost < best_cost.get(neighbor, float('inf')):
                best_cost[neighbor] = new_cost
                priority = new_cost + heuristic(graph, neighbor, goal)
                frontier.append((priority, (neighbor, current_path + [neighbor], new_cost)))

    return []
