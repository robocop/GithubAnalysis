#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
# sudo apt-get build-dep python-matplotlib
# pip3 install matplotlib --user
import pygraphviz

#from networkx.algorithms import bipartite

def get_bipartite_graph(B,input_file):
    i = 0
    for line in gzip.open(input_file):
        i += 1
        data_line = json.loads(line.decode('utf8'))

        B.add_node(data_line['actor']['login'], bipartite=0)
        B.add_node(data_line['repo']['name'], bipartite=1)
        B.add_edge(data_line['actor']['login'], data_line['repo']['name'])

#        if i == 1000:
#            break

    #nx.draw_graphviz(B,prog='circo')
    #nx.write_dot(B,'file2.dot')
    #plt.show()

def clean(B):
    connected_components = list(nx.connected_components(B))
    sorted(connected_components, key = lambda cc: len(cc))
    to_remove = set()
    for i in range(0,len(connected_components)-1):
        to_remove.union(connected_components[i])
    for node in to_remove:
        B.remove_node(node)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <github archives>' % sys.argv[0])
    B = nx.Graph()
    for i in range(1,len(sys.argv)):
        get_bipartite_graph(B,sys.argv[i])
    clean(B)
    nx.write_dot(B,'e.dot')
