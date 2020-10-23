from aiohttp import ClientSession
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector, ProxyError, \
	ProxyConnectionError, ProxyTimeoutError
from mo_dots import to_data, Data, DataObject, Null, NullType, FlatList, LIST
from random import randrange
import requests
from typing import Union, Any

proxies, one_hot = [], []
has_init = False


class ActError(Exception):
	""" General ActProxy exception. ActProxy also exports aiohttp[socks] exceptions: ProxyError, ProxyConnectionError,
	ProxyTimeoutError"""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def act_parse_json(proxy_items: list) -> Union[list, None]:
	"""
	Parse the proxy list JSON supplied by ActProxy API.
		:rtype: Union[list, None]
		:type proxy_items: list
		:param proxy_items: List of proxy lines returned from ActProxy API.
		:return: List of mo-dots dict objects containing proxies.
	"""
	_proxies = []
	for line in proxy_items:
		line_spl = line.split(';')
		host_spl = line_spl[0].split(':')
		if len(host_spl) >= 2:
			_proxies.append({
				'host': host_spl[0],
				'port': host_spl[1],
				'username': line_spl[1],
				'password': line_spl[2]
			})
	return _proxies


def init(api_keys: list, output_format='json', get_userpass=True) -> Union[list, None]:
	"""
	Synchronously initialize ActProxy API & return proxies from account.
		:rtype: Union[list, None]
		:param api_keys: List of ActProxy.com API keys.
		:param output_format: 'json' or 'raw'; must be 'json' to use connectors.
		:param get_userpass: Include usernames & passwords in results? Must be True to use connectors.
		:return: A list of proxies as mo-dots objects if proxies are available. None if not.
	"""
	global proxies, one_hot, has_init
	if api_keys is None:
		api_keys = []
		raise ValueError('api_keys must be a list containing at least one API key')
	userpass = 'true' if get_userpass else 'false'
	formatter = '&format=json' if output_format == 'json' else ''
	proxies = []
	proxies_csv = ''
	for key_num, api_key in enumerate(api_keys):
		api_url = f'https://actproxy.com/proxy-api/{api_key}?userpass={userpass}{formatter}'
		resp = requests.get(api_url)
		if resp.status_code == 200:
			if output_format == 'json':
				proxy_items = resp.json()
			else:
				proxy_items = resp.text.splitlines()
				proxies_csv += resp.text
			_proxies = act_parse_json(proxy_items)
			if isinstance(_proxies, list) and len(_proxies):
				proxies.extend(_proxies)
				has_init = True
			else:
				raise TypeError(f"ActProxy API Key #{key_num} didn't return a proxy list")
		else:
			raise ActError(f"HTTP error {resp.status_code} contacting ActProxy.")
	if output_format == 'json':
		one_hot = [0 for p in proxies]
		return to_data(proxies) or None
	else:
		return proxies_csv or None


async def aioinit(api_keys: list = None, output_format='json', get_userpass=True) -> Data:
	"""
	Asynchronously initialize ActProxy API & return proxies from account.
		:param api_keys: List of ActProxy.com API keys.
		:param output_format: 'json' or 'raw'; must be 'json' to use connectors.
		:param get_userpass: Include usernames & passwords in results? Must be True to use connectors.
		:return: A mo-dots object (Eg: proxies[0].username or proxies[0]['username']) in the case of 'json' as
				output_format. A Str in case of 'raw' as output_format.
	"""
	global proxies, one_hot, has_init
	if api_keys is None:
		api_keys = []
		raise ValueError('api_keys must be a list containing at least one API key')
	async with ClientSession() as session:
		userpass = 'true' if get_userpass else 'false'
		formatter = '&format=json' if output_format == 'json' else ''
		proxies = []
		proxies_csv = ''
		for key_num, api_key in enumerate(api_keys):
			api_url = f'https://actproxy.com/proxy-api/{api_key}?userpass={userpass}{formatter}'
			async with session.get(api_url) as resp:
				if resp.status == 200:
					if output_format == 'json':
						proxy_items = await resp.json(content_type=None)
						_proxies = act_parse_json(proxy_items)
						if isinstance(_proxies, list) and len(_proxies):
							proxies.extend(_proxies)
							has_init = True
						else:
							raise TypeError(f"ActProxy API Key #{key_num} didn't return a proxy list")
					else:
						proxies_csv += await resp.text()
				else:
					raise ActError(f"HTTP error {resp.status} contacting ActProxy.")
		if output_format == 'json':
			one_hot = [0 for p in proxies]
			return to_data(proxies) or None
		else:
			proxy_lines = proxies_csv.splitlines()
			return to_data(proxy_lines) if len(proxy_lines) else None


def rotate(protocol='socks5'):
	"""
	Get the next proxy in the one-hot rotation for use with the requests[socks] package after having once run
	actproxy.init(output_format='json').
		:param protocol: 'socks5' or 'http'; must correspond to your ActProxy proxies' type.
		:return: Dict formatted for use in the requets[socks] package's proxies= parameter.
	"""
	proxy = one_hot_proxy()
	requests_proxy = {
		'http': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}',
		'https': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}'
	}
	return to_data(requests_proxy)


def aiohttp_rotate(protocol: str = 'socks5', return_proxy: Any = False) -> Union[ProxyConnector, tuple]:
	"""
	Get an aiohttp connector that uses the next proxy in the one-hot rotation after having once run
	actproxy.aioinit(output_format='json').
		:param protocol: 'socks5' or 'http'; must correspond to your ActProxy proxies' type.
		:param return_proxy: Boolean; Return tuple(proxy, ProxyConnector) instead of just ProxyConnector.
		:return: An aiohttp connector set to use the next proxy.
	"""
	proxy = one_hot_proxy()
	proxy_connector = ProxyConnector.from_url(
		f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}'
	)
	return proxy, proxy_connector if return_proxy else proxy_connector


def random_proxy(protocol: str = 'socks5') -> Data:
	"""
	Get a random proxy from your account after having once run actproxy.init(output_format='json') or
	actproxy.aioinit(output_format='json')
		:param protocol: 'socks5' or 'http'; must be the same as your ActProxy proxies.
		:return: A random proxy Data (Dict-like) object.
	"""
	global proxies
	last_prox = len(proxies) - 1
	rand_prox = randrange(0, last_prox)
	proxy = to_data(proxies[rand_prox])
	return to_data({
		'http': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}',
		'https': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}'
	})


def aiohttp_random(protocol='socks5', return_proxy: Any = False) -> Union[ProxyConnector, tuple]:
	"""
	Get a random aiohttp connector after having once run actproxy.aioinit(output_format='json')
		:param protocol: 'socks5' or 'http'; must be the same as your ActProxy proxies.
		:param return_proxy: Boolean; Return tuple(proxy, ProxyConnector) instead of just ProxyConnector.
		:return: ProxyConnector or tuple(proxy: Data, proxy_connector: ProxyConnector)
	"""
	proxy = random_proxy(protocol)
	proxy = proxy.https
	proxy_connector = ProxyConnector.from_url(proxy)
	return proxy, proxy_connector if return_proxy else proxy_connector


def one_hot_proxy():
	"""
	Get the next proxy in the one-hot rotation and flip the next proxy bit hot.
		:return: mo-dots (Dict-like) object containing the proxy's various parameters.
	"""
	global one_hot, proxies
	if not has_init:
		raise ActError("First, run actproxy.init() or actproxy.aioinit()")
	if not len(proxies):
		raise ActError('No proxies available. Check connection or ActProxy account.')
	hlen = len(one_hot) - 1
	hdex = 0
	try:
		hdex = one_hot.index(1)
	except ValueError:
		pass
	one_hot[hdex] = 0
	if hlen == hdex:
		one_hot[0] = 1
	else:
		one_hot[hdex + 1] = 1
	return to_data(proxies[hdex])
