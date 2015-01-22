#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
import numpy
import os

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
    """
        A bipartite graph that links the users with the repositories they contributed to
    """
    def __init__(self):
        self.graph = nx.Graph()

    def load_gz(self, input_file, eventType = None):
        """
            Add the data of the file to the graph
        """
        for line in gzip.open(input_file):
            data_line = json.loads(line.decode('utf8'))
            if not eventType or data_line['type'] == eventType:
                self.graph.add_node(data_line['actor']['login'], bipartite=0)
                self.graph.add_node(data_line['repo']['name'], bipartite=1)
                self.graph.add_edge(data_line['actor']['login'], data_line['repo']['name'])

    def get_authors(self):
        """
            Get the set of authors
        """
        return set(n for n,d in self.graph.nodes(data=True) if d['bipartite'] == 0)

    def get_repos(self):
        """
            Get the set of repositories
        """
        return set(n for n,d in self.graph.nodes(data=True) if d['bipartite'] == 1)

    def remove_small_connected_components(self, sz):
        """
            Remove all cc of size <= sz
        """
        nodes_to_remove = [n for cc in nx.connected_components(self.graph) for n in cc if len(cc) <= sz]
        for n in nodes_to_remove:
            self.graph.remove_node(n)

    def build_community_graph_from_bipartite_graph(self):
        """"
            Projection : graph which nodes are the users and (uv) is an edge iff u and v have contributed to a same repository
        """
        return nx.projected_graph(self.graph, self.get_authors())

    def clean(self):
        H=self.graph.copy()
        connected_components = list(nx.connected_components(H))
        biggest = sorted(connected_components,key = lambda cc : len(cc))
        for n in H.nodes():
            if n not in biggest[-1]:
                H.remove_node(n)
        i = -1
        while(nx.diameter(H) <= 4):
            print(i)
            i-=1
            H = self.graph.copy()
            for n in H.nodes():
                if n not in biggest[i]:
                    H.remove_node(n)
        print("i=%d" % i)
        self.graph = H

    def general_characteristics(self, k=3,diameter=False):
        print('Density: %f' % nx.density(self.graph))
        print('Number of nodes: %d' % self.graph.number_of_nodes())
        print('Number of edges: %d' % self.graph.number_of_edges())
        connected_components = list(nx.connected_components(self.graph))
        if diameter:
            print('Diameter: %d' % nx.diameter(self.graph))
        print('Average clustering number: %f' % nx.average_clustering(self.graph))
        connected_components = list(nx.connected_components(self.graph))
        print('Number of connected components: %d' % len(connected_components))
        print('Size of the smallest connected component: %d' % min([len(cc) for cc in connected_components]))
        print('Median size of connected component: %f' % median([len(cc) for cc in connected_components]))
        print('Mean size of connected component: %f' % mean([len(cc) for cc in connected_components]))
        print('Size of the biggest connected component: %d' % max([len(cc) for cc in connected_components]))
        kcliques = list(nx.k_clique_communities(self.graph,k))
        print('Number of %d-clique communities: %d' % (k,len(kcliques)))
        if len(kcliques) > 0:
            print('Size of the smallest %d-clique communities: %d' % (k,min([len(cc) for cc in kcliques])))
            print('Median size of %d-clique communities: %f' % (k,median([len(cc) for cc in kcliques])))
            print('Mean size of %d-clique communities: %f' % (k,mean([len(cc) for cc in kcliques])))
            print('Size of the biggest %d-clique communities: %d' % (k,max([len(cc) for cc in kcliques])))

    def save__mml(self, file):
        """
            Save the graph in mml format
        """
        nx.write_graphml(self.graph, file)

class CommunityGraph:
    """
        A graph that links all the users that worked on a same project
    """
    def __init__(self, G):
        if isinstance(G,BipartiteGraph):
            self.graph = G.build_community_graph_from_bipartite_graph()
        else:
            self.graph = G

    def general_characteristics(self, k=3):
        print('Density: %f' % nx.density(self.graph))
        print('Number of nodes: %d' % self.graph.number_of_nodes())
        print('Number of edges: %d' % self.graph.number_of_edges())
        connected_components = list(nx.connected_components(self.graph))
        if(len(connected_components) == 1):
            print('Diameter: %d' % nx.diameter(self.graph))
        print('Average clustering number: %f' % nx.average_clustering(self.graph))
        print('Number of connected components: %d' % len(connected_components))
        print('Size of the smallest connected component: %d' % min([len(cc) for cc in connected_components]))
        print('Median size of connected component: %f' % median([len(cc) for cc in connected_components]))
        print('Mean size of connected component: %f' % mean([len(cc) for cc in connected_components]))
        print('Size of the biggest connected component: %d' % max([len(cc) for cc in connected_components]))
        kcliques = list(nx.k_clique_communities(self.graph,k))
        print('Number of %d-clique communities: %d' % (k,len(kcliques)))
        if len(kcliques) > 0:
            print('Size of the smallest %d-clique communities: %d' % (k,min([len(cc) for cc in kcliques])))
            print('Median size of %d-clique communities: %f' % (k,median([len(cc) for cc in kcliques])))
            print('Mean size of %d-clique communities: %f' % (k,mean([len(cc) for cc in kcliques])))
            print('Size of the biggest %d-clique communities: %d' % (k,max([len(cc) for cc in kcliques])))

    def remove_isolated_nodes(self, deg):
        """
            Remove all nodes of degree <= deg
        """
        modified = False
        for n in self.graph.nodes():
            if nx.degree(self.graph, n) <= deg: # fix the lowest degree
                self.graph.remove_node(n)
                modified = True
        return modified

    def remove_small_connected_components(self, sz):
        """
            Remove all cc of size <= sz
        """
        nodes_to_remove = [n for cc in nx.connected_components(self.graph) for n in cc if len(cc) <= sz]
        for n in nodes_to_remove:
            self.graph.remove_node(n)

    def communityGraph(self, k):
        """
            Return the graph whose nodes are k-cliques.
        """
        alias = {}
        communities = list(set(x) for x in nx.k_clique_communities(self.graph, k))
        H = nx.Graph()
        for i in range (0,len(communities)):
            H.add_node(i)
            alias[i] = communities[i]
        for (u,v) in self.graph.edges():
            for i in range(0,len(communities)):
                for j in range(i+1,len(communities)):
                    if u in alias[i] and v in alias[j]:
                        H.add_edge(i,j)
        return (H, alias)

    def save__mml(self, file):
        """
            Save the graph in mml format
        """
        nx.write_graphml(self.graph, file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <github archives>' % sys.argv[0])

    ### Log all data of all the files
    #Logger = GitHubActivity()
    #B = BipartiteGraph()
    #for i in range(1,len(sys.argv)):
    #    Logger.load_gz(sys.argv[i])
    #
    #Logger.plot()


    ### Read all the file of a folder
    B = BipartiteGraph()
    for file in os.listdir(sys.argv[1]):
        print(file)
        B.load_gz(sys.argv[1] + '/' + file,'IssuesEvent')

    ### Build projection, remove small cc << take a BipartiteGraph as input and output a CommunityGraph
    #CommunityG = CommunityGraph(B)
    #CommunityG.remove_small_connected_components(50)

    ### Print general characteristics of a community graph
    #CommunityG.general_characteristics(4)
    #print('')

    ### Build community graph
    #(H,alias) = CommunityG.communityGraph(4)
    #CommunityH = CommunityGraph(H)
    #CommunityH.general_characteristics(4)

#    B.remove_small_connected_components(100)
    B.general_characteristics()

    B.clean()

    print('')

    B.general_characteristics(diameter=True)
    B.save__mml('B.graphml')

    #CommunityG.save__mml('G.graphml')

    #CommunityH.save__mml('H.graphml')

    ### Display small graphs
    #nx.draw(H)
    #plt.show()
    #nx.write_dot(H,"graph.dot") # only python2 ?
