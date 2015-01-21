#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib as plt

import numpy

def median(lst):
    return numpy.median(numpy.array(lst))

def mean(lst):
    return numpy.mean(numpy.array(lst))


def get_bipartite_graph(input_file):
    B = nx.Graph()

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
    G = nx.Graph()
    authors = get_authors(bipartite_graph)

    for x in authors:
        G.add_node(x)
        repos = bipartite_graph.neighbors(x)
        for repo in repos:
            for y in bipartite_graph.neighbors(repo):
                if x != y:
                    G.add_edge(x, y)
    return G


def general_characteristics(G):
    print('Density: %f' % nx.density(G))
    print('Number of nodes: %d' % G.number_of_nodes())
    print('Number of edges: %d' % G.number_of_edges())
    print('Average cluestering number: %f' % nx.average_clustering(G))
    print('Number of connected components: %d' % nx.number_connected_components(G))
    print('Size of the smallest connected component: %d' % min([len(cc) for cc in nx.connected_components(G)]))
    print('Median size of connected component: %f' % median([len(cc) for cc in nx.connected_components(G)]))
    print('Mean size of connected component: %f' % mean([len(cc) for cc in nx.connected_components(G)]))
    print('Size of the biggest connected component: %d' % max([len(cc) for cc in nx.connected_components(G)]))




if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    B = get_bipartite_graph(sys.argv[1])
    G = build_community_graph_from_bipartite_graph(B)

    general_characteristics(G)
