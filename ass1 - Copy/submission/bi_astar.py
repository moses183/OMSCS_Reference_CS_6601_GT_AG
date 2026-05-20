#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# bi_astar.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math


from submission.priority_queue import PriorityQueue
from submission.astar import euclidean_dist_heuristic

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def null_heuristic(graph, u, v):

    return 0

def gn(graph,path):
    i=0
    cost=0
    while i < len(path)-1:
        cost+=graph.get_edge_weight(path[i],path[i+1])
        i+=1
    return cost


def euclidean_dist_heuristic(graph, u, v):

    ux,uy=graph.nodes[u]['pos']
    vx,vy=graph.nodes[v]['pos']
    euc=((vx-ux)**2+(vy-uy)**2)**0.5
    return round(euc,3)

def prn(graph,path,u,v,eps,heuristic=euclidean_dist_heuristic):
    hn=heuristic(graph,u,v)
    pgn=gn(graph,path)
    fn=hn+pgn
    return max(fn,((2*pgn)+eps))

def bidirectional_a_star(graph, start, goal, heuristic=euclidean_dist_heuristic) -> list:
    """
    Exercise 2: Bidirectional A*.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path via bi-A* as a list from the start to the goal node (including both).
    """
    emp = PriorityQueue()
    if start == goal:
        return []
    eps=float("inf")
    for e in graph.edges:
        eps=min(eps,graph.get_edge_weight(e[0],e[1]))
    path=[]

    fexplored = dict()
    ffrontier = PriorityQueue()
    fpathier = PriorityQueue()
    fprn=prn(graph,path,start,goal,eps,heuristic)
    ffrontier.append((fprn, start))
    fpathier.append((fprn, [start]))
    f_front_paths = {start: [start]}

    rexplored = dict()
    rfrontier = PriorityQueue()
    rpathier = PriorityQueue()
    rprn=prn(graph,path,goal,start,eps,heuristic)
    rfrontier.append((rprn, goal))
    rpathier.append((rprn, [goal]))
    r_front_paths = {goal: [goal]}

    U = float('inf')
    Upath = []

    while not ffrontier.__eq__(emp) and not rfrontier.__eq__(emp):

        #print("F "+ffrontier.__str__())
        #print("R "+rfrontier.__str__())
        #print("U"+str(Upath))



        fcost, fnoi = ffrontier.top()
        fpoi = fpathier.top()[1]

        rcost, rnoi = rfrontier.top()
        rpoi = rpathier.top()[1]

        mincost = min(fcost, rcost)

        fgn=gn(graph,fpoi)
        rgn=gn(graph,rpoi)

        ffn=heuristic(graph,fnoi,goal)+fgn
        rfn=heuristic(graph,rnoi,start)+rgn

        if U <= max(mincost,ffn,rfn,(fgn+rgn+eps)):
            return Upath

        if mincost == fcost:
            fcost, fnoi = ffrontier.pop()
            fpoi = fpathier.pop()[1]
            fns = sorted(list(graph.neighbors(fnoi)))

            if fnoi in rexplored.keys():
                continue

            if rfrontier.__contains__(fnoi):
                rfrontier.remove(rfrontier.ele(fnoi))

            fexplored[fnoi] = (fcost, fpoi)

            for n in fns:
                np = fpoi + [n]
                nc = prn(graph,np,n,goal,eps,heuristic)
                if (n in fexplored.keys() and fexplored[n][0] <= nc) or (ffrontier.__contains__(n) and ffrontier.ele(n)[0]<=nc): #gn(graph,f_front_paths[n]) <= gn(graph, np) ):
                    continue

                if rfrontier.__contains__(n):
                    rn = rfrontier.ele(n)
                    p2 = r_front_paths[rn[1]]
                    gcomp = gn(graph, np) + gn(graph, p2)
                    U = min(U, gcomp)
                    if gcomp == U:
                        Upath = list(np) + list(r_front_paths[rn[1]][1:])

                ffrontier.append((nc, n))
                fpathier.append((nc, np))
                f_front_paths[n] = np

        if mincost == rcost:
            rcost, rnoi = rfrontier.pop()
            rpoi = rpathier.pop()[1]

            rns = sorted(list(graph.neighbors(rnoi)))

            if rnoi in fexplored.keys():
                continue

            if ffrontier.__contains__(rnoi):
                ffrontier.remove(ffrontier.ele(rnoi))

            rexplored[rnoi] = (rcost, rpoi)
            for n in rns:
                np = [n] + rpoi
                nc = prn(graph,np,n,start,eps,heuristic)
                if (n in rexplored.keys() and rexplored[n][0] <= nc) or (rfrontier.__contains__(n) and rfrontier.ele(n)[0]<=nc): # gn(graph,r_front_paths[n]) <= gn(graph, np) ):
                    continue

                if ffrontier.__contains__(n):
                    fn = ffrontier.ele(n)
                    p2=f_front_paths[fn[1]]
                    gcomp=gn(graph,np)+gn(graph,p2)
                    U = min(U, gcomp)
                    if gcomp == U:
                        Upath = list(f_front_paths[fn[1]]) + list(np[1:])

                rfrontier.append((nc, n))
                rpathier.append((nc, np))
                r_front_paths[n] = np

    # TODO: finish this function!͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
