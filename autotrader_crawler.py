import re
import collections
import time

import random
import requests
from bs4 import BeautifulSoup
from datetime import date
from pprint import pprint
import json

from app import app, carsDb
from models import *

headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
base_url = 'https://www.autotrader.com'


def crawl_url(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    cars = soup.find_all(name = 'div',attrs = {'data-cmp':'inventoryListing'})
    make = url.split('/')[4].upper()
    model = url.split('/')[5].upper()
    if not cars:
        return
    for i in range(len(cars)):
        car = cars[i]
        car_details = car.find(name = 'div', attrs = {'class' : 'inventory-listing-body'})
        link_tag = car_details.find(name = 'a', attrs = {'href' : True})
        link = "https://www.autotrader.com" + link_tag['href']
        year = link_tag.text.split(' ')[1]
        trim = link_tag.text.split(' ')[-1]
        if model.endswith(trim):
            trim = ""
        price = car.find(name = 'span', attrs = {'class' : 'first-price'}).text
        price = int(price.replace(',',''))
        details = car_details.find(name='div', attrs={'class' : 'item-card-specifications'}).text
        mileage = details.split(' ')[0]
        mileage = int(mileage.replace(',', ''))

        color = str(details.split(' ')[2][:-4])
        location = car.find(name = 'div', attrs={'data-cmp' : 'ownerDistance'}).text
        print(make, model, trim, color, year, price, location, mileage)
        try:
            db_row = CarsModel(
                        make        = make,
                        model       = model,
                        trim        = trim,
                        color       = color,
                        year        = year,
                        price       = price,
                        location    = location,
                        mileage     = mileage,
                        link        = link,
                        timestamp   = date.today()
                              )

            carsDb.session.add(db_row)
            carsDb.session.commit()
            pprint(db_row)
        except Exception as e:
            carsDb.session.rollback()
            print('Cant add to database..', str(e))
        finally:
            carsDb.session.close()

cnt = 0
make_model = json.load(open('./files/Autotrader_Make_Model.json','r'))
#locations = json.load(open('./files/TrueCar_Location.json','r'))
# Only crawl for austin location and 2018 or newer cars
for make, models in make_model.items():
    for model in models:
        url = f"{base_url}/cars-for-sale/{make}/{model}/austin-tx/?numRecords=100&startYear=2020"
        print(url)
        time.sleep(random.uniform(0.5,1.6))
        try:
            crawl_url(url)
        except Exception as e:
            print(str(e))
