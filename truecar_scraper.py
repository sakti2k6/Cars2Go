from pprint import pprint
import lxml
import requests
from bs4 import BeautifulSoup
from datetime import date

from app import app, carsDb
from models import *

def truecar_scraper(url, session, headers):
    response = session.get(url, headers = headers)

    print(f"Processing URL: {response.url}")
    print("----------------------------------------")
    soup = BeautifulSoup(response.content,'html.parser')
    cars = soup.find_all(name = 'a',attrs = {'data-test':'usedListing'})
    if not cars:
        return

    base_url = "https://www.truecar.com"
    for car in cars:
        link = base_url + car['href']

        car_details = car.find(name = 'div', attrs = {'data-test' : 'cardContent'})
        price = car_details.find(name = 'div', attrs = {'data-test' : 'vehicleListingPriceAmount'})
        if price:
            price = int(price.text[1:].replace(',',''))
        else:
            return

        year = int(car_details.find(name = 'span', attrs = {'class' : 'vehicle-card-year'}).get_text())
        if year < 2020:
            return

        make = url.split('/')[5].upper()
        model = url.split('/')[6].upper()

        trim = car_details.find(name = 'div', attrs = {'data-test' : 'vehicleCardTrim'}).get_text()

        mileage = car_details.find(name = 'div', attrs = {'data-test' : 'vehicleMileage'}).get_text()
        mileage = mileage.split(' ')[0].replace(',','')
        mileage = int(mileage)

        location = car_details.find(name = 'div', attrs = {'data-test' : 'vehicleCardLocation'}).text
        color = car_details.find(name = 'div', attrs = {'data-test' : 'vehicleCardColors'}).text

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
            print('Cant add to database..', str(e))

