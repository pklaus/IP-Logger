
import socket
from ipaddress import IPv4Address, ip_address

def reverse_entry_for(host):
    try:
        addr = socket.gethostbyname(host)
    except:
        addr = host
    return socket.gethostbyaddr(addr)[0]

def get_ip_address(text):
    ip = ip_address(text)
    if not hasattr(ip, 'ipv4_mapped'): return ip
    if ip.ipv4_mapped:
        return ip.ipv4_mapped
    else:
        return ip

