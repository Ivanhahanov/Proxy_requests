import urllib.request as urllib
import requests
import certifi

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


def request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib.ProxyHandler({'https': '102.65.157.113:8080'})
        opener = urllib.build_opener(proxy_support)
        urllib.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request = urllib.Request(url, None, headers)
    return urllib.urlopen(request, cafile=certifi.where()).read()

# This time, rather than install the OpenerDirector, we use it directly:
print(request('http://icanhazip.com/'))
#print(requests.get('https://2ip.ru/',headers=headers, proxies={'https': 'socks5://127.0.0.1:9050'}).text)
from stem import Signal
from stem.control import Controller

import requests
proxies = {
    'http': 'socks5://localhost:9050',
    'https': 'socks5://localhost:9050'
}

def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()

renew_connection()
url = 'https://courses.digitaleconomy.world/'
print(requests.get(url, proxies=proxies).text)
print(requests.get('http://icanhazip.com/', proxies=proxies).text)
