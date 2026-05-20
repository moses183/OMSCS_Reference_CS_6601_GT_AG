#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# bi_ucs.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math
from submission.priority_queue import PriorityQueue

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
def gn(graph,path):
    i=0
    cost=0
    while i < len(path)-1:
        cost+=graph.get_edge_weight(path[i],path[i+1])
        i+=1
    return cost


def bidirectional_ucs(graph, start, goal) -> list:
    """
    Exercise 1: Bidirectional Search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.

    Returns:
        The best path via bi-UCS as a list from the start to the goal node (including both).
    """
    emp = PriorityQueue()
    if start == goal:
        return []

    fexplored = dict()
    ffrontier = PriorityQueue()
    fpathier = PriorityQueue()
    ffrontier.append((0, start))
    fpathier.append((0, [start]))
    f_front_paths={start:[start]}

    rexplored = dict()
    rfrontier = PriorityQueue()
    rpathier = PriorityQueue()
    rfrontier.append((0, goal))
    rpathier.append((0, [goal]))
    r_front_paths = {goal: [goal]}

    U=float('inf')## infinite path cost
    Upath=[]

    while not ffrontier.__eq__(emp) and not rfrontier.__eq__(emp):

        fcost,fnoi=ffrontier.top()
        fpoi=fpathier.top()[1]


        rcost, rnoi = rfrontier.top()
        rpoi = rpathier.top()[1]


        mincost=min(fcost,rcost)

        if U <= (rcost+fcost):
            return Upath
        if mincost==fcost:
            fcost, fnoi = ffrontier.pop()
            fpoi = fpathier.pop()[1]
            fns = sorted(list(graph.neighbors(fnoi)))

            if fnoi in rexplored.keys():
                continue

            if rfrontier.__contains__(fnoi):
                rfrontier.remove(rfrontier.ele(fnoi))

            fexplored[fnoi] = (fcost,fpoi)

            for n in fns:
                np=fpoi+[n]
                nc=gn(graph,np)
                if (n in fexplored.keys() and fexplored[n][0]<=nc) or (ffrontier.__contains__(n) and ffrontier.ele(n)[0]<=nc):
                    continue


                if rfrontier.__contains__(n):
                    rn=rfrontier.ele(n)
                    U=min(U,nc+rn[0])
                    if nc+rn[0]==U:
                        Upath=list(np)+list(r_front_paths[rn[1]][1:])


                ffrontier.append((nc,n))
                fpathier.append((nc,np))
                f_front_paths[n]=np


        if mincost==rcost:
            rcost, rnoi = rfrontier.pop()
            rpoi = rpathier.pop()[1]

            rns = sorted(list(graph.neighbors(rnoi)))

            if rnoi in fexplored.keys():
                continue

            if ffrontier.__contains__(rnoi):

                ffrontier.remove(ffrontier.ele(rnoi))

            rexplored[rnoi] = (rcost,rpoi)
            for n in rns:
                np=[n]+rpoi
                nc=gn(graph,np)
                if (n in rexplored.keys() and rexplored[n][0]<=nc) or (rfrontier.__contains__(n) and rfrontier.ele(n)[0]<=nc):
                    continue

                if ffrontier.__contains__(n):
                    fn=ffrontier.ele(n)
                    U=min(U,nc+fn[0])
                    if nc+fn[0]==U:
                        Upath=list(f_front_paths[fn[1]])+list(np[1:])


                rfrontier.append((nc,n))
                rpathier.append((nc,np))
                r_front_paths[n] = np



























    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
