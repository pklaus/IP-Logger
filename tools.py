
import socket
from ipaddress import ip_address

def lookup(host, family=0):
    """
    Lookup hostname and resolve to IP address.

    You can restrict the lookup to IPv4 or IPv6 by setting
    family to socket.AF_INET or socket.AF_INET6.
    """
    try:
        addrinfo = socket.getaddrinfo(host, 'http', family=family)
        return addrinfo[0][4][0]
    except:
        return host

def reverse_lookup(host, family=0):
    """
    Do a reverse lookup (rDNS).

    But first, we try a forward lookup, in case
    you gave us a host name, not an IP address.
    For the forward lookup you can again specify
    the family to search for IPv4/IPv6.
    """
    addr = lookup(host, family=0)
    try:
        return socket.gethostbyaddr(addr)[0]
    except:
        return addr

def get_ip_address(text):
    """
    This is my wrapper for ipaddress.ip_address().

    If it finds that an IPv4-mapped IPv6 was created,
    it returns it's IPv4 equivalent.
    """
    ip = ip_address(text)
    if not hasattr(ip, 'ipv4_mapped'): return ip
    if ip.ipv4_mapped:
        return ip.ipv4_mapped
    else:
        return ip

def get_netloc(host, port):
    try:
        hostip = ip_address(host)
        if hostip.version == 6:
            host = "[{}]".format(hostip)
        else:
            host = str(hostip)
    except:
        pass
    return "{}:{}".format(host, port)

