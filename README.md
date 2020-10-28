# actproxy

Python package providing [actproxy.com](https://actproxy.com/aff.php?aff=30) API access and proxy rotation methods for requests (synchronous) and aiohttp
(asyncio). Can also be used independently. Supports socks5, http/https, and ipv4/ipv6 as per actproxy's services.

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.org/project/actproxy/)

## Quick-Start (AIOHTTP)

```python
import actproxy
from aiohttp import ClientSession


async def main():
    actproxy_api_keys = [
        "xxxxxxxxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxxxxxxxx"
    ]
    # Initialize API. Also returns your proxies.
    await actproxy.aioinit(actproxy_api_keys)
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

actproxy_api_keys = [
    "xxxxxxxxxxxxxxxxxxxxxxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxx"
]
# Initialize API. Also returns your proxies.
actproxy.init(actproxy_api_keys)
url = "http://dummy.restapiexample.com/api/v1/employees"
resp = requests.get(url, proxies=actproxy.rotate())
if resp.status_code == 200:
    resp_json = resp.json()
    print(resp_json)
```

## Methods

```python
actproxy.aioinit(api_keys: List = None, output_format: DumpFormat = 'json', get_userpass: Boolean = True) -> Union[FlatList, str, None]
```

Fetches your proxies from ActProxy & returns them. Must be run before the other aiohttp
functions.

```python
actproxy.init(api_keys: List[str], output_format: DumpFormat = 'json', get_userpass: Any = True) -> Union[FlatList, str, None]
```

Fetches your proxies from ActProxy & returns
them. Must be run before the other synchronous functions.

```python
actproxy.aiohttp_rotate(protocol: ProxyProto = return_proxy: Boolean = False) -> Union[ProxyConnector, Tuple[Data, ProxyConnector]]
```

Returns an aiohttp connector which uses the next proxy from your list.

```python
actproxy.rotate(protocol: ProxyProto = 'socks5') -> Data
```
Returns the next proxy from your list. Return variable is suitable for use with requests[socks].

```python
actproxy.random_proxy(protocol: ProxyProto = 'socks5') -> Data
```

Returns a random proxy from your list. Return variable is suitable for use with
requests[socks].

```python
actproxy.aiohttp_random(protocol: ProxyProto = 'socks5', return_proxy: Boolean = False) -> Union[ProxyConnector, Tuple[Data, ProxyConnector]]
```

Returns an aiohttp connector which uses uses a random proxy from your list.

```python
actproxy.one_hot_proxy() -> Data
```

Similar to rotate() but returns a single proxy dict/object for use in places other than
aiohttp or requests.

## Changelog

**0.1.7** - _10/28/2020_ : Relax Python version constraint (3.8-4.0).

**0.1.6** - _10/24/2020_ : Lock aiohttp version fixing [aiohttp #5112](https://github.com/aio-libs/aiohttp/issues/5112)

**0.1.5** - _10/24/2020_ : Rotator bug fix. CSV fix. Better type-hints & coverage.

**0.1.4** - _10/23/2020_ : Support multiple API keys. Unit tests. Fixes.

**0.1.3** - _9/29/2020_ : Minor fixes and addition of docstrings.

**0.1.2** - _9/28/2020_ : Initial release version.