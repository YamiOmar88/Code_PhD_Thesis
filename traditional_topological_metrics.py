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

    # Calculate in- and out-degree
    # ============================
    indeg, outdeg = G.degree

    # Calculate in- and out-strength
    # ==============================
    instr, outstr = G.strength

    # Calculate betweenness centrality
    # ================================
    V = list(G.nodes)
    V.sort()

    betcen = betweenness_centrality.bC(V, edges, normalized=False, directed=True)

    # Calculate clustering coeff. and triangles
    # =========================================
    # Calculate UNWEIGHTED CC and triangles
    UW_clustcoeff, UW_triangles = clustering_coefficient.cc_unweighted(edges)
    UW_C = sum(UW_clustcoeff.values())/len(UW_clustcoeff.values())
    print("UNWEIGHTED Network clustering coefficient: ", UW_C, "\n\n\n")

    # Calculate WEIGHTED CC and triangles
    wE = clustering_coefficient.wEdges_maker(edges)
    W_clustcoeff, triangles = clustering_coefficient.cc_weighted(wE)
    W_C = sum(W_clustcoeff.values())/len(W_clustcoeff.values())
    print("WEIGHTED Network clustering coefficient: ", W_C, "\n\n\n")


    # Print results
    # =============


    instr = {k:round(v/total_number_of_items_manufactured,2) for k,v in instr.items()}
    outstr = {k:round(v/total_number_of_items_manufactured,2) for k,v in outstr.items()}
    betcen = {k:round(v,2) for k,v in betcen.items()}
    UW_cc = {k:round(v,4) for k,v in UW_clustcoeff.items()}
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
    print("\n\n\nStrongly Connected Components:")
    for i in SCC:
        print(i)


    # =========================================================================
    # Subgraph Clustering Coefficient
    # =========================================================================
    print("\n\n\n\nSubgraph Clustering Coefficient:\n")
    for i in SCC:
        if len(i) > 1:
            subgraph = {k:1 for k,v in edges.items() if k[0] in i and k[1] in i}
            subgraph = clustering_coefficient.wEdges_maker(subgraph)
            subgraph_clustcoef, subgraph_triangles = clustering_coefficient.cc_weighted(subgraph)
            subgraph_C = sum(subgraph_clustcoef.values())/len(subgraph_clustcoef.values())
        else:
            print(i, "0")
