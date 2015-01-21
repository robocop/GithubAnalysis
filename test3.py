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

def get_bipartite_graph(input_file):
    B = nx.Graph()

    i = 0
    for line in gzip.open(input_file):
        i += 1
        data_line = json.loads(line.decode('utf8'))

        B.add_node(data_line['actor']['login'], bipartite=0)
        B.add_node(data_line['repo']['name'], bipartite=1)
        B.add_edge(data_line['actor']['login'], data_line['repo']['name'])
        
        if i == 1000000:
            break

    for n in B.nodes():
        if len(nx.node_connected_component(B,n)) < 5: # fix the lowest degree
            B.remove_node(n)

    #nx.draw_graphviz(B,prog='circo')
    #nx.write_dot(B,'file2.dot')
    #plt.show()
    nx.write_dot(B,'e.dot')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    get_bipartite_graph(sys.argv[1])
