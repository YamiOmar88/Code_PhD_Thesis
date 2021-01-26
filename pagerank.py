# ======================================================================
# ======================================================================
# Page Rank Algorithm
# ======================================================================
# ======================================================================

# NOTES: You call pageRank(E) where
# -   E is as dictionary containing the edges as keys and the counts
#     as values. Use i for dummy start point and f for dummy end point.
# -   nodes is a list of nodes

def makeMatrix(E, nodes):
    colSum = {}
    for n in nodes:
        colSum[n] = 0
        for m in nodes:
            colSum[n] = colSum[n] + E.get((n, m), 0)

    matrix = {}
    for k in E.keys():
        matrix[k] = E[k] / float( colSum[k[0]] )

    return matrix



def vectorE(M, nodes):
    v = {k: 0.0 for k in nodes}
    for k in M.keys():
        if k[0] == 'i':
            v[k[1]] = float(M[k])
    return v



def pageRank(E, nodes, B=0.85):
    #nodes.sort()
    M = makeMatrix(E, nodes)
    e = vectorE(M, nodes)
    aux = float( len(nodes) )
    v = {k: 1/aux for k in nodes}

    vp = {k: 0.0 for k in nodes}
    while any([abs(i - j) for i,j in zip(vp.values(), v.values())]) > 0.001:
        for n in nodes:
            mult = 0
            for m in nodes:
                mult = mult + M.get((m, n), 0) * v[m]
            vp[n] = B * mult + (1 - B) * e[n]
        v, vp = vp.copy(), v.copy()

    return vp
