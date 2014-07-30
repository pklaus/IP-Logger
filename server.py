#!/usr/bin/env python

try:
    from bottle import route, run, request
    ext_deps = True
except ImportError:
    ext_deps = False
from datetime import datetime
from ipaddress import ip_address
import argparse
import shelve
import hmac
import sys

if not ext_deps:
    sys.stderr.write("Missing external dependency: bottle. Please install it first.\n")
    sys.exit(2)

parser = argparse.ArgumentParser(description='IP Logger Server - Logging the remote IP addresses of trusted clients.')
parser.add_argument('shelvefile', help='The file to store previous requests in.')
parser.add_argument('--server-secret', '-s', help='The secret code of this server.', required=True)
args = parser.parse_args()

d = shelve.open(args.shelvefile)
print("Currently stored entries: {}".format(len(d)))

@route('/log')
def log():
    try:
        name = request.query.name
        salt = request.query.salt
        auth = request.query.auth
        if not hmac.compare_digest(auth, hmac.new(args.server_secret.encode('utf-8'), salt.encode('utf-8'), digestmod='sha1').hexdigest()):
            raise NameError('Auth code incorrect.')
        messagesig = request.query.messagesig
        clienttime = request.query.clienttime
        clienttime = datetime.strptime(clienttime, "%Y-%m-%dT%H:%M:%S.%f")
        servertime = datetime.now()
        ip = ip_address(request.remote_addr)
        dataset = dict(name=name, salt=salt, messagesig=messagesig, auth=auth, clienttime=clienttime, servertime=servertime, ip=ip)
        d[servertime.isoformat()] = dataset
    except Exception as ex:
        return {'success': False, 'exception': str(ex)}
    return {'success': True, 'data': {'ip': request.remote_addr, 'servertime': servertime.isoformat()} }

run(host='0.0.0.0', port=2000)

d.close()

