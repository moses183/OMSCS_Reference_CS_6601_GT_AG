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

    frontier=[start]
    pathier=[[start]]
    explored=set()

    while frontier:
        noi=frontier.pop(0)
        poi=pathier.pop(0)
        ns=sorted(list(graph.neighbors(noi)))
        for n in ns:
            if n ==goal :
                return poi+[n]
            if n not in frontier and n not in explored:
                frontier.append(n)
                pathier.append(poi+[n])
        if noi not in explored:
            explored.add(noi)









    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
