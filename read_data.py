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


def general_characteristics(G,k=3):
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
    kcliques = list(nx.k_clique_communities(G,k))
    print('Number of %d-clique communities: %d' % (k,len(kcliques)))
    print('Size of the smallest %d-clique communities: %d' % (k,min([len(cc) for cc in kcliques])))
    print('Median size of %d-clique communities: %f' % (k,median([len(cc) for cc in kcliques])))
    print('Mean size of %d-clique communities: %f' % (k,mean([len(cc) for cc in kcliques])))
    print('Size of the biggest %d-clique communities: %d' % (k,max([len(cc) for cc in kcliques])))

def remove_isolated_nodes(G,degree):
    modified = False
    for n in G.nodes():
        if nx.degree(G,n) <= degree: # fix the lowest degree
            G.remove_node(n)
            modified = True
    return modified

def remove_small_connected_components(G,size):
    nodes_to_remove = [n for cc in nx.connected_components(G) for n in cc if len(cc) <= size]
    for n in nodes_to_remove:
        G.remove_node(n)

def communityGraph(G,k):
    """
        Return the graph whose nodes are k-cliques.
    """
    alias = {}
    communities = list(set(x) for x in nx.k_clique_communities(G,k))
    H = nx.Graph()
    for i in range (0,len(communities)):
        H.add_node(i)
        alias[i] = communities[i]
    for (u,v) in G.edges():
        for i in range(0,len(communities)):
            for j in range(0,len(communities)):
                if u in alias[i] and v in alias[j]:
                    H.add_edge(i,j)
    return (H,alias)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: ./%s <github archives>' % sys.argv[0])
    B = nx.Graph()
    for i in range(1,len(sys.argv)):
        get_bipartite_graph(B,sys.argv[i])
    G = build_community_graph_from_bipartite_graph(B)
#    while(remove_isolated_nodes(G,10)):
#        print("iteration")
#    remove_small_connected_components(G,10)
    general_characteristics(G,4)
    (H,alias) = communityGraph(G,4)
    print("")
    general_characteristics(H,4)
    nx.draw(H)
    plt.show()
