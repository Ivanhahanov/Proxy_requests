from stem import Signal
from stem.control import Controller
import requests
import time
from bs4 import BeautifulSoup
import random
import logging
logging.basicConfig(filename="proxy.log",
                    level=logging.INFO,
                    datefmt='%I:%M:%S',
                    format='%(asctime)s %(message)s')

url = 'https://courses.digitaleconomy.world/'
ip_num = 10
proxies = {
    'http': 'socks5://localhost:9050',
    'https': 'socks5://localhost:9050'
}

newIP = '0.0.0.0'
secondsBetweenChecks = 2

def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()
        
def request(new_url, method='GET', **kwargs):
    if method == 'GET':
        return requests.get(new_url, proxies=proxies).text
    elif method == 'POST':
        return requests.post(new_url, params=kwargs, proxies=proxies).text

def show_ip(site):
    soup = BeautifulSoup(site, features="html.parser")
    ip = soup.find("div", {"class": "ip"})
    return ip.getText()

def generate_phone():
    return '8' + ''.join(random.randint(9) for _ in range(10))

for i in range(0, ip_num):
    renew_connection()
    oldIP = newIP
    newIP = show_ip(request('https://hidemy.name/ru/ip/'))
    seconds = 0
    while oldIP == newIP:
        time.sleep(secondsBetweenChecks)
        seconds += secondsBetweenChecks
        newIP = show_ip(request('https://hidemy.name/ru/ip/'))

        if seconds > 40:
            logging.critical('Seconds: %d' % seconds)
        elif seconds > 20:
            logging.warning('To many seconds: %d', seconds)
        print('Waiting for new IP address [ %d sec ]' % seconds)

    print()
    logging.info('IP: %s' % newIP)
    print('newIP: %s' % newIP)
    # You can send post and get requests by using request() function
    # request(url, method, args)
