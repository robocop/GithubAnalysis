#!/usr/bin/env python3

import gzip
import json
import sys

def actor(input_file):
    i = 0
    for line in gzip.open(input_file):
        data_line = json.loads(line.decode('utf8'))
        if i == 0:
            print(data_line)
        print('Author = %s, Repo = %s, Action = %s' %
              (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))
        i += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    actor(sys.argv[1])
