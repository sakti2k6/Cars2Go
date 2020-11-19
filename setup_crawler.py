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

class setup_crawler:
    '''
    Contains methods  to dowloads robots.txt and extract the car make/model and all location information from the sitemap xml files
    '''
    headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
    def __init__(self):
        try:
            os.mkdir('./files')
        except:
            pass

    def download_robots_txt(self, url):
        website_name = url.split('.')[-2]
        robot = url + '/robots.txt'
        res = requests.get(robot, headers=self.headers)
        try:
            with open(f'./files/{website_name}_robots.txt','wb') as f:
                f.write(res.content)
        except:
            raise Exception(f"Unable to create {website_name}_robots.txt")

