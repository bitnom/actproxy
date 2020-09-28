# actproxy (Python Package)

This Python package provides actproxy API access and proxy rotation methods for requests (synchronous) and aiohttp
(asyncio).

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
await actproxy.aioinit(actproxy_api_key)
url = "http://dummy.restapiexample.com/api/v1/employees"
resp = requests.get(url, proxies=actproxy.rotate())
if resp.status_code == 200:
    resp_json = resp.json()
```

## Methods

`actproxy.aioinit(api_key)`: Fetches your proxies from ActProxy & returns them. Must be run before other aiohttp
functions.

`actproxy.init(api_key)`: Fetches your proxies from ActProxy & returns them. Must be run before other synchronous
functions.

`actproxy.aiohttp_rotate()`: Returns an aiohttp connector which uses the next proxy from your list.

`actproxy.rotate()`: Returns the next proxy from your list. Return variable is suitable for use with requests[socks].

`actproxy.random_proxy()`: Returns a random proxy from your list. Return variable is suitable for use with
requests[socks].

`actproxy.aiohttp_random()`: Returns an aiohttp connector which uses uses a random proxy from your list.

`actproxy.one_hot_proxy()`: Similar to rotate() but returns a single proxy dict/object for use in places other than
aiohttp or requests.