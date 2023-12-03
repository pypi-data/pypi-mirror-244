"""
Get your own ip address

Example:
  import getownip
  print("public IPv4: " + getownip.get(getownip.Public, getownip.IPv4))
  print("local IPv6: " + getownip.get(getownip.Local, getownip.IPv6))

To retrieve a local ip address, a default route must exist. Otherwise, None is returned.

When retrieving a public ip address, a random one of a list of servers is accessed.
Currently, the following list of servers is used:

| service       | IPv4 | IPv6 |
|---------------|------|------|
| getmyip.dev   |  yes |  yes |
| icanhazip.com |  yes |  yes |
| ident.me      |  yes |  yes |
| ipaddress.com |  yes |      |
| ipext.org     |  yes |  yes |
| ipify.org     |  yes |  yes |
| ipinfo.io     |  yes |      |
| ipy.ch        |  yes |      |
| l2.io         |  yes |      |
| meineipv6.de  |  yes |  yes |
| my-ip.io      |  yes |  yes |
| seeip.org     |  yes |  yes |
| tnedi.me      |  yes |  yes |

If one of these services fails to answer, another one will be tried until every service has failed.
In this case, the last occurred exception will be thrown.
"""

import enum, random, re, socket, urllib.request

class IPVersion(enum.Enum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"
IPv4 = IPVersion.IPv4
IPv6 = IPVersion.IPv6

class IPType(enum.Enum):
    Local = "Local"
    Public = "Public"
Local = IPType.Local
Public = IPType.Public

def _is_ipv4_valid(s):
    if not re.match('^([1-9][0-9]*\\.){3}[1-9][0-9]*$', s):
        return False
    parts = [int(p) for p in s.split(".")]
    for p in parts:
        if p >= 256:
            return False
    return True

def _is_ipv6_valid(s):
    parts = s.split(":")
    if len(parts) < 2 or len(parts) > 8:
        return False
    empties = sum(part == "" for part in parts)
    if empties > 1:
        return False
    if empties == 0 and len(parts) < 8:
        return False
    for part in parts:
        if not re.match('^[0-9a-f]{0,4}$', part):
            return False

def _get_local_ip(ip_version):
    if ip_version is IPv4:
        socket_type = socket.AF_INET
        target_ip = "192.0.2.1"
    elif ip_version is IPv6:
        socket_type = socket.AF_INET6
        target_ip = "100::1"
    else:
        raise ValueError("ip_version must bei either IPv4 or IPv6")
    with socket.socket(socket_type, socket.SOCK_DGRAM) as s:
        try:
            s.connect((target_ip, 1))
        except OSError as e:
            if e.errno == 101:
                # "Network is unreachable"
                # -> No ip address (or no default route) available
                return None
        return s.getsockname()[0]

_ipv4_endpoints = (
    "https://ipv4.getmyip.dev/",
    "http://ipv4.icanhazip.com/",
    "http://4.ident.me/",
    "http://api.ipaddress.com/myip",
    "https://api4.ipext.org/",
    "http://api.ipify.org/",
    "http://ipinfo.io/ip",
    "http://api.ipy.ch/",
    "http://www.l2.io/ip",
    "http://v4only.meineipv6.de/mro.php?format=plaintext",
    "https://api4.my-ip.io/v1/ip",
    "https://ipv4.seeip.org/",
    "http://4.tnedi.me/",
)
_ipv6_endpoints = (
    "https://ipv6.getmyip.dev/",
    "http://ipv6.icanhazip.com/",
    "http://6.ident.me/",
    "https://api6.ipext.org/",
    "http://api6.ipify.org/",
    "http://v6only.meineipv6.de/mro.php?format=plaintext",
    "https://api6.my-ip.io/v1/ip",
    "https://ipv6.seeip.org/",
    "http://6.tnedi.me/",
)

def _get_public_ip(ip_version):
    if ip_version is IPv4:
        endpoints = list(_ipv4_endpoints)
        addr_family = socket.AF_INET
    elif ip_version is IPv6:
        endpoints = list(_ipv6_endpoints)
        addr_family = socket.AF_INET6
    else:
        raise ValueError("ip_version must bei either IPv4 or IPv6")
    random.shuffle(endpoints)
    err = None
    for endpoint in endpoints:
        try:
            res=urllib.request.urlopen(endpoint, timeout=10)
            ip_addr = res.read().decode().strip()
            socket.inet_pton(addr_family, ip_addr)
            return ip_addr
        except Exception as e:
            # URLError with errno 101 means "Network is unreachable"
            # This could mean that no ip of the given version is available.
            # If this error occurs for all targets, this is likely the cause.
            if not isinstance(e, urllib.error.URLError) or e.reason.errno != 101:
                err = e
    if err is None:
        return None
    raise err

def get(ip_type, ip_version):
    """
    Get your own ip address.

    ip_type must be one of:
      getownip.Local:  Get the ip address assigned to this machine, which may be a local address behind a NAT.
                       Note, that a default gateway is still needed, otherwise None is returned.
      getownip.Public: Get the global ip address this machine uses to interact with servers over the internet.
                       For this operation to succeed, an internet connection is required. Otherwise, an exception will be thrown.

    ip_version must be one of:
      getownip.IPv4
      getownip.IPv6
    (depending on the desired ip address version)
    """
    if ip_type is Local:
        return _get_local_ip(ip_version)
    elif ip_type is Public:
        return _get_public_ip(ip_version)
    else:
        raise ValueError("ip_type must bei either Local or Public")
