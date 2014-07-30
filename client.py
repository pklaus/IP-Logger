#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import json
from datetime import datetime
import argparse
import hashlib, uuid
import shelve
import sys
from ipaddress import ip_address

parser = argparse.ArgumentParser(description='IP Logger Client')
parser.add_argument('host', help='The hostname of the server to connect to')
parser.add_argument('port', help='The port the server listens to')
parser.add_argument('--shelvefile', help='A file to log to')
parser.add_argument('--name', '-n', help='The name of this client to transmit to the server', default='')
parser.add_argument('--client-secret', '-c', help='The secret code of this client', required=True)
parser.add_argument('--server-secret', '-s', help='The secret code of this client', required=True)

args = parser.parse_args()

if args.shelvefile:
    d = shelve.open(args.shelvefile)

data = {}
data['name'] = args.name
data['clienttime'] = datetime.now().isoformat()
data['salt'] = uuid.uuid4().hex
authbytes = (data['salt'] + args.server_secret).encode('utf-8')
data['auth'] = hashlib.sha512(authbytes).hexdigest()
messagesigbytes = (data['salt'] + args.name + args.client_secret + data['clienttime']).encode('utf-8')
data['messagesig'] = hashlib.sha512(authbytes).hexdigest()

url = 'http://{}:{}/log?clienttime={clienttime}&name={name}&salt={salt}&messagesig={messagesig}&auth={auth}'
url = url.format(args.host, args.port, **data)
try:
    result = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
except:
    sys.stderr.write("Cannot connect to the server at http://{}:{}\n".format(args.host, args.port)) 
    sys.exit(2)

try:
    result['success']
    if not result['success']:
        sys.stderr.write("No success. The following error occured:\n")
        sys.stderr.write(result['exception'])
        sys.stderr.write("\n")
        sys.exit(128)
    data['ip'] = ip_address(result['data']['ip'])
    data['host'] = "{}:{}".format(args.host, args.port)
    data['servertime'] = result['data']['servertime']
    data['servertime'] = datetime.strptime(data['servertime'], "%Y-%m-%dT%H:%M:%S.%f")
    if args.shelvefile: d[data['servertime'].isoformat()] = data
except KeyError:
    sys.stderr.write("Response seems to be incorrect.\n")
    sys.stderr.write(str(result))
    sys.stderr.write("\n")
    sys.exit(3)
finally:
    if args.shelvefile: d.close()

