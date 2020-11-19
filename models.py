from app import carsDb

class CarsModel(carsDb.Model):
    __tablename__ = 'cars'

    id = carsDb.Column(carsDb.Integer, primary_key=True)
    make = carsDb.Column(carsDb.String())
    model = carsDb.Column(carsDb.String())
    trim = carsDb.Column(carsDb.String())
    color = carsDb.Column(carsDb.String())
    year = carsDb.Column(carsDb.Integer)
    price = carsDb.Column(carsDb.Integer)
    location = carsDb.Column(carsDb.String())
    mileage = carsDb.Column(carsDb.Integer)
    link = carsDb.Column(carsDb.String())
    timestamp = carsDb.Column(carsDb.Date())

    def __init__(self, make, model, trim, color, year, price, location, mileage, link, timestamp):
        self.make = make
        self.model = model
        self.trim = trim
        self.color = color
        self.year = year
        self.price = price
        self.location = location
        self.mileage = mileage
        self.link = link
        self.timestamp = timestamp

    def __repr__(self):
        return f'<car id:{self.id}, {self.year} {self.make} {self.model} ${self.price:,} {self.color} {self.location} {self.mileage}>'
