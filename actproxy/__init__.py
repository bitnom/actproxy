from aiohttp import ClientSession
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector, ProxyError, \
	ProxyConnectionError, ProxyTimeoutError
from mo_dots import to_data
from random import randrange
import requests

proxies, one_hot = [], []
has_init = False


class ActError(Exception):
	""" General ActProxy exception. ActProxy also exports aiohttp[socks] exceptions: ProxyError, ProxyConnectionError,
	ProxyTimeoutError"""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def act_parse_json(proxy_items):
	"""
	Parse the proxy list JSON supplied by ActProxy API.
		:param proxy_items: List of proxy lines returned from ActProxy API.
		:return: List of dicts containing proxies.
	"""
	_proxies = []
	for line in proxy_items:
		line_spl = line.split(';')
		host_spl = line_spl[0].split(':')
		if len(host_spl) >= 3:
			_proxies.append({
				'host': host_spl[0],
				'port': host_spl[1],
				'username': line_spl[1],
				'password': line_spl[2]
			})
	return _proxies


def init(api_keys=[], output_format='json', get_userpass=True):
	"""
	Synchronously initialize ActProxy API & return proxies from account.
		:param api_key: ActProxy.com API key.
		:param output_format: 'json' or 'raw'; must be 'json' to use connectors.
		:param get_userpass: Include usernames & passwords in results? Must be True to use connectors.
		:return: A mo-dots object (Eg: proxies[0].username or proxies[0]['username']) in the case of 'json' as
				output_format. A Str in case of 'raw' as output_format.
	"""
	global proxies, one_hot, has_init
	userpass = 'true' if get_userpass else 'false'
	formatter = '&format=json' if output_format == 'json' else ''
	proxies = []
	proxies_csv = ''
	for api_key in api_keys:
		api_url = f'https://actproxy.com/proxy-api/{api_key}?userpass={userpass}{formatter}'
		resp = requests.get(api_url)
		if resp.status_code == 200:
			if output_format == 'json':
				proxy_items = resp.json()
				_proxies = act_parse_json(proxy_items)
				if len(proxies):
					proxies.append(_proxies)
					has_init = True
			else:
				proxies_csv += resp.text
		else:
			raise ActError(f"HTTP error {resp.status_code} contacting ActProxy.")
	if output_format == 'json':
		one_hot = [0 for p in proxies]
		return to_data(proxies) if len(proxies) else None
	else:
		return proxies_csv


async def aioinit(api_keys=[], output_format='json', get_userpass=True):
	"""
	Asynchronously initialize ActProxy API & return proxies from account.
		:param api_key: ActProxy.com API key.
		:param output_format: 'json' or 'raw'; must be 'json' to use connectors.
		:param get_userpass: Include usernames & passwords in results? Must be True to use connectors.
		:return: A mo-dots object (Eg: proxies[0].username or proxies[0]['username']) in the case of 'json' as
				output_format. A Str in case of 'raw' as output_format.
	"""
	global proxies, one_hot, has_init
	async with ClientSession() as session:
		userpass = 'true' if get_userpass else 'false'
		formatter = '&format=json' if output_format == 'json' else ''
		proxies = []
		proxies_csv = ''
		for api_key in api_keys:
			api_url = f'https://actproxy.com/proxy-api/{api_key}?userpass={userpass}{formatter}'
			async with session.get(api_url) as resp:
				if resp.status == 200:
					if output_format == 'json':
						proxy_items = await resp.json(content_type=None)
						_proxies = act_parse_json(proxy_items)
						if len(_proxies):
							proxies.append(_proxies)
							has_init = True
					else:
						proxies_csv += await resp.text()
				else:
					raise ActError(f"HTTP error {resp.status} contacting ActProxy.")
		if output_format == 'json':
			one_hot = [0 for p in proxies]
			return to_data(proxies) if len(proxies) else None
		else:
			return proxies_csv


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
	return requests_proxy


def aiohttp_rotate(protocol='socks5'):
	"""
	Get an aiohttp connector that uses the next proxy in the one-hot rotation after having once run
	actproxy.aioinit(output_format='json').
		:param protocol: 'socks5' or 'http'; must correspond to your ActProxy proxies' type.
		:return: An aiohttp connector set to use the next proxy.
	"""
	proxy = one_hot_proxy()
	return ProxyConnector.from_url(f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}')


def random_proxy(protocol='socks5'):
	"""
	Get a random proxy from your account after having once run actproxy.init(output_format='json') or
	actproxy.aioinit(output_format='json')
		:param protocol: 'socks5' or 'http'; must be the same as your ActProxy proxies.
		:return: A random proxy mo-dots (Dict-like) object.
	"""
	global proxies
	last_prox = len(proxies) - 1
	rand_prox = randrange(0, last_prox)
	proxy = proxies[rand_prox]
	requests_proxy = {
		'http': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}',
		'https': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}'
	}
	return requests_proxy


def aiohttp_random(protocol='socks5'):
	"""
	Get a random aiohttp connector after having once run actproxy.aioinit(output_format='json')
		:param protocol: 'socks5' or 'http'; must be the same as your ActProxy proxies.
		:return:
	"""
	proxy = random_proxy()
	return ProxyConnector.from_url(f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}')


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
