#!/usr/bin/env python3

import gzip
import sys
import json

def actor(input_file):
    """
        Print all the actor/repository id pairs
    """
    for line in gzip.open(input_file):
        data = json.loads(line.decode())
        print(data["actor"]["id"], data["repo"]["id"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Provide exactly one archive in input')
    actor(sys.argv[1])
