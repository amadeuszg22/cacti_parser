#!/usr/bin/python3

import urllib3
from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime, timedelta
import csv
import pandas as pd
import io

class config:
        host = 'wanreporting.ch.pmi'
        url = '/cacti/graph_view.php?action=tree&tree_id=26&leaf_id=6305'
        status = ''
        links = {}
        sites = {}
        countries = {}
        regions  = {}
        services = {}
        graphids = []


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
        print (host)
        print (link)
        page = requests.get('http://'+config.host+'/cacti/'+link)
        soup = BeautifulSoup(page.content, features="html.parser")
        find = soup.find_all('a')
        #print find[1]
        csvm = re.compile('^(<a href="graph_xport)')
        hrefs = []
        for a in find:
                hrefs.append(str(a))
                for c in hrefs:
                        if csvm.match(c):
                                id = re.findall(r'[-\d]+', c)
                                if id[0] not in config.graphids:
                                        config.graphids.append(id[0])
        print (config.graphids)
        tdag = (datetime.now() - timedelta(days=1)).timestamp()
        tnw = datetime.now().timestamp()
        tp = str(int(tdag))
        tn = str(int(tnw))
        for item in config.graphids:
                request = requests.get('http://'+config.host+'/cacti/graph_xport.php?local_graph_id='+item+'&rra_id=0&view_type=tree&graph_start='+tp+'&graph_end='+tn)
                decoded = request.content.decode('utf-8')
                cs = csv.DictReader(decoded, delimiter=',')
                #print (list(cs))
                writer = csv.writer(open('./csv/'+host+item+'.csv', 'w'))
                for r in cs:
                        print (r['Title:'])  #('t'.join(r['Title:']))
                        writer.writerow(r)
                        time.sleep(1)


cacti_scrap()
graph_scrap('PKRK4591',config.links['PKRK4591'])
print (len(config.links))

