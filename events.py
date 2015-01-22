#!/usr/bin/env python3

import gzip
import json
import sys

class Counter:
    def __init__(self):
        self.total = 0
        self.M = {}

    def countEvents(self,input_file):
        for line in gzip.open(input_file):
            data_line = json.loads(line.decode('utf8'))
            self.total += 1
            try:
                self.M[data_line['type']] += 1
            except:
                self.M[data_line['type']] = 1


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
    counter = Counter()
    for i in range(1,len(sys.argv)):
        counter.countEvents(sys.argv[i])
    events = list(counter.M.items())
    events = sorted(events,key = lambda x : -x[1])
    for i in events:
        print("{0} \t({1:.1f}%)\t:{2}".format(i[1],i[1]/counter.total*100,i[0]))
