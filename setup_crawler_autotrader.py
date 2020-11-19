import re
import collections
import time
from typing import List

import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import html5lib

from file_utilities import download_file, gunzip_file

headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
base_url = 'https://www.autotrader.com'


def download_robots_txt(url):
    robot = url + '/robots.txt'
    res = requests.get(robot, headers=headers)
    try:
        with open('./files/autotrader_robots.txt','wb') as f:
            f.write(res.content)
    except:
        raise Exception("Unable to create autotrader_robots.txt")

def get_used_cars_xmls():
    used_xml_url = ""
    with open('./files/autotrader_robots.txt') as f:
        for line in f:
            if re.search('sitemap_used_geo', line):
                used_xml_url = line.split()[1]
                break;

    if not used_xml_url:
        raise Exception("autotrader used car urls not found")

    res = requests.get(used_xml_url, headers=headers)
    sp = BeautifulSoup(res.content, 'lxml-xml')
    xml_gz_links = [f.text for f in sp.find_all(name='loc')]
    return xml_gz_links

def extract_metadata(xml_gz_links):
    makeModel = dict()
    location = dict()
    for xml in xml_gz_links:
        print(xml)
        res = requests.get(xml, headers=headers)
        soup = BeautifulSoup(res.content,'lxml-xml')
        for link in soup.find_all(name='loc'):
            print(link.text)
            fields = link.text.split('/')
            zipcode = fields[6].split('-')[-1]
            state = fields[6].split('-')[-2]
            city = fields[6].split('-')[:-2]
            city = '-'.join(city)
            print(city, state, zipcode)
            if zipcode not in location:
                location[zipcode] = [city, state]

            make, model = fields[4], fields[5]
            if make not in makeModel:
                makeModel[make] = set()
            makeModel[make].add(model)
            print(make, model)

    #Write car "Make/Model" and "State/City" data to json files
    location_list = location
    makeModel_list = {key:list(val) for key, val in makeModel.items()}
    json.dump(location_list, open('./files/Autotrader_Location.json','w'))
    json.dump(makeModel_list, open('./files/Autotrader_Make_Model.json','w'))

def run():
    download_robots_txt(base_url)
    print("[INFO] [TrueCar] Downloaded Robots.txt for website")
    xmlgz_links = get_used_cars_xmls()
    print(xmlgz_links[0])
    print("[INFO] [TrueCar] Got the sitemap xml files car make model")
    extract_metadata(xmlgz_links)
    print("[INFO] [TrueCar] Extracted the car make/model/location metadata")
