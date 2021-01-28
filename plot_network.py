# Manufacturing Entropy - Code for the article
# Original Data: Kaggle competition - Bosch Manufacturing Data: train_date.csv file
# Data used in this file: pre-processed ("data/clean_manufacturing_paths.txt" and "data/clean_manufacturing_edges.txt")
# Yamila Mariel Omar
# Date of original code: 29th October 2019
# Date of code last modification: 21st July 2020



# ===== Function definitions ============

def add_self_loops(paths, edges):
    for k,v in paths.items():
        self_loop = (k[-1], k[-1])
        edges[self_loop] = edges.get(self_loop, 0) + v
    return edges




def generate_dot_file(graph, node_colors, graph_name, filename, edgelabel=False):
    # File creation
    file_content = ''

    # General graph info
    file_content += 'digraph ' + graph_name + '{\n'
    file_content += 'size = "40,20";\n'
    file_content += 'graph[rankdir=TB, center=true, margin=0.05, nodesep=0.2, ranksep=0.5]\n'
    file_content += 'node[fontname="times-bold", fontsize=20]\n'
    file_content += 'edge[arrowsize=0.2, arrowhead=normal, fontsize=8]\n'

    for n in graph.nodes:
        file_content += str(n) + ' [shape=circle, style=filled, color= ' + node_colors[n] + ', width=0.75, height=0.75, fixedsize=true]\n'

    if edgelabel:
        for k,v in graph.edges.items():
            file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=1.5, label=' + str(round(v,2)) + ']\n'
            #file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=1.5]\n'
    else:
        for k,v in graph.edges.items():
            file_content += str(k[0]) + ' -> ' + str(k[1]) + ' [penwidth=1.5]\n'

    file_content += '}'

    path = "figures/" + filename
    with open(path, 'w') as f:
        f.write(file_content)
    return True

# ===== End Function definitions =========



if __name__ == "__main__":
    # Import needed modules
    # =====================
    from graphfile import GraphFile
    from graph import Graph
    import datetime

    # Read data: clean paths and clean edges
    # ======================================
    filename_paths = "data/clean_manufacturing_paths.txt"
    filename_edges = "data/clean_manufacturing_edges.txt"
    edges = GraphFile(filename_edges).read_edges_from_file()
    paths = GraphFile(filename_paths).read_paths_with_count()

    # Generate graph from clean edges
    # ===============================
    edges = add_self_loops(paths, edges)
    G = Graph(edges)

    print("Number of nodes: ", len(G.nodes))
    print("Number of edges: ", len(G.edges.keys()))

    # Color code nodes
    # =======================
    node_colors = dict()
    for node in G.nodes:
        if node in {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}: # Start nodes threshold 0.001
            node_colors[node] = "salmon"
        elif node in {24,25}:
            node_colors[node] = "palegreen"
        elif node in {26,27,28}: # End nodes threshold 0.001
            node_colors[node] = "lightblue"
        else:
            node_colors[node] = "gold"

    # Generate DOT file with network graph
    # ====================================
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = today + "_manufacturing_network_graph.dot"
    generate_dot_file(G, node_colors, "Bosch", filename)



    # =========================================================================
    # PLOT SUBGRAPHS
    # =========================================================================
    # import depth_first_search as dfs
    # in_adjlist, out_adjlist = G.adjacencyList
    # SCC = dfs.scc(out_adjlist)
    # SCC.sort()
    # SCC = [sorted(x) for x in SCC]
    #
    # for number, component in enumerate(SCC):
    #     if len(component) > 1:
    #         filename = "manufacturing_subgraph_" + str(number) + ".dot"
    #         subgraph = {k:v for k,v in edges.items() if k[0] in component and k[1] in component}
    #         max_weight = max(subgraph.values())
    #         subgraph = {k:v/max_weight for k,v in subgraph.items()}
    #         S = Graph(subgraph)
    #     generate_dot_file(S, node_colors, "BoschSubgraph", filename, edgelabel=True)
