# Code for PhD Thesis - Maximum Flow Problem
# Data: F2.txt
# Yamila Mariel Omar
# Date of original code: 10th February 2021
# Date of code last modification: 10th February 2021

from capacity import Capacity
from fordfulkerson import FordFulkerson
import string
import json

import sys
sys.path.append('..')

from graphfile import GraphFile
from graph import Graph


# Load edges
# ==========
filename = "data/F2.txt"
edges = GraphFile(filename).read_edges_from_file()
total_items = sum([v for k,v in edges.items() if "source" in k])
edges = {k:v/total_items for k,v in edges.items()}

G = Graph(edges)


# Get edges capacity
# ==================
filename = "results/capacity_estimation.json"
nodes_capacity =  open(filename, "r").read()
nodes_capacity = json.loads(nodes_capacity)
nodes_capacity = {int(k[1:]):v for k,v in nodes_capacity.items()}
C = Capacity(nodes_capacity, source_node='source', sink_node='sink')
C_edges = C.get_edges_capacity(G, "weight")


# Flow Network
# ============
flow_network = Graph(C_edges.copy())

antiparallel_edges = flow_network.find_antiparallel_edges()
counter = 0
while len(antiparallel_edges) > 0:
    edge = antiparallel_edges.pop(0)
    anti = (edge[1],edge[0])
    antiparallel_edges.remove( anti )
    w = flow_network.edges[anti]
    flow_network.deleteEdge(anti[0], anti[1])
    new_node = string.ascii_lowercase[counter]
    flow_network.addEdge(i=edge[1], j=new_node, w_ij=w)
    flow_network.addEdge(i=new_node, j=edge[0], w_ij=w)
    counter += 1


# Update node list
# ================
flow_network.nodes = flow_network._get_set_of_nodes()


# Maximum Flow
# ============
flow, residual_network = FordFulkerson(flow_network, startNode='source', endNode='sink')


# Final flow
# ==========
flow = {k:v for k,v in flow.items() if v > 0}
flow_fraction = {k:round(v/C_edges[k],2) for k,v in flow.items()}

# Total items to produce daily
# ============================
count = 0
for k,v in flow.items():
    if k[1] == "sink": count += v

print("Total items to produce per day: ", count)


# Save flow fraction
# ==================
filename = "results/flow_fraction.txt"
GraphFile(filename).write_graph_to_file(flow_fraction)
