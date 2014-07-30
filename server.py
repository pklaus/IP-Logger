#!/usr/bin/env python

from bottle import route, run, request
from datetime import datetime
from ipaddress import ip_address
import argparse
import shelve
import hashlib

parser = argparse.ArgumentParser(description='IP Logger Server - Logging the remote IP addresses of trusted clients.')
parser.add_argument('shelvefile', help='The file to store previous requests in.')
parser.add_argument('--server-secret', '-s', help='The secret code of this server.')
args = parser.parse_args()

d = shelve.open(args.shelvefile)
print("Currently stored entries: {}".format(len(d)))
#from pprint import pprint
#for el in list(d):
#    pprint(d[el])

@route('/log')
def log():
    try:
        name = request.query.name
        salt = request.query.salt
        auth = request.query.auth
        authbytes = (salt + args.server_secret).encode('utf-8')
        if not auth == hashlib.sha512(authbytes).hexdigest():
            raise NameError('Auth code incorrect.')
        messagesig = request.query.messagesig
        clienttime = request.query.time
        servertime = datetime.now()
        ip = ip_address(request.remote_addr)
        dataset = dict(name=name, salt=salt, messagesig=messagesig, auth=auth, clienttime=clienttime, servertime=servertime, ip=ip)
        d[servertime.isoformat()] = dataset
    except Exception as ex:
        return {'message': 'NAK', 'exception': str(ex)}
    return {'message': 'OK'}

run(host='localhost', port=2000)

d.close()

