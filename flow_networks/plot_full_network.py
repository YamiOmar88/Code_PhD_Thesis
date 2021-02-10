# Code for PhD Thesis - Plot complex network
# Data: F2.txt
# Yamila Mariel Omar
# Date of original code: 9th February 2021
# Date of code last modification: 9th February 2021

from graphviz import Digraph
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

# Get node list
# =============
nodes = G.nodes

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
             '35': "-1,2!",
             '36': "1,2!",
             '37': "0,1!",
             'sink': "0,0!"}

# Graphviz
# ========
g = Digraph("G", engine="neato", filename="results/full_network.gv")
g.attr(rankdir="TB", size='10,10', splines="true")

g.attr("node", shape="oval", style="filled", color="lightgrey", fontname="times-bold", fontsize="16")
g.node("source", pos=positions['source'])
g.node("sink", pos=positions['sink'])

g.attr("node", shape="circle", fixedsize="true", style="filled", fontname="times-bold", fontsize="20")
for n in nodes:
    if n not in ['source', 'sink']:
        g.node(str(n), width='0.5', color="lightblue", pos=positions[str(n)])

for i in nodes:
    for j in nodes:
        if (i,j) in G.edges.keys():
            weight = str(5 * G.edges[(i,j)])
            g.edge(str(i), str(j), penwidth=weight, color="#000000")

g.view()
