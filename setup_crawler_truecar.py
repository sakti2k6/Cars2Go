import re
import collections
import time
from pprint import pprint
import os
import lxml
import random
import requests
from bs4 import BeautifulSoup
import html5lib
import json
from datetime import date

from file_utilities import download_file, gunzip_file

class TrueCar_Setup:
    '''
    Dowload robots.txt and extract the car make/model and all location information from the sitemap xml files
    '''
    headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
    base_url = 'https://www.truecar.com'

    def __init__(self):
        try:
            os.mkdir('./files')
        except:
            pass

    def download_robots_txt(self, url):
        robot = url + '/robots.txt'
        res = requests.get(robot, headers=self.headers)
        try:
            with open('./files/truecar_robots.txt','wb') as f:
                f.write(res.content)
        except:
            raise Exception("Unable to create truecar_robots.txt")

    def get_used_cars_xmls(self):
        with open('./files/truecar_robots.txt') as f:
            for line in f:
                if re.search('used-sitemap-index', line):
                    used_xml_url = line.split()[1]
                    break;

        if not used_xml_url:
            raise Exception("TrueCar used car urls not found")

        res = requests.get(used_xml_url, headers=self.headers)
        sp = BeautifulSoup(res.content, 'lxml-xml')
        xml_gzs_links = [f.text for f in sp.find_all(name='loc') if re.search(r"sitemap-make_model_city_\d+.xml",f.text)]
        return xml_gzs_links

    def extract_metadata(self, xmlgz_links):
        makeModel = dict()
        location = dict()
        for xml_gz in xmlgz_links:
            print("Downloading.....",xml_gz)
            xml = download_file(xml_gz, "TrueCar_")
            if xml.endswith('.gz'):
                xml = gunzip_file(xml)

            file = open(xml, 'r')
            soup = BeautifulSoup(file,'lxml-xml')
            for link in soup.find_all(name='loc'):
                fields = link.text.split('/')
                city_state = fields[7].split('-')
                state = city_state[-1]
                city_state.pop()
                city = '-'.join(city_state[1:])
                if state not in location:
                    location[state] = set()
                location[state].add(city)

                make, model = fields[5], fields[6]
                if make not in makeModel:
                    makeModel[make] = set()
                makeModel[make].add(model)

            file.close()
            os.remove(xml)

        #Write car "Make/Model" and "State/City" data to json files
        location_list = {key:list(val) for key, val in location.items()}
        makeModel_list = {key:list(val) for key, val in makeModel.items()}
        json.dump(location_list, open('./files/TrueCar_Location.json','w'))
        json.dump(makeModel_list, open('./files/TrueCar_Make_Model.json','w'))

    def run(self):
        self.download_robots_txt(obj.base_url)
        print("[INFO] [TrueCar] Downloaded Robots.txt for website")
        xmlgz_links = self.get_used_cars_xmls()
        print("[INFO] [TrueCar] Got the sitemap xml files car make model")
        self.extract_metadata(xmlgz_links)
        print("[INFO] [TrueCar] Extracted the car make/model/location metadata")

if __name__ == "__main__":
    obj = TrueCar_Setup()
    obj.run()
