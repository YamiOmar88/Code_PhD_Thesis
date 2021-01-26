# ======================================================================
# ======================================================================
# Page Rank Algorithm
# ======================================================================
# ======================================================================

def make_transition_matrix(E, nodes):
    '''Internal function to calculate the transition matrix.
    Input variables:
        - E: dictionary with edges as keys and weight as value.
        - nodes: list of nodes.

    Output variables:
        - matrix: dictionary corresponding to the transition matrix.
    '''
    colSum = {}
    for n in nodes:
        colSum[n] = 0
        for m in nodes:
            colSum[n] = colSum[n] + E.get((n, m), 0)

    matrix = {}
    for k in E.keys():
        matrix[k] = E[k] / float( colSum[k[0]] )

    return matrix




def pagerank(E, nodes, start_nodes=None, B=0.85):
    '''Function allowing to calculate the PageRank algorithm.
    Input variables:
        - E: dictionary with edges as keys and weight as value.
        - nodes: list of nodes.
        - start_nodes: (default=None) dictionary of nodes with their starting
                       fraction.
        - B: (default=0.85) taxation value, typically between 0.8 and 0.9.

    Output variables:
        - vp
    '''
    nodes.sort()
    M = make_transition_matrix(E, nodes)

    if start_nodes == None:
        e = {n: 1/len(nodes) for n in nodes}
    else:
        e = start_nodes

    v = {k: 1/len(nodes) for k in nodes}

    vp = {k: 0 for k in nodes}
    while any([abs(i - j) for i,j in zip(vp.values(), v.values())]) > 0.001:
        for n in nodes:
            mult = 0
            for m in nodes:
                mult = mult + M.get((m, n), 0) * v[m]
            vp[n] = B * mult + (1 - B) * e[n]
        v, vp = vp.copy(), v.copy()

    return vp
