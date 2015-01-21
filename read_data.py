#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt

import numpy

def median(lst):
    return numpy.median(numpy.array(lst))

def mean(lst):
    return numpy.mean(numpy.array(lst))


def get_bipartite_graph(B,input_file):
    for line in gzip.open(input_file):
        data_line = json.loads(line.decode('utf8'))
        B.add_node(data_line['actor']['login'], bipartite=0)
        B.add_node(data_line['repo']['name'], bipartite=1)
        B.add_edge(data_line['actor']['login'], data_line['repo']['name'])

        # print('Author = %s, Repo = %s, Action = %s' %
        #      (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))

    return B

def get_authors(bipartite_graph):
    return set(n for n,d in bipartite_graph.nodes(data=True) if d['bipartite']==0)

def get_repos(bipartite_graph):
    return set(n for n,d in bipartite_graph.nodes(data=True) if d['bipartite']==1)

def build_community_graph_from_bipartite_graph(bipartite_graph):
    return nx.projected_graph(bipartite_graph, get_authors(bipartite_graph))

def general_characteristics(G):
    print('Density: %f' % nx.density(G))
    print('Number of nodes: %d' % G.number_of_nodes())
    print('Number of edges: %d' % G.number_of_edges())
    #print('Average cluestering number: %f' % nx.average_clustering(G))
    print('Number of connected components: %d' % nx.number_connected_components(G))
    print('Size of the smallest connected component: %d' % min([len(cc) for cc in nx.connected_components(G)]))
    print('Median size of connected component: %f' % median([len(cc) for cc in nx.connected_components(G)]))
    print('Mean size of connected component: %f' % mean([len(cc) for cc in nx.connected_components(G)]))
    print('Size of the biggest connected component: %d' % max([len(cc) for cc in nx.connected_components(G)]))

    plt.plot(nx.degree_histogram(G))
    plt.axis([0, 20, 0, 30000])

    plt.show()


def remove_isolated_nodes(G,degree):
    modified = False
    for n in G.nodes():
        if nx.degree(G,n) <= degree: # fix the lowest degree
            G.remove_node(n)
            modified = True
    return modified

def save_graph(G, file):
    nx.write_graphml(G, file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: ./%s <github archives>' % sys.argv[0])
    B = nx.Graph()
    for i in range(1,len(sys.argv)):
        get_bipartite_graph(B,sys.argv[i])
    G = build_community_graph_from_bipartite_graph(B)
    while(remove_isolated_nodes(G,5)):
        print("iteration")
    general_characteristics(G)
    save_graph(G, 'test.graphml')
