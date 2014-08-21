#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import json
from datetime import datetime
import argparse
import hmac
import uuid
import shelve
import sys
from ipaddress import ip_address
from tools import reverse_lookup, lookup, get_ip_address

def main():
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
    
    # Preparing the message to transmit
    data = {}
    data['name'] = args.name
    clienttime = datetime.utcnow()
    data['clienttime'] = clienttime.isoformat()
    data['host'] = args.host
    data['hostip'] = lookup(args.host)
    data['reversehost'] = reverse_lookup(args.host)
    data['salt'] = uuid.uuid4().hex
    data['auth'] = hmac.new(args.server_secret.encode('utf-8'), data['salt'].encode('utf-8'), digestmod='sha1').hexdigest()
    messagesigbytes = (data['salt'] + args.name + data['clienttime']).encode('utf-8')
    data['messagesig'] = hmac.new(args.client_secret.encode('utf-8'), messagesigbytes, digestmod='sha1').hexdigest()
    
    url = 'http://{}:{}/log?{}'
    url = url.format(args.host, args.port, "&".join(["{}={}".format(key, data[key]) for key in data]))
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
        # customizations of the dataset to be logged locally:
        data['ip'] = get_ip_address(result['data']['ip'])
        data['reverseclient'] = result['data']['reverseclient']
        data['clienttime'] = clienttime
        data['servertime'] = datetime.strptime(result['data']['servertime'], "%Y-%m-%dT%H:%M:%S.%f")
        data['type'] = 'client'
        if args.shelvefile: d[data['servertime'].isoformat()] = data
    except KeyError:
        sys.stderr.write("Response seems to be incorrect.\n")
        sys.stderr.write(str(result))
        sys.stderr.write("\n")
        sys.exit(3)
    finally:
        if args.shelvefile: d.close()

if __name__ == '__main__':
    main()

