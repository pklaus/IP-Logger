#!/usr/bin/env python

try:
    from bottle import Bottle, route, run, request, abort
    ext_deps = True
except ImportError:
    ext_deps = False
from datetime import datetime
from ipaddress import ip_address
import argparse
import shelve
import hmac
import sys
import traceback
from tools import reverse_lookup, get_ip_address

if not ext_deps:
    sys.stderr.write("Missing external dependency: bottle. Please install it first.\n")
    sys.exit(2)

DATA = None
SERVER_SECRET = None
DEBUG = False

app = Bottle()

@app.route('/log')
def log():
    try:
        name = request.query.name
        salt = request.query.salt
        auth = request.query.auth
        if not hmac.compare_digest(auth, hmac.new(SERVER_SECRET.encode('utf-8'), salt.encode('utf-8'), digestmod='sha1').hexdigest()):
            raise NameError('Auth code incorrect.')
        messagesig = request.query.messagesig
        clienttime = request.query.clienttime
        host = request.query.host
        hostip = get_ip_address(request.query.hostip)
        reversehost = request.query.reversehost
        clienttime = datetime.strptime(clienttime, "%Y-%m-%dT%H:%M:%S.%f")
        servertime = datetime.utcnow()
        ip = get_ip_address(request.remote_addr)
        reverseclient = reverse_lookup(str(ip))
        dataset = dict(host=host, reversehost=reversehost, hostip=hostip, name=name, salt=salt, messagesig=messagesig, auth=auth, clienttime=clienttime, servertime=servertime, ip=ip, reverseclient=reverseclient, type='server')
        DATA[servertime.isoformat()] = dataset
    except Exception as ex:
        if DEBUG:
            tb = traceback.format_exc()
            return {'success': False, 'exception': "{}: {}\n{}".format(type(ex), ex, tb)}
        else:
            return {'success': False, 'exception': "{}".format(ex)}
    # customizations of the dataset to be returned to client:
    del dataset['clienttime']
    dataset['servertime'] = servertime.isoformat()
    dataset['ip'] = request.remote_addr
    dataset['hostip'] = request.query.hostip
    return {'success': True, 'data': dataset }

@app.route('/list/by/<grouped>')
def list_log_entries(grouped):
    if grouped not in ('ip', 'name'): abort(404, 'Requested grouping not supported')
    by_ip = dict()
    for key in DATA:
        d = DATA[key]
        d['clienttime'] = d['clienttime'].isoformat()
        d['servertime'] = d['servertime'].isoformat()
        d['hostip'] = str(d['hostip'])
        d['ip'] = str(d['ip'])
        try:
            by_ip[d[grouped]].append(d)
        except KeyError:
            by_ip[d[grouped]] = [d]
    return dict(entries=by_ip)

def main():

    global SERVER_SECRET, DATA, DEBUG

    parser = argparse.ArgumentParser(description='IP Logger Server - Logging the remote IP addresses of trusted clients.')
    parser.add_argument('shelvefile', help='The file to store previous requests in.')
    parser.add_argument('--server-secret', metavar='R@Nd0MK3y', help='The secret code of this server.', required=True)
    parser.add_argument('--server-adapter', metavar='wsgiref', default='wsgiref', help='Which server to run this web app with. Depends on 3rd party Python modules.  If you need IPv6, try "cherrypy".')
    parser.add_argument('--host', metavar='0.0.0.0', default='0.0.0.0', help='The host/IP to bind the server to. Use "::" for IPv6.')
    parser.add_argument('--port', metavar=2000, default=2000, type=int, help='The port the server should listen at. Default: 2000.')
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode.')

    args = parser.parse_args()

    DEBUG = args.debug
    SERVER_SECRET = args.server_secret
    DATA = shelve.open(args.shelvefile)
    print("Currently stored entries: {}".format(len(DATA)))
    
    run(app, server=args.server_adapter, host=args.host, port=args.port, debug=DEBUG)
    
    DATA.close()

if __name__ == '__main__':
    main()

