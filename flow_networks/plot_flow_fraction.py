# Code for PhD Thesis - Plot flow fraction
# Data: flow_fraction.txt
# Yamila Mariel Omar
# Date of original code: 10th February 2021
# Date of code last modification: 10th February 2021

from graphviz import Digraph
import sys
sys.path.append('..')

from graphfile import GraphFile
from graph import Graph

# Load edges
# ==========
filename = "results/flow_fraction.txt"
edges = GraphFile(filename).read_edges_from_file()
G = Graph(edges)

# Get node list
# =============
nodes = G.nodes


# =================================================================
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

color_gradient = ["#008000",  #green
                  "#339900",
                  "#66B200",
                  "#99CC00",
                  "#CCE500",
                  "#FFFF00",   #yellow
                  "#FFCC00",
                  "#FF9900",
                  "#FF6600",
                  "#FF3300",
                  "#FF0000"]   #red

fraction_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# =================================================================

g = Digraph("G", engine="neato", filename="results/flow_fraction.gv")
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
            fraction = G.edges[(i,j)]
            x = fraction_list.index( round(fraction, 1) )
            col = color_gradient[x]
            g.edge(str(i), str(j), penwidth="2", color=col, label=str(fraction))


g.view()
