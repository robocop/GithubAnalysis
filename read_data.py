import gzip
import json
import networkx as nx
from networkx.algorithms import bipartite


def get_bipartite_graph():
    B = nx.Graph()

    for line in gzip.open('data/2015-01-01-15.json.gz'):
        data_line = json.loads(line.decode('utf8'))

        B.add_node(data_line['actor']['login'], bipartite=0)
        B.add_node(data_line['repo']['name'], bipartite=1)
        B.add_edge(data_line['actor']['login'], data_line['repo']['name'])

        print('Author = %s, Repo = %s, Action = %s' %
              (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))

    return B


if __name__ == "__main__":
    B = get_bipartite_graph()
    nx.draw_networkx(B)
