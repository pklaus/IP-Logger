
import socket
from ipaddress import IPv4Address, ip_address

def lookup(host):
    try:
        return socket.gethostbyname(host)
    except:
        return host

def reverse_lookup(host):
    addr = lookup(host)
    try:
        return socket.gethostbyaddr(addr)[0]
    except:
        return addr

def get_ip_address(text):
    ip = ip_address(text)
    if not hasattr(ip, 'ipv4_mapped'): return ip
    if ip.ipv4_mapped:
        return ip.ipv4_mapped
    else:
        return ip

