# Code for PhD Thesis - Plot complex network
# Data: F2.txt
# Yamila Mariel Omar
# Date of original code: 9th February 2021
# Date of code last modification: 9th February 2021

from graphviz import Digraph
import string
import json
from capacity import Capacity

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


# Get node list
# =============
nodes = flow_network._get_set_of_nodes()

# Nodes positions in plot
# =======================
positions = {'source': "0,9!",
             '24': "-1,8!",
             '25': "1,8!",
             '26': "-1,7!",
             '27': "1,7!",
             '29': "0,6!",
             '30': "0,5!",
             '33': "0,4!",
             '34': "0,3!",
             '35': "-2,2!",
             '36': "2,2!",
             '37': "0,1!",
             'a': "-2,5.5!",
             'b': "-2,4.75!",
             'c': "2,5!",
             'd': "2,4!",
             'e': "-3,3.75!",
             'f': "2,3!",
             'g': "-1,2!",
             'h': "-2,3!",
             'i': "1,3!",
             'j': "1,2!",
             'k': "-2,1!",
             'l': "2,1!",
             'sink': "0,0!"}

# Graphviz
# ========
g = Digraph("G", engine="neato", filename="results/no_antiparallel.gv")
g.attr(rankdir="TB", size='10,10', splines="true")

g.attr("node", shape="oval", style="filled", color="lightgrey", fontname="times-bold", fontsize="16")
g.node("source", pos=positions['source'])
g.node("sink", pos=positions['sink'])

g.attr("node", shape="circle", fixedsize="true", style="filled", fontname="times-bold", fontsize="20")
for n in nodes:
    if type(n) != str:
        g.node(str(n), width='0.5', color="lightblue", pos=positions[str(n)])
    elif n in string.ascii_lowercase:
        g.node(n, width='0.5', color="salmon", pos=positions[n])

for i in nodes:
    for j in nodes:
        if (i,j) in flow_network.edges.keys():
            if flow_network.edges[(i,j)] < 1000:
                weight = str(5 * flow_network.edges[(i,j)] /1000)
            else:
                weight = str(1)

            g.edge(str(i), str(j), penwidth=weight, color="#000000")


g.view()
