# Code for PhD Thesis
# Data: Graph of product family F2
# Yamila Mariel Omar
# Date of original code: 2nd February 2021
# Date of code last modification: 2nd February 2021

import graphfile
import graph
import datetime

def remove_i_and_f(edges):
    new_edges = dict()
    for k,v in edges.items():
        if 'i' in k:
            continue
        elif 'f' in k:
            key = (k[0],k[0])
            new_edges[key] = v
        else:
            new_edges[k] = v
    return new_edges




if __name__ == "__main__":

    # Read data
    # =========
    graph_to_study = "F2"
    full_path = "/home/ubadmin/PhD/CET_4/code/"
    file = graphfile.GraphFile(full_path + "data/" + graph_to_study + ".txt")
    edges = file.read_edges_from_file()

    # Process data
    # ==============
    edges = remove_i_and_f(edges)
    g = graph.Graph(edges)

    # Get entropy
    # ===========
    C_H = {}
    start = datetime.datetime.now()
    for i in g.nodes:
        i, c = g.calculate_node_entropy(i)
        C_H[i] = c
    end = datetime.datetime.now()
    print("Elapsed time: ", end - start)
