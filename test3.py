#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
import numpy
# sudo apt-get build-dep python-matplotlib
# pip3 install matplotlib --user
import pygraphviz

#from networkx.algorithms import bipartite

def median(lst):
    return numpy.median(numpy.array(lst))

def mean(lst):
    return numpy.mean(numpy.array(lst))

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
    biggest = max(connected_components,key = lambda cc : len(cc))
    nodes = list(B.nodes())
    for n in nodes:
        if n not in biggest:
            B.remove_node(n)

def general_characteristics(G):
    print('Density: %f' % nx.density(G))
    print('Number of nodes: %d' % G.number_of_nodes())
    print('Number of edges: %d' % G.number_of_edges())
    print('Average cluestering number: %f' % nx.average_clustering(G))
    connected_components = list(nx.connected_components(G))
    print('Number of connected components: %d' % len(connected_components))
    print('Size of the smallest connected component: %d' % min([len(cc) for cc in connected_components]))
    print('Median size of connected component: %f' % median([len(cc) for cc in connected_components]))
    print('Mean size of connected component: %f' % mean([len(cc) for cc in connected_components]))
    print('Size of the biggest connected component: %d' % max([len(cc) for cc in connected_components]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <github archives>' % sys.argv[0])
    B = nx.Graph()
    for i in range(1,len(sys.argv)):
        get_bipartite_graph(B,sys.argv[i])
    general_characteristics(B)
    clean(B)
    print('')
    general_characteristics(B)
    nx.write_dot(B,'e.dot')
