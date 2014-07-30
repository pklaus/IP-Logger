#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import json
from datetime import datetime
import argparse
import hashlib, uuid
import sys

parser = argparse.ArgumentParser(description='IP Logger Client')
parser.add_argument('host', help='The hostname of the server to connect to')
parser.add_argument('port', help='The port the server listens to')
parser.add_argument('--name', '-n', help='The name of this client to transmit to the server', default='')
parser.add_argument('--client-secret', '-c', help='The secret code of this client', required=True)
parser.add_argument('--server-secret', '-s', help='The secret code of this client', required=True)

args = parser.parse_args()

data = {}
data['name'] = args.name
data['time'] = datetime.now().isoformat()
data['salt'] = uuid.uuid4().hex
authbytes = (data['salt'] + args.server_secret).encode('utf-8')
data['auth'] = hashlib.sha512(authbytes).hexdigest()
messagesigbytes = (data['salt'] + args.name + args.client_secret + data['time']).encode('utf-8')
data['messagesig'] = hashlib.sha512(authbytes).hexdigest()

url = 'http://{}:{}/log?time={time}&name={name}&salt={salt}&messagesig={messagesig}&auth={auth}'.format(args.host, args.port, **data)
try:
    result = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
except:
    print("Cannot connect to the server at http://{}:{}".format(args.host, args.port)) 
    sys.exit(2)

from pprint import pprint
pprint(result)

