#!/usr/bin/python

import urllib3
from bs4 import BeautifulSoup
import requests
import re
import time


class config:
        host = 'wanreporting.ch.pmi'
        url = '/cacti/graph_view.php?action=tree&tree_id=26&leaf_id=6305'
        status = ''
        links = {}
        sites = {}
        countries = {}
        regions  = {}
        services = {}

def cacti_scrap():
        #try:
        #print ('http://'+config.host+config.url)
        page = requests.get('http://'+config.host+config.url)
        soup = BeautifulSoup(page.content, features="html.parser")
        find = soup.find_all('script')[6]
        text = ("".join(find)).split('\n')
        while '' in text:
                text.remove('')
#       print text
        texts = re.compile("^(ou)") #"^(?<!\w )[^\w]"
        treea = re.compile("^(tre)")
        hmath = re.compile("^(Host:)")
        for line in text:
                if texts.match(line):
                        lines = line.partition('"')
                        #print lines[2]
                        if not treea.match(lines[2]):
                                #print lines[2]
                                if hmath.match(lines[2]):
                                        host = re.split(r'["]', lines[2])
                                        name = re.split(r'[\s+]', host[0])
                                        #print name[1]
                                        link = re.sub(";","&", host[2])
                                        #print link
                                        config.links[name[1]] = link
                                        #time.sleep(1)
        return

def graph_scrap(host,link):
        print host
        print link
        page = requests.get('http://'+config.host+'/cacti/'+link)
        soup = BeautifulSoup(page.content, features="html.parser")
        find = soup.find_all('a')
        for a in find:
                print a
                time.sleep(1)

cacti_scrap()
graph_scrap('PKRK2465',config.links['PKRK2465'])
print (len(config.links))
