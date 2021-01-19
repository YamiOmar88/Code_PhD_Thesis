# Code for PhD Thesis
# Functions to calculate the Betweenness Centrality
# Yamila Mariel Omar
# Date of original code: August 2017
# Date of code last modification: 19th January 2021


'''The code to calculate the betweenness centrality is based on the algorithms
of Ulrik Brandes. The user must call the function

bC(V, E, weighted=False, normalized=False, directed=True)}

with the following input variables:
    1. V is a list of nodes.
    2. E is a dictionary with edges as keys, and weights as values (for
       unweighted graphs, w = 1 for all w). Weights are interpreted as follows:
       higher values indicate stronger ties.
    3. normalized is a boolean variable that indicates whether output values
       should be normalized. This variable is False by default.
    4. directed is a boolean variable that indicates whether the graph is
       directed. This variable is True by default.

The function returns a dictionary that contains each node as key and its
betweenness centrality as value.'''



def adj(u, E, directed):
    adjNodes = []
    for e in E:
        if e[0] == u:
            adjNodes.append(e[1])
        elif (not directed) and (e[1] == u):
            adjNodes.append(e[0])
    adjNodes = set(adjNodes)
    return adjNodes


def bC(V, E, weighted=False, normalized=False, directed=True):
    betCen = dict.fromkeys(V, 0)
    Q, S = ([], [])
    for s in V:
        # Initialization
        pred = dict.fromkeys(V, [])
        dist = dict.fromkeys(V, float('inf'))
        sigma = dict.fromkeys(V, 0)
        dist[s] = 0
        sigma[s] = 1
        Q.append(s)

        while len(Q) > 0:
            v = Q.pop(0)
            S.append(v)
            adj_v = adj(v, E.keys(), directed)
            for w in adj_v:
                # Path discovery: is w found for the first time?
                if dist[w] == float('inf'):
                    dist[w] = dist[v] + 1
                    Q.append(w)

                # Path counting: is the edge (v,w) on a shortest path?
                if dist[w] == dist[v] + 1:
                    if weighted:
                        sigma[w] = sigma[w] + E[(v,w)]*sigma[v]
                    else:
                        sigma[w] = sigma[w] + sigma[v]
                    pred[w] = pred[w] + [v]

        # Accumulation
        dependency = dict.fromkeys(V, 0)
        while len(S) > 0:
            w = S.pop()
            for v in pred[w]:
                if weighted:
                    dependency[v] = dependency[v] + E[(v,w)]*(sigma[v]/float(sigma[w])) * (1 + dependency[w])
                else:
                    dependency[v] = dependency[v] + (sigma[v]/float(sigma[w])) * (1 + dependency[w])
            if w != s:
                betCen[w] = betCen[w] + dependency[w]

    # If graph is undirected, the algorithm gives a BC that is doubled
    if directed == False:
        for k,v in betCen.items():
            betCen[k] = float(v) / 2.0

    # Normalization
    if normalized == True:
        n = len(V)
        for k,v in betCen.items():
            if directed == True:
                betCen[k] = float(v) / ((n-1)*(n-2))
            else:
                betCen[k] = 2 * float(v) / ((n-1)*(n-2))

    return betCen
