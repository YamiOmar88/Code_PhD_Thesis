# ======================================================================
# ======================================================================
# Depth-First Search
# ======================================================================
# ======================================================================

# NOTES: You call dfs(G, u, myOrder) where:
# - G is a dictionary with nodes as keys and adjacency-lists as values.
# - u has default value None, but can be any node from which you desire
#   to start exploring the graph.
# - myOrder is a list with a specific order of the nodes to be visited.


def dfs(G, u = None, myOrder = None, returnTrees = False):
    gP = {x: {'visited': None, 'predecesor': None, 'd': None, 'f': None} for x in G.keys()}
    time = 0
    myNodes = G.keys()
    if u != None:
        myNodes.remove(u)
        myNodes = [u] + myNodes
    elif myOrder != None:
        myNodes = myOrder
    myTrees = []
    for u in myNodes:
        if gP[u]['visited'] == None:
            gP, time, myTrees = dfs_visit(G, u, gP, time, myTrees)
    if not returnTrees:
        return gP
    else:
        return gP, myTrees


def dfs_visit(G, u, gP, time, myTrees):
    time = time + 1
    gP[u]['d'] = time
    gP[u]['visited'] = 0
    S, tree = [], []
    S.append(u)
    tree.append(u)
    while len(S) > 0:
        u = S.pop()
        gCount = 0
        for v in G[u]:
            if gP[v]['visited'] == None:
                gP[v]['predecesor'] = u
                time = time + 1
                gP[v]['d'] = time
                gP[v]['visited'] = 0
                S.append(v)
                tree.append(v)
                break
            else:
                gCount = gCount + 1
        if gCount == len(G[u]):
            gP[u]['visited'] = 1
            time = time + 1
            gP[u]['f'] = time
            if gP[u]['predecesor'] != None:
                aux = gP[u]['predecesor']
                S.append(aux)
    myTrees.append(tree)
    return gP, time, myTrees


# The adjacency list function takes a list of tuples (edges) and creates
# the correpsonding adjacency-list dictionary.
def adjacency_list(E):
    d = {}
    for e in E:
        t, h = e[0], e[1]
        d[t] = d.get(t, []) + [h]
        d[h] = d.get(h, [])
    for k  in d.keys():
        d[k] = set(d[k])
    return d


# ======================================================================
# ======================================================================
# Strongly Connected Components
# ======================================================================
# ======================================================================

# Calculate the TRANSPOSE OF G (G with its edges reversed)
def Grev(G):
    Gt = dict.fromkeys(G.keys(), [])
    for k in G.keys():
        for v in G[k]:
            Gt[v] = Gt.get(v, []) + [k]
    return Gt


# Order the nodes in decreasing order of u.f
def f_order(gP):
    myList = []
    for k in gP.keys():
        aux = (gP[k]['f'], k)
        myList.append(aux)
    myList.sort(reverse = True)
    result = [b for a,b in myList]
    return result

# Strongly Connected Components
def scc(G):
    myGp = dfs(G)
    nodeOrder = f_order(myGp)
    Gt = Grev(G)
    myGp, trees = dfs(Gt, myOrder = nodeOrder, returnTrees = True)
    return trees
