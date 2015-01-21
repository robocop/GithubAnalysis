import gzip
import json


def actor():
    i = 0
    for line in gzip.open('data/2015-01-01-15.json.gz'):
        data_line = json.loads(line.decode('utf8'))
        if i == 0:
            print(data_line)
        print('Author = %s, Repo = %s, Action = %s' %
              (data_line['actor']['login'], data_line['repo']['name'], data_line['type']))
        i += 1


if __name__ == "__main__":
    actor()