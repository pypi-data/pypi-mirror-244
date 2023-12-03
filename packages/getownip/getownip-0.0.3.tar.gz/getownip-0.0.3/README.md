# getownip - A python script to determine your ip address

Example:

```python
import getownip
print("public IPv4: " + getownip.get(getownip.Public, getownip.IPv4))
print("local IPv6: " + getownip.get(getownip.Local, getownip.IPv6))
```

To retrieve a local ip address, a default route must exist. Otherwise, `None` is returned.

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
