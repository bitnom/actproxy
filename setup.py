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
    'version': '0.1.0',
    'description': "Interface to actproxy.com's API and services.",
    'long_description': None,
    'author': 'TensorTom',
    'author_email': '14287229+TensorTom@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
