
import socket

def reverse_entry_for(host):
    try:
        addr = socket.gethostbyname(host)
    except:
        addr = host
    return socket.gethostbyaddr(addr)[0]

