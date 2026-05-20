#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# bfs.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def return_your_name() -> str:
    """Return your first and last name from this function as a string"""
    return "Aarushi Gajri"
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError


def breadth_first_search(graph, start, goal) -> list:
    """
    Warm-up exercise: Implement breadth-first-search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.

    Returns:
        The best path via BFS as a list from the start to the goal node (including both).
    """
    if start == goal:
        return []

    frontier = [(start, [start])]
    visited = {start}
    next_index = 0

    while next_index < len(frontier):
        current_node, current_path = frontier[next_index]
        next_index += 1

        for neighbor in sorted(graph.neighbors(current_node)):
            if neighbor == goal:
                return current_path + [neighbor]

            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append((neighbor, current_path + [neighbor]))

    return []
