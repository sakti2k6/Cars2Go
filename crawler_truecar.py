import re
import collections
import time

from pprint import pprint
import lxml
import random
import requests
from bs4 import BeautifulSoup
import json
from datetime import date

from app import app, carsDb
from models import *

from scrapper_truecar import scrapper_truecar

class crawler_truecar:
    def __init__(self):
        self.base_url = "https://www.truecar.com"

    def crawl_url(self, url):
        headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
        queue = collections.deque()
        session = requests.Session()
        response = session.get(url, headers = headers, timeout = (5,10))
        queue.append(url)
        soup = BeautifulSoup(response.content,'html.parser')

        #Find no of pages in the current page
        pages = soup.find_all(name = 'a',attrs = {'data-test':'paginationLink'})
        if pages:
            count = int(pages[-1].text)
            for i in range(2, count+1):
                queue.append(f'{url}?page={str(i)}')

        cnt = len(queue)
        while queue:
            nextUrl = queue.popleft()
            scrapper_truecar(nextUrl, session, headers)
            pausetime = random.uniform(0.4,1.5)
            time.sleep(pausetime)

        session.close()
        return cnt

    def run_spider(self):
        cnt = 0
        make_model = json.load(open('./files/TrueCar_Make_Model.json','r'))
        #locations = json.load(open('./files/TrueCar_Location.json','r'))
        # Only crawl for austin location
        year = 'year-2020-max' #Only crawl 2020 car models
        for make, models in make_model.items():
            for model in models:
                url = f"{self.base_url}/used-cars-for-sale/listings/{make}/{model}/{year}/location-austin-tx/"
                try:
                    cnt += self.crawl_url(url)
                except Exception as e:
                    print(str(e))
        return cnt


if __name__ == "__main__":
    start_time = time.time()
    spider = crawler_truecar()
    cnt = spider.run_spider()
    print(f"All URLs {cnt} Crawled in {time.time()-start_time} seconds")

