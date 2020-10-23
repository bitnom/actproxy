from aiohttp import ClientSession
import toml
import actproxy
from actproxy import Data, Null, FlatList, ProxyConnector

store = toml.load('secrets.toml')
ACT_KEYS = [
	store['act']['api_keys'][0],
	store['act']['api_keys'][1]
]
INITIALIZED = False
ECHO_URL = 'https://ipecho.net/plain'


async def test_init():
	global INITIALIZED
	api_resp = await actproxy.aioinit(ACT_KEYS)
	assert api_resp not in (None, Null)
	assert isinstance(api_resp, FlatList)
	assert len(api_resp) > 0
	assert isinstance(api_resp[0], Data)
	assert 'host' in api_resp[0] and 'port' in api_resp[0] \
	       and 'username' in api_resp[0] and 'password' in api_resp[0]
	INITIALIZED = True


async def test_aiohttp_rotate():
	global INITIALIZED
	assert INITIALIZED is True
	proxy, proxy_connector = actproxy.aiohttp_rotate(return_proxy=True)
	assert isinstance(proxy_connector, ProxyConnector)
	assert isinstance(proxy, Data)
	async with ClientSession(connector=proxy_connector, requote_redirect_url=False) as _session:
		async with _session.get(ECHO_URL, max_redirects=30) as _resp:
			assert _resp.status == 200
			remote_ip = await _resp.text()
			assert remote_ip == proxy.host


async def test_aiohttp_random():
	global INITIALIZED
	assert INITIALIZED is True
	proxy, proxy_connector = actproxy.aiohttp_random(return_proxy=True)
	assert isinstance(proxy_connector, ProxyConnector)
	assert isinstance(proxy, str)
	async with ClientSession(connector=proxy_connector, requote_redirect_url=False) as _session:
		async with _session.get(ECHO_URL, max_redirects=30) as _resp:
			assert _resp.status == 200
			remote_ip = await _resp.text()
			assert remote_ip in proxy
