# actproxy

Python package providing [actproxy.com](https://actproxy.com/aff.php?aff=30) API access and proxy rotation methods for requests (synchronous) and aiohttp
(asyncio). Can also be used independently. Supports socks5, http/https, and ipv4/ipv6 as per actproxy's services.

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.org/project/actproxy/)

## Quick-Start (AIOHTTP)

```python
import actproxy
from aiohttp import ClientSession


async def main():
    actproxy_api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
    # Initialize API. Also returns your proxies.
    await actproxy.aioinit(actproxy_api_key)
    # Use a new AIOHTTP connector which rotates & uses the next proxy.
    async with ClientSession(connector=actproxy.aiohttp_rotate()) as session:
        url = "http://dummy.restapiexample.com/api/v1/employees"
        async with session.get(url) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                print(resp_json)
```

## Quick-Start (Requests)

```python
import actproxy
import requests

actproxy_api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
# Initialize API. Also returns your proxies.
actproxy.init(actproxy_api_key)
url = "http://dummy.restapiexample.com/api/v1/employees"
resp = requests.get(url, proxies=actproxy.rotate())
if resp.status_code == 200:
    resp_json = resp.json()
    print(resp_json)
```

## Methods

`actproxy.aioinitaioinit(api_keys=[], output_format='json', get_userpass=True)`: Fetches your proxies from ActProxy & returns them. Must be run before the other aiohttp
functions.

`actproxy.initinit(api_keys=[], output_format='json', get_userpass=True)`: Fetches your proxies from ActProxy & returns
them. Must be run before the other synchronous functions.

`actproxy.aiohttp_rotate(protocol='socks5')`: Returns an aiohttp connector which uses the next proxy from your list.

`actproxy.rotate(protocol='socks5')`: Returns the next proxy from your list. Return variable is suitable for use with requests[socks].

`actproxy.random_proxy(protocol='socks5')`: Returns a random proxy from your list. Return variable is suitable for use with
requests[socks].

`actproxy.aiohttp_random(protocol='socks5')`: Returns an aiohttp connector which uses uses a random proxy from your list.

`actproxy.one_hot_proxy()`: Similar to rotate() but returns a single proxy dict/object for use in places other than
aiohttp or requests.

## Changelog

**0.1.3** - _9/29/2020_ : Minor fixes and addition of docstrings.

**0.1.2** - _9/28/2020_ : Initial release version.