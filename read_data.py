#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import matplotlib.pyplot as plt
import sys

#from networkx.algorithms import bipartite


def get_bipartite_graph(input_file):
    B = nx.Graph()
    i=0
    for line in gzip.open(input_file):
        i+=1
        data_line = json.loads(line.decode('utf8'))

        B.add_node(data_line['actor']['login'], bipartite=0)
        B.add_node(data_line['repo']['name'], bipartite=1)
        B.add_edge(data_line['actor']['login'], data_line['repo']['name'])

        print('Author = %s, Repo = %s, Action = %s' %
              (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))
        if i==1000:
            break

    return B


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    G = get_bipartite_graph(sys.argv[1])
    pos=nx.spring_layout(G)
    nx.draw(G,pos,node_color='#A0CBE2',width=1,edge_cmap=plt.cm.Blues,with_labels=False)
    plt.savefig("graph.png") # save as png

