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
import shutil
import gzip
import json
from datetime import date


class TrueCar_Setup:
    headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
    base_url = 'https://www.truecar.com'

    def __init__(self):
        try:
            os.mkdir('./files')
        except:
            pass

    def download_file(self, url, prefix):
        local_filename = prefix + url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f, length=16*1024*1024)

        return local_filename

    def gunzip_file(self, compress_file):
        uncompress_file = compress_file.strip('.gz')
        with gzip.open(compress_file, 'rb') as f_in:
            with open(uncompress_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(compress_file)
        return uncompress_file

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
            xml = self.download_file(xml_gz, "TrueCar_")
            if xml.endswith('.gz'):
                xml = self.gunzip_file(xml)

            file = open(xml, 'r')
            soup = BeautifulSoup(file,'lxml-xml')
            for link in soup.find_all(name='loc'):
                fields = link.text.split('/')
                city_state = fields[7].split('-')
                state = city_state[-1]
                city_state.pop()
                city = '-'.join(city_state[1:])
                #print(city, state)
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
