# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['actproxy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-socks>=0.5.5,<0.6.0',
 'aiohttp>=3.6.2,<4.0.0',
 'mo-dots>=3.93.20259,<4.0.0',
 'requests[socks]>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['setupgen = poetry.command_line:main']}

setup_kwargs = {
    'name': 'actproxy',
    'version': '0.1.2',
    'description': 'Sync & asyncio (Requests & AIOHTTP) proxy rotator + utils for actproxy API & services.',
    'long_description': '# actproxy (Python Package)\n\nThis Python package provides actproxy API access and proxy rotation methods for requests (synchronous) and aiohttp\n(asyncio).\n\n## Quick-Start (AIOHTTP)\n\n```python\nimport actproxy\nfrom aiohttp import ClientSession\n\n\nasync def main():\n    actproxy_api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"\n    # Initialize API. Also returns your proxies.\n    await actproxy.aioinit(actproxy_api_key)\n    # Use a new AIOHTTP connector which rotates & uses the next proxy.\n    async with ClientSession(connector=actproxy.aiohttp_rotate()) as session:\n        url = "http://dummy.restapiexample.com/api/v1/employees"\n        async with session.get(url) as resp:\n            if resp.status == 200:\n                resp_json = await resp.json()\n                print(resp_json)\n```\n\n## Quick-Start (Requests)\n\n```python\nimport actproxy\nimport requests\n\nactproxy_api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"\n# Initialize API. Also returns your proxies.\nactproxy.init(actproxy_api_key)\nurl = "http://dummy.restapiexample.com/api/v1/employees"\nresp = requests.get(url, proxies=actproxy.rotate())\nif resp.status_code == 200:\n    resp_json = resp.json()\n    print(resp_json)\n```\n\n## Methods\n\n`actproxy.aioinit(api_key)`: Fetches your proxies from ActProxy & returns them. Must be run before other aiohttp\nfunctions.\n\n`actproxy.init(api_key)`: Fetches your proxies from ActProxy & returns them. Must be run before other synchronous\nfunctions.\n\n`actproxy.aiohttp_rotate()`: Returns an aiohttp connector which uses the next proxy from your list.\n\n`actproxy.rotate()`: Returns the next proxy from your list. Return variable is suitable for use with requests[socks].\n\n`actproxy.random_proxy()`: Returns a random proxy from your list. Return variable is suitable for use with\nrequests[socks].\n\n`actproxy.aiohttp_random()`: Returns an aiohttp connector which uses uses a random proxy from your list.\n\n`actproxy.one_hot_proxy()`: Similar to rotate() but returns a single proxy dict/object for use in places other than\naiohttp or requests.',
    'author': 'TensorTom',
    'author_email': '14287229+TensorTom@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TensorTom/actproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
