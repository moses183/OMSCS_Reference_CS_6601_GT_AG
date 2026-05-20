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
    emp= PriorityQueue()
    if start==goal:
        return []
    explored = dict()
    frontier = PriorityQueue()
    pathier=PriorityQueue()
    frontier.append((0,start))
    pathier.append((0,[start]))

    while not frontier.__eq__(emp):


        cost,noi=frontier.pop()
        poi=pathier.pop()[1]


        if noi in explored and explored[noi]<=cost:
            continue

        if noi==goal:
            return poi
        ns=sorted(list(graph.neighbors(noi)))
        for n in ns:
            wt = graph.get_edge_weight(noi, n)
            addwt = wt + cost
            if n not in explored or explored[n]<=addwt:
                np=poi+[n]
                frontier.append((addwt,n))
                pathier.append((addwt,np))
        if noi not in explored:
            explored[noi]=cost



    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
