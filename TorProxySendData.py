#!/usr/bin/python
# -*- coding: utf-8 -*-
import certifi
import stem
import stem.connection

import time
import urllib.request as urllib

from stem import Signal
from stem.control import Controller

import requests
import bs4

# initialize some HTTP headers
# for later usage in URL requests
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}

# initialize some
# holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# how many IP addresses
# through which to iterate?
nbrOfIpAddresses = 3

# seconds between
# IP address checks
secondsBetweenChecks = 2


# request a URL
def request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib.ProxyHandler({"http": "127.0.0.1:8118"})
        opener = urllib.build_opener(proxy_support)
        urllib.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request = urllib.Request(url, None, headers)
    return urllib.urlopen(request).read()


# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()


# cycle through
# the specified number
# of IP addresses via TOR 
for i in range(0, nbrOfIpAddresses):

    # if it's the first pass
    if newIP == "0.0.0.0":
        # renew the TOR connection
        renew_connection()
        # obtain the "new" IP address
        newIP = request("http://icanhazip.com/")
    # otherwise
    else:
        # remember the
        # "new" IP address
        # as the "old" IP address
        oldIP = newIP
        # refresh the TOR connection
        renew_connection()
        # obtain the "new" IP address

        newIP = request("http://icanhazip.com/")

    r = request('https://2ip.ru/')
    print(r)
    # zero the 
    # elapsed seconds    
    seconds = 0

    # loop until the "new" IP address
    # is different than the "old" IP address,
    # as it may take the TOR network some
    # time to effect a different IP address
    while oldIP == newIP:
        # sleep this thread
        # for the specified duration
        time.sleep(secondsBetweenChecks)
        # track the elapsed seconds
        seconds += secondsBetweenChecks
        # obtain the current IP address
        newIP = request("http://icanhazip.com/")
        # signal that the program is still awaiting a different IP address
        print("%d seconds elapsed awaiting a different IP address." % seconds)
    # output the
    # new IP address
    print("")
    print("newIP: %s" % newIP)
    # request = urllib.Request('https://2ip.ru/', None, headers)
    # print(urllib.urlopen(request).read())
    # url = 'https://courses.digitaleconomy.world/'
    # name = 'ksdfjgw'
    # surname = 'al.fhaw'
    # patronymic = 'lefhlc'
    # birthday = ''
    # topics = 'Информатика и вычислительная техника,Прикладная информатика'
    # country = 'Россия'
    # city = 'Москва'
    # email = 'adsad@mail.ru'
    # phone = '81234567890'
    # agree_person_data = 'on'
    # r = requests.post(url, params={'name': name,
    #                                'surname': surname,
    #                                'patronymic': patronymic,
    #                                'birthday': ' ',
    #                                'topics': topics,
    #                                'subject_1': 'on',
    #                                'subject_3': 'on',
    #                                'country': ' ',
    #                                'city': city,
    #                                'works': ' ',
    #                                'email': email,
    #                                'phone': phone,
    #                                'agree_person_data': 'on'})
    # print(r.status_code)
    # r.encoding = 'utf-8'
    # print(r.text)
    # print("https://script.google.com/macros/s/AKfycbxs7xZJ9jwERtfBIKnZeVbzWdsKjOVE8vrj4ntx2_MLgsxSatww/exec" in r.text)
