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
    ux,uy=graph.nodes[u]['pos']
    vx,vy=graph.nodes[v]['pos']
    euc=((vx-ux)**2+(vy-uy)**2)**0.5
    return round(euc,3)
    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError

def gn(graph,path):
    i=0
    cost=0
    while i < len(path)-1:
        cost+=graph.get_edge_weight(path[i],path[i+1])
        i+=1
    return cost


def a_star(graph, start, goal, heuristic) -> list:
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
    emp = PriorityQueue()
    if start == goal:
        return []
    explored = dict()
    frontier = PriorityQueue()
    pathier = PriorityQueue()
    frontier.append((heuristic(graph,start,goal)+0, start))
    pathier.append((heuristic(graph,start,goal)+0, [start]))

    while not frontier.__eq__(emp):

        cost,noi=frontier.pop()
        poi=pathier.pop()[1]

        if noi in explored and explored[noi]<=cost:
            continue

        if noi==goal:
            return poi
        ns=sorted(list(graph.neighbors(noi)))
        for n in ns:
            np = poi + [n]
            addwt=gn(graph,np)+heuristic(graph,n,goal)
            if n not in explored or explored[n]<=addwt:
                frontier.append((addwt,n))
                pathier.append((addwt,np))
        if noi not in explored:
            explored[noi]=cost




    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
