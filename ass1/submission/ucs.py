#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# ucs.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math
from submission.priority_queue import PriorityQueue

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def uniform_cost_search(graph, start, goal) -> list:
    """
    Warm-up exercise: Implement uniform_cost_search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.

    Returns:
        The best path via UCS as a list from the start to the goal node (including both).
    """
    if start == goal:
        return []

    frontier = PriorityQueue()
    frontier.append((0, (start, [start], 0)))

    best_cost = {start: 0}
    explored = set()

    while frontier.size() > 0:
        _, (current_node, current_path, path_cost) = frontier.pop()

        if current_node in explored:
            continue
        if path_cost > best_cost.get(current_node, float('inf')):
            continue

        if current_node == goal:
            return current_path

        explored.add(current_node)

        for neighbor in sorted(graph.neighbors(current_node)):
            if neighbor in explored:
                continue

            new_cost = path_cost + graph.get_edge_weight(current_node, neighbor)
            if new_cost < best_cost.get(neighbor, float('inf')):
                best_cost[neighbor] = new_cost
                frontier.append((new_cost, (neighbor, current_path + [neighbor], new_cost)))

    return []
