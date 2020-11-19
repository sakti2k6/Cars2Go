from flask import Flask, redirect, url_for, render_template, request, session, flash

from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import os
import json


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
carsDb = SQLAlchemy(app)

import models


app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_query = dict()
        user_query2 = {key:val for key, val in request.form.items()}
        print(user_query2)
        for key, val in request.form.items():
            if key == 'make' or key == 'model':
                if val:
                    user_query[key] = val
                else:
                    user_query[key] = ''
            elif  key == 'maxyear':
                if val:
                    user_query[key] = val
                else:
                    user_query[key] = 2021
            elif 'min' in key:
                if val:
                    user_query[key] = val
                else:
                    user_query[key] = 0
            elif 'max' in key:
                if val:
                    user_query[key] = val
                else:
                    user_query[key] = 99999999

        user_query = json.dumps(user_query)
        #print(user_query)
        #flash(f"Querying for car : {query}")
        return redirect(url_for("search", query_data=user_query))
    else:
        return render_template("home.html")


@app.route("/search")
def search():
    #print(request.values)
    item = request.args['query_data'] #Gets all the query fields as a string
    item = json.loads(item) # convert to dictionary
    makeQ = f"%{item['make']}%".upper()
    modelQ = f"%{item['model']}%".upper()
    cars = models.CarsModel.query.\
           filter(models.CarsModel.make.like(makeQ)).\
           filter(models.CarsModel.model.like(modelQ)).\
           filter(models.CarsModel.price.between(item['minprice'],item['maxprice'])).\
           filter(models.CarsModel.mileage.between(item['minmiles'],item['maxmiles'])).\
           filter(models.CarsModel.year.between(item['minyear'],item['maxyear'])).\
           order_by(models.CarsModel.price).limit(50).all()

    print(len(cars))
    results = []
    for car in cars:
        result = {
                'make'  : car.make,
                'model' : car.model,
                'trim'  : car.trim,
                'color' : car.color,
                'year'  : car.year,
                'price' : car.price,
                'location' : car.location,
                'mileage' : car.mileage,
                'link' : car.link
                }
        #print(result)
        result['make']    = f"{car.make}".title()
        result['model']   = f"{car.model}".title()
        result['trim']    = f"{car.trim}".title()
        result['color']   = f"{car.color}".title()
        result['year']    = f"{car.year}"
        result['link']    = f"{car.link}"
        result['location']   = f"{car.location}"
        result['price']   = f"${car.price:,}"
        result['mileage'] = f"{car.mileage:,} miles"
        results.append(result)

    return render_template("search.html", cars=results, num=len(results))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
