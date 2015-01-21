#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt


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
    return nx.projected_graph(bipartite_graph, get_authors(bipartite_graph))

def general_characteristics(G):
    print('Density: %f' % nx.density(G))
    print('Number of nodes: %d' % G.number_of_nodes())
    print('Number of edges: %d' % G.number_of_edges())
    print('Average cluestering number: %f' % nx.average_clustering(G))



    plt.plot(nx.degree_histogram(G))
    print('ok')
    plt.axis([0, 5, 0, 4000])

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    B = get_bipartite_graph(sys.argv[1])
    G = build_community_graph_from_bipartite_graph(B)

    general_characteristics(G)
