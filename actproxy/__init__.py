from aiohttp import ClientSession
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector, ProxyError, \
	ProxyConnectionError, ProxyTimeoutError
from mo_dots import to_data
from random import randrange
import requests

proxies, one_hot = [], []
has_init = False


class ActError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def act_parse_json(proxy_items):
	global one_hot, proxies
	for line in proxy_items:
		line_spl = line.split(';')
		host_spl = line_spl[0].split(':')
		proxies.append({
			'host': host_spl[0],
			'port': host_spl[1],
			'username': line_spl[1],
			'password': line_spl[2]
		})
	one_hot = [0 for p in proxies]
	return proxies


def init(api_key, output_format='json', get_userpass=True):
	global proxies, one_hot, has_init
	has_init = True
	userpass = 'true' if get_userpass else 'false'
	api_url = f'https://actproxy.com/proxy-api/{api_key}?format={output_format}&userpass={userpass}'
	resp = requests.get(api_url)
	if resp.status_code == 200:
		proxy_items = resp.json()
		proxies = act_parse_json(proxy_items)
		return to_data(proxies) if len(proxies) else None
	else:
		raise ActError(f"HTTP error {resp.status_code} contacting ActProxy.")


async def aioinit(api_key, output_format='json', get_userpass=True):
	global proxies, one_hot, has_init
	has_init = True
	userpass = 'true' if get_userpass else 'false'
	async with ClientSession() as session:
		api_url = f'https://actproxy.com/proxy-api/{api_key}?format={output_format}&userpass={userpass}'
		async with session.get(api_url) as resp:
			if resp.status == 200:
				proxy_items = await resp.json(content_type=None)
				proxies = act_parse_json(proxy_items)
				return to_data(proxies) if len(proxies) else None
			else:
				raise ActError(f"HTTP error {resp.status} contacting ActProxy.")


def rotate(protocol='socks5'):
	proxy = one_hot_proxy()
	requests_proxy = {
		'http': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}',
		'https': f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}'
	}
	return requests_proxy


def aiohttp_rotate(protocol='socks5'):
	proxy = one_hot_proxy()
	return ProxyConnector.from_url(f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}')


def random_proxy():
	global proxies
	last_prox = len(proxies) - 1
	rand_prox = randrange(0, last_prox)
	return proxies[rand_prox]


def aiohttp_random(protocol='socks5'):
	proxy = random_proxy()
	return ProxyConnector.from_url(f'{protocol}://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.port}')


def one_hot_proxy():
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
