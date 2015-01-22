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

class GitHubActivity:
    def __init__(self):
        self.log = dict()

    def add(self, id, value):
        self.log[id] = value

    def load_gz(self, input_file):
        day = int(input_file.split('-')[2])
        hour = int(input_file.split('-')[3].split('.')[0])
        id = day*24+hour
        i = sum(1 for line in gzip.open(input_file))

        #print('%d %d' % (id, i))
        self.add(id, i)

    def plot(self):
        x = []
        y = []
        for key in self.log.keys():
            x.append(key/24.)
            y.append(self.log[key])
        plt.plot(x, y, 'r--')
        plt.show()


class BipartiteGraph:
    def __init__(self):
        self.B = nx.Graph()

    def load_gz(self, input_file):
        """
            Add the data of the file to the graph
        """
        for line in gzip.open(input_file):


            data_line = json.loads(line.decode('utf8'))
            self.B.add_node(data_line['actor']['login'], bipartite=0)
            self.B.add_node(data_line['repo']['name'], bipartite=1)
            self.B.add_edge(data_line['actor']['login'], data_line['repo']['name'])


    def get_authors(self):
        """
            Get the set of authors
        """
        return set(n for n,d in self.B.nodes(data=True) if d['bipartite'] == 0)

    def get_repos(self):
        """
            Get the set of repositories
        """
        return set(n for n,d in self.B.nodes(data=True) if d['bipartite'] == 1)

    def build_community_graph_from_bipartite_graph(self):
        """"
            Graph which nodes are the users and (uv) is an edge iff u and v has contributed to a same repository
        """
        return nx.projected_graph(self.B, self.get_authors())

class CommunityGraph:
    def __init__(self, G):
        self.G = G

    def general_characteristics(self, k=3):
        print('Density: %f' % nx.density(self.G))
        print('Number of nodes: %d' % self.G.number_of_nodes())
        print('Number of edges: %d' % self.G.number_of_edges())
        print('Average cluestering number: %f' % nx.average_clustering(self.G))
        connected_components = list(nx.connected_components(self.G))
        print('Number of connected components: %d' % len(connected_components))
        print('Size of the smallest connected component: %d' % min([len(cc) for cc in connected_components]))
        print('Median size of connected component: %f' % median([len(cc) for cc in connected_components]))
        print('Mean size of connected component: %f' % mean([len(cc) for cc in connected_components]))
        print('Size of the biggest connected component: %d' % max([len(cc) for cc in connected_components]))
        kcliques = list(nx.k_clique_communities(self.G,k))
        print('Number of %d-clique communities: %d' % (k,len(kcliques)))
        if len(kcliques) > 0:
            print('Size of the smallest %d-clique communities: %d' % (k,min([len(cc) for cc in kcliques])))
            print('Median size of %d-clique communities: %f' % (k,median([len(cc) for cc in kcliques])))
            print('Mean size of %d-clique communities: %f' % (k,mean([len(cc) for cc in kcliques])))
            print('Size of the biggest %d-clique communities: %d' % (k,max([len(cc) for cc in kcliques])))

    def remove_isolated_nodes(self, degree):
        modified = False
        for n in self.G.nodes():
            if nx.degree(self.G, n) <= degree: # fix the lowest degree
                self.G.remove_node(n)
                modified = True
        return modified

    def remove_small_connected_components(self, size):
        nodes_to_remove = [n for cc in nx.connected_components(self.G) for n in cc if len(cc) <= size]
        for n in nodes_to_remove:
            self.G.remove_node(n)

    def communityGraph(self, k):
        """
            Return the graph whose nodes are k-cliques.
        """
        alias = {}
        communities = list(set(x) for x in nx.k_clique_communities(self.G, k))
        H = nx.Graph()
        for i in range (0,len(communities)):
            H.add_node(i)
            alias[i] = communities[i]
        for (u,v) in self.G.edges():
            for i in range(0,len(communities)):
                for j in range(i+1,len(communities)):
                    if u in alias[i] and v in alias[j]:
                        H.add_edge(i,j)
        return (H, alias)

    def save__mml(self, file):
        nx.write_graphml(self.G, file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <github archives>' % sys.argv[0])
    Logger = GitHubActivity()


    B = BipartiteGraph()
    for i in range(1,len(sys.argv)):
        #B.load_gz(sys.argv[i])
        Logger.load_gz(sys.argv[i])

    Logger.plot()

    #G = B.build_community_graph_from_bipartite_graph()
    #CommunityG = CommunityGraph(G)

    #while CommunityG.remove_isolated_nodes(10):
    #    print("iteration")

    #CommunityG.remove_small_connected_components(10)



    #CommunityG.general_characteristics(4)
    #print('')

    #(H,alias) = CommunityG.communityGraph(4)
    #CommunityH = CommunityGraph(H)
    #CommunityH.general_characteristics(4)

    #CommunityG.save__mml('G.graphml')
    #CommunityH.save__mml('H.graphml')

    #    nx.draw(H)
    #    plt.show()
    #nx.write_dot(H,"graph.dot") # only python2
