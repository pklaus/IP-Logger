#!/usr/bin/env python

from datetime import datetime
from ipaddress import ip_address
from pprint import pprint
import argparse
import shelve
import hashlib
import sys
import pdb

parser = argparse.ArgumentParser(description='Analyzer for IP Logger Logfiles')
parser.add_argument('shelvefile', help='The file to store previous requests in.')
parser.add_argument('--server-secret', '-s', help='The secret code of the server.')
args = parser.parse_args()

d = shelve.open(args.shelvefile)
print("Currently stored entries: {}".format(len(d)))

earliest = datetime.now()
latest = datetime(1900, 1, 1)
nameset = set()
for el in list(d):
    entry = d[el]
    #pprint(entry)
    earliest = min(entry['servertime'], earliest)
    latest = max(entry['servertime'], latest)
    nameset.add(entry['name'])

print("Earliest entry: {}.".format(earliest))
print("Latest entry: {}.".format(latest))
print("Names used: {}.".format(nameset))

content = [d[a] for a in d]
pprint(content)

print("Analyze whatever else you like. Enter `c` to quit.")
pdb.set_trace()

d.close()

