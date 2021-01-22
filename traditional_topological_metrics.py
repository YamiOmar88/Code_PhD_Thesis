# Code for PhD Thesis
# Data: full manufacturing network obtained from Kaggle competition data (after cleaning)
# Yamila Mariel Omar
# Date of original code: 19th January 2021
# Date of code last modification: 19th January 2021


from graphfile import GraphFile
from graph import Graph
import betweenness_centrality
import clustering_coefficient
import depth_first_search as dfs


if __name__ == "__main__":
    # Read data
    # =========
    filename = "data/clean_manufacturing_edges.txt"
    edges = GraphFile(filename).read_edges_from_file()
    G = Graph(edges)

    # =========================================================================
    # DEGREE
    # =========================================================================
    indeg, outdeg = G.degree

    # =========================================================================
    # STRENGTH
    # =========================================================================
    instr, outstr = G.strength

    # =========================================================================
    # BETWEENNESS CENTRALITY
    # =========================================================================
    V = list(G.nodes)
    V.sort()

    betcen = betweenness_centrality.bC(V, edges, normalized=False, directed=True)

    # =========================================================================
    # CLUSTERING COEFFICIENT AND TRIANGLES
    # =========================================================================
    # Unweighted
    # ==========
    UW_clustcoeff, UW_triangles = clustering_coefficient.cc_unweighted(edges)
    UW_C = sum(UW_clustcoeff.values())/len(UW_clustcoeff.values())
    print("BDN Clustering Coefficient: ", round(UW_C,3))
    print("BDN - Triangles: ", UW_triangles, "\n\n\n")

    # Weighted
    # ========
    wE = clustering_coefficient.wEdges_maker(edges)
    W_clustcoeff, W_triangles = clustering_coefficient.cc_weighted(wE)
    W_C = sum(W_clustcoeff.values())/len(W_clustcoeff.values())
    print("WDN Clustering Coefficient: ", round(W_C,3))
    print("WDN - Triangles: ", W_triangles, "\n\n\n")


    # =========================================================================
    # PRINT TABLE 6.1
    # =========================================================================
    total_number_of_items_manufactured = 0
    with open("data/clean_manufacturing_paths.txt", "r") as f:
        for line in f:
            line = line.strip().split(" ")
            total_number_of_items_manufactured += int(line[-1])

    instr = {k:round(v/total_number_of_items_manufactured,2) for k,v in instr.items()}
    outstr = {k:round(v/total_number_of_items_manufactured,2) for k,v in outstr.items()}
    betcen = {k:round(v,2) for k,v in betcen.items()}
    UW_cc = {k:round(v,2) for k,v in UW_clustcoeff.items()}
    W_cc = {k:round(v,4) for k,v in W_clustcoeff.items()}

    for k,v in indeg.items():
        s = str(k) + " & " + str(v) + " & " + str(outdeg[k]) + " & "
        s += str(instr[k]) + " & " + str(outstr[k]) + " & "
        s += str(betcen[k]) + " & " + str(UW_cc[k]) + " & " + str(W_cc[k]) + " \\\\"
        print(s)


    # =========================================================================
    # STRONGLY CONNECTED COMPONENTS
    # =========================================================================
    in_adjlist, out_adjlist = G.adjacencyList
    SCC = dfs.scc(out_adjlist)
    SCC.sort()
    SCC = [sorted(x) for x in SCC]

    # Print SCC
    # =========
    print("\n\n\nStrongly Connected Components:")
    for i in SCC:
        print(i)


    # =========================================================================
    # SUBGRAPH CLUSTERING COEFFICIENT
    # =========================================================================
    def subgraph_clustering_coefficient(edges, scc, weighted=True):
        ''' '''
        if weighted:
            subgraph = {k:v for k,v in edges.items() if k[0] in scc and k[1] in scc}
        else:
            subgraph = {k:1 for k,v in edges.items() if k[0] in scc and k[1] in scc}

        subgraph = clustering_coefficient.wEdges_maker(subgraph)
        subgraph_localC, subgraph_triangles = clustering_coefficient.cc_weighted(subgraph)
        subgraph_C = sum(subgraph_localC.values())/len(subgraph_localC.values())
        return subgraph_C, subgraph_localC, subgraph_triangles
    # ================================================

    # Main
    print("\n\n\n\nSubgraph Clustering Coefficient:")
    for i in SCC:
        if len(i) > 1:
            w_SC, w_SlC, w_St = subgraph_clustering_coefficient(edges, i, weighted=True)
            uw_SC, uw_SlC, uw_St = subgraph_clustering_coefficient(edges, i, weighted=False)
            #print(i, " & ", round(uw_SC,2), " & ", round(w_SC,2), "\\\\")
            print("SCC: {}\nBDN Triangles: {}\nWDN Triangles: {}\n\n".format(i, uw_St, w_St))
        else:
            #print(i, " &  0 & 0\\\\")
            pass
