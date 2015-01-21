import gzip
import sys
import json

def actor():
    for line in gzip.open('2015-01-01-15.json.gz'):
        data = json.loads(line.decode())
        print(data["actor"]["id"], data["repo"]["id"])

if __name__ == "__main__":
    actor()
