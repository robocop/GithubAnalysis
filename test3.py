#!/usr/bin/env python3

import gzip
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt
# sudo apt-get build-dep python-matplotlib
# pip3 install matplotlib --user

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

        rem_list = []
        
        for n in B.nodes():
            if len(nx.node_connected_component(B,n)) < 3:
                rem_list.append(n)

        B.remove_nodes_from(rem_list)

        #print('Author = %s, Repo = %s, Action = %s' % (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))
        
        if i > 500:
            break

    nx.draw(B)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    B = get_bipartite_graph(sys.argv[1])
