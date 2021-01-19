# Code for PhD Thesis
# Functions to calculate the Clustering Coefficient and Triangle Type Fractions
# Yamila Mariel Omar
# Date of original code: 3rd May 2017
# Date of code last modification: 19th January 2021



'''The user must call the function CCunweighted(E) to calculate the clustering
coefficient of a BDN or CCweighted(wE) in the case of a WDN. The input variables
are as follows:

    1. E or wE: is a dictionary that contains edges as keys and, item counts or
       weights as values (respectively). To calculate weighted edges, the user
       may call the function wEdgesMaker(E, totSum) where totSum is the total
       items manufactured in the manufacturing network under study.

These functions return two things:

    1. CC: a dictionary with nodes as keys and their clustering coefficient as
       value.
    2. frac: a dictionary with the fraction of each triangle type in the family
       under study. The possible triangles are: cycle, middleman, in or out.
'''

# ===============================
# Degree
# Yamila Mariel Omar
# 3rd May 2017
# ===============================

def adjacency_list(E):
    d_in, d_out = {}, {}
    for e in E:
        t, h = e[0], e[1]
        d_out[t] = d_out.get(t, []) + [h]
        d_in[h] = d_in.get(h, []) + [t]
    d_in = {k:set(v) for k,v in d_in.items()}
    d_out = {k:set(v) for k,v in d_out.items()}
    return d_in, d_out


def adjacency_weight(E):
    s_in, s_out = {}, {}
    for e in E.keys():
        t, h = e[0], e[1]
        s_out[t] = s_out.get(t, 0) + E[e]
        s_in[h] = s_in.get(h, 0) + E[e]
    return s_in, s_out


def degree(E, weighted=False):
    if not weighted:
        inDegree, outDegree = adjacency_list(E.keys())
        inDegree = {k:len(v) for k,v in inDegree.items()}
        outDegree = {k:len(v) for k,v in outDegree.items()}
    else:
        inDegree, outDegree = adjacency_weight(E)
    nodes = set(inDegree.keys()) | set(outDegree.keys())
    d = {}
    for n in nodes:
        d[n] = inDegree.get(n, 0) + outDegree.get(n, 0)
    return d


# ======================
# Clustering Coefficient
# Yamila Mariel Omar
# 4th May 2017
# ======================

def bilateral_edges(Ein, Eout):
    nodes = set(Ein.keys()) | set(Eout.keys())
    d_bilateral = {}
    for n in nodes:
        d_bilateral[n] = len(Ein.get(n, set()) & Eout.get(n, set()))
    return d_bilateral

def cc_unweighted(E):
    CC = {}
    Ein, Eout = adjacency_list(E)
    nodes = set(Ein.keys()) | set(Eout.keys())
    deg = degree(E)
    bilEdges = bilateral_edges(Ein, Eout)
    import itertools
    tot, cyc, mid, inn, out = {}, {}, {}, {}, {}
    for n in nodes:
        neighbors = Ein.get(n, set()) | Eout.get(n, set())
        for x in itertools.combinations(neighbors, 2):
            i,j,h = n, x[0], x[1]
            a_ij, a_ji, a_ih, a_hi, a_jh, a_hj = 0, 0, 0, 0, 0, 0
            if j in Eout.get(i, set()): a_ij = 1
            if i in Eout.get(j, set()): a_ji = 1
            if h in Eout.get(i, set()): a_ih = 1
            if i in Eout.get(h, set()): a_hi = 1
            if h in Eout.get(j, set()): a_jh = 1
            if j in Eout.get(h, set()): a_hj = 1
            tot[n] = tot.get(n, 0) + (a_ij + a_ji)*(a_ih + a_hi)*(a_jh + a_hj)

            # Get the differnt triangles sums
            cyc[n] = cyc.get(n, 0) + float(a_ij*a_hi*a_jh + a_ji*a_ih*a_hj)
            mid[n] = mid.get(n, 0) + float(a_ij*a_hi*a_hj + a_ji*a_ih*a_jh)
            inn[n] = inn.get(n, 0) + float(a_ji*a_hi*a_jh + a_ji*a_hi*a_hj)
            out[n] = out.get(n, 0) + float(a_ij*a_ih*a_jh + a_ij*a_ih*a_hj)

        CC[n] = 0.5 * float(tot[n]) / float(deg[n] * (deg[n] - 1) - 2*bilEdges[n])

    # Get the different triangles fractions
    for k in tot.keys():
        cyc[k] = cyc[k] / tot[k]
        mid[k] = mid[k] / tot[k]
        inn[k] = inn[k] / tot[k]
        out[k] = out[k] / tot[k]

    cyc = round(sum(cyc.values()) / len(cyc.keys()), 3)
    mid = round(sum(mid.values()) / len(mid.keys()), 3)
    inn = round(sum(inn.values()) / len(inn.keys()), 3)
    out = round(sum(out.values()) / len(out.keys()), 3)

    fractions = {'cycles': cyc, 'middlemen': mid, 'in': inn, 'out': out}

    return CC, fractions


def wEdges_maker(E, totSum):
    wE = {}
    for k,v in E.items():
        wE[k] = v / float(totSum) # Total number of transactions
    return wE


def cc_weighted(wE):
    CC = {}
    Ein, Eout = adjacency_list(wE)
    nodes = set(Ein.keys()) | set(Eout.keys())
    deg = degree(wE)
    bilEdges = bilateral_edges(Ein, Eout)
    import itertools
    tot, cyc, mid, inn, out = {}, {}, {}, {}, {}
    for n in nodes:
        neighbors = Ein.get(n, set()) | Eout.get(n, set())
        for x in itertools.combinations(neighbors, 2):
            i,j,h = n, x[0], x[1]
            w_ij, w_ji, w_ih, w_hi, w_jh, w_hj = 0, 0, 0, 0, 0, 0
            if j in Eout.get(i, set()): w_ij = wE[(i,j)]**(1.0/3)
            if h in Eout.get(i, set()): w_ih = wE[(i,h)]**(1.0/3)
            if h in Eout.get(j, set()): w_jh = wE[(j,h)]**(1.0/3)
            if i in Eout.get(j, set()): w_ji = wE[(j,i)]**(1.0/3)
            if i in Eout.get(h, set()): w_hi = wE[(h,i)]**(1.0/3)
            if j in Eout.get(h, set()): w_hj = wE[(h,j)]**(1.0/3)
            tot[n] = tot.get(n, 0) + (w_ij + w_ji)*(w_ih + w_hi)*(w_jh + w_hj)

            # Get the differnt triangles sums
            cyc[n] = cyc.get(n, 0) + float(w_ij*w_hi*w_jh + w_ji*w_ih*w_hj)
            mid[n] = mid.get(n, 0) + float(w_ij*w_hi*w_hj + w_ji*w_ih*w_jh)
            inn[n] = inn.get(n, 0) + float(w_ji*w_hi*w_jh + w_ji*w_hi*w_hj)
            out[n] = out.get(n, 0) + float(w_ij*w_ih*w_jh + w_ij*w_ih*w_hj)

        CC[n] = 0.5 * tot[n] / float(deg[n]*(deg[n]-1) - 2*bilEdges[n])

    # Get the different triangles fractions
    for k in tot.keys():
        cyc[k] = cyc[k] / tot[k]
        mid[k] = mid[k] / tot[k]
        inn[k] = inn[k] / tot[k]
        out[k] = out[k] / tot[k]

    cyc = round(sum(cyc.values()) / len(cyc.keys()), 3)
    mid = round(sum(mid.values()) / len(mid.keys()), 3)
    inn = round(sum(inn.values()) / len(inn.keys()), 3)
    out = round(sum(out.values()) / len(out.keys()), 3)

    fractions = {'cycles': cyc, 'middlemen': mid, 'in': inn, 'out': out}

    return CC, fractions
