# Code for PhD Thesis
# Data: full manufacturing network obtained from Kaggle competition data (after cleaning)
# Yamila Mariel Omar
# Date of original code: 26th January 2021
# Date of code last modification: 26th January 2021


from graphfile import GraphFile
from graph import Graph
import pagerank

if __name__ == "__main__":
    # Read data
    # =========
    filename = "data/clean_manufacturing_edges.txt"
    edges = GraphFile(filename).read_edges_from_file()
    G = Graph(edges)

    # Get start nodes and their fraction
    # ==================================
    total_number_of_items_manufactured = 0
    start_nodes = {n: 0 for n in G.nodes}
    with open("data/clean_manufacturing_paths.txt", "r") as f:
        for line in f:
            line = line.strip().split(" ")
            n_0 = int(line[0])
            path_count = int(line[-1])
            start_nodes[n_0] += path_count
            total_number_of_items_manufactured += path_count

    start_nodes = {k:v/total_number_of_items_manufactured for k,v in start_nodes.items()}


    # CALCULATE PAGERANK FOR DIFFERENT CONDITIONS
    # ===========================================
    # Case 1: Original algorithm
    E = {k:1 for k,v in edges.items()}
    start_nodes_all = {n:1/len(G.nodes) for n in G.nodes}
    PR_1 = pagerank.pagerank(E, list(G.nodes), start_nodes_all, B=0.85)

    # Case 2: Edge weights considered
    PR_2 = pagerank.pagerank(edges, list(G.nodes), start_nodes_all, B=0.85)

    # Case 3: Edge weights and start nodes considered
    PR_3 = pagerank.pagerank(edges, list(G.nodes), start_nodes, B=0.85)

    # Print table for LaTeX
    for k,v in PR_1.items():
        print(k, " & ", round(v,3), " & ", round(PR_2[k],3), " & ", round(PR_3[k],3), "\\\\")
