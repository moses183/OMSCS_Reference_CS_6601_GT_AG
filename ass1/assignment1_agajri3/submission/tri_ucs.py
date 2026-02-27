#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# tri_ucs.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math
from submission.priority_queue import PriorityQueue

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃ https://idm-lab.org/bib/abstracts/papers/ijcai20a.pdf
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def gn(graph,path):
    i=0
    cost=0
    while i < len(path)-1:
        cost+=graph.get_edge_weight(path[i],path[i+1])
        i+=1
    return cost

def tridirectional_search(graph, goals) -> list:
    """
    Exercise 3: Tridirectional UCS Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    emp = PriorityQueue()
    pqs=dict()
    pathqs=dict()
    U=dict()
    Upath=dict()
    exp=dict()
    finpath=[]
    expall=dict()

    gtemp=goals.copy()

    st1 = ''.join(sorted(goals[0] + goals[1]))
    st2 = ''.join(sorted(goals[1] + goals[2]))
    st3 = ''.join(sorted(goals[0] + goals[2]))


    if len(set(goals))==2:
        l=list(set(goals))
        st=''.join(sorted(l[0]+l[1]))
        U[st]=float('inf')

    else:

        U[st1]=float('inf')
        U[st2]=float('inf')
        U[st3]=float('inf')




    for g in goals:

        pqs[g]=PriorityQueue()
        pathqs[g]=PriorityQueue()
        pqs[g].append((0,g))
        pathqs[g].append((0,[g]))
        exp[g]=dict()

    print("G "+str(goals))
    while any(not pq.__eq__(emp) for pq in pqs.values()):

        '''
        if U[st1] != float('inf') and U[st2] != float('inf') and goals[1] in gtemp:
            gtemp.remove(goals[1])
        if U[st2] != float('inf') and U[st3] != float('inf') and goals[2] in gtemp:
            gtemp.remove(goals[2])
        if U[st1] != float('inf') and U[st3] != float('inf') and goals[0] in gtemp:
            gtemp.remove(goals[0])
        '''

        for g in gtemp:
            #print(g)
            #print(pqs[g].__str__())
            if pqs[g].__eq__(emp):
                break
            cost,noi=pqs[g].pop()
            _,poi=pathqs[g].pop()



            if noi in goals and noi != g:
                st=''.join(sorted(noi+poi[0]))
                U[st]=min(U[st],cost)
                if U[st]==cost:
                    Upath[st]=(poi,st)
                    #print("Greach")
                    #print(poi)]

            if noi in expall.keys() and expall[noi][1]!=poi[0]:
                newp=poi+expall[noi][0][::-1][1:]
                cost2=gn(graph,newp)
                st = ''.join(sorted(poi[0] + expall[noi][1]))
                U[st] = min(U[st], cost2)
                if U[st] == cost2:

                    Upath[st] = (newp, st)
                    #print("Ireach")
                    #print(newp)


            #if noi in exp[g].keys() and exp[g][noi]<=cost:
            #    continue



            ns = sorted(list(graph.neighbors(noi)))
            exp[g][noi] = cost
            if noi not in expall.keys() or expall[noi][2]>cost :
                expall[noi]=[poi,poi[0],cost]
            for n in ns:
                np=poi+[n]
                nc=gn(graph,np)

                if pqs[g].__contains__(n) and pqs[g].ele(n)[0]>nc :
                    pqs[g].remove(pqs[g].ele(n))


                if n not in exp[g].keys() and (not pqs[g].__contains__(n)) or (n in exp[g].keys() and exp[g][n]>=nc):
                    pqs[g].append((nc,n))
                    pathqs[g].append((nc,np))
                #if n in exp[g].keys() and exp[g][n]<=nc:
                #    pqs[g].append((nc, n))
                 #   pathqs[g].append((nc, np))



        while all(uval!=float('inf') for uval in U.values()):


            p=PriorityQueue()
            sts=[st1,st2,st3]

            p1=Upath[sts[0]][0]
            p2=Upath[sts[1]][0]
            p3=Upath[sts[2]][0]
            p1rev=p1[::-1]
            p2rev=p2[::-1]
            p3rev=p3[::-1]

            #print(p1)
            #print(p2)
            #print(p3)

            if all(x in p1 for x in goals):
                pcost=gn(graph,p1)
                p.append((pcost,p1))
            if all(x in p2 for x in goals):
                pcost=gn(graph,p2)
                p.append((pcost,p2))
            if all(x in p3 for x in goals):
                pcost=gn(graph,p3)
                p.append((pcost,p3))
            if p1[-1]==p2[0]:

                c1=p1+p2[1:]
                pcost=gn(graph,c1)
                p.append((pcost,c1))

            if p1[0]==p2[-1]:

                c1=p2+p1[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))
            if p1[-1]==p3[0]:

                c1=p1+p3[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))
            if p1[0]==p3[-1]:

                c1=p3+p1[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))
            if p2[-1]==p3[0]:

                c1=p2+p3[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))
            if p2[0]==p3[-1]:
                c1=p3+p2[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p1[0]==p2[0]:
                c1=p1rev+p2[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p3[0]==p2[0]:
                c1=p3rev+p2[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p1[0]==p3[0]:
                c1=p1rev+p3[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p1[-1]==p2[-1]:
                #print(p1[-1]+" "+p2[-1])
                c1=p1+p2rev[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p3[-1]==p2[-1]:
                c1=p3+p2rev[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            if p1[-1]==p3[-1]:
                c1=p1+p3rev[1:]
                pcost = gn(graph, c1)
                p.append((pcost,c1))

            #print(p.pq_as_list())

            return p.top()[1]




    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError


