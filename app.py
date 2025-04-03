from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['car_rental']
cars_collection = db['cars']
rentals_collection = db['rentals']

# Initialize Database
def init_db():
    if cars_collection.count_documents({}) == 0:
        cars_collection.insert_many([
            {"model": "Civic", "brand": "Honda", "available": True},
            {"model": "Corolla", "brand": "Toyota", "available": True},
            {"model": "Model 3", "brand": "Tesla", "available": True}
        ])

@app.route('/')
def home():
    cars = list(cars_collection.find())
    return render_template('index.html', cars=cars)

@app.route('/rent/<car_id>', methods=['POST'])
def rent_car(car_id):
    renter_name = request.form.get('renter_name')
    cars_collection.update_one({"_id": car_id}, {"$set": {"available": False}})
    rentals_collection.insert_one({"car_id": car_id, "renter_name": renter_name})
    return redirect(url_for('home'))

@app.route('/return/<car_id>', methods=['POST'])
def return_car(car_id):
    cars_collection.update_one({"_id": car_id}, {"$set": {"available": True}})
    rentals_collection.delete_one({"car_id": car_id})
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
