#!/usr/bin/env python3

import os
import logging
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set up the base directory and database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/')
def index():
    return '<h1>Code Challenge: Pizza Restaurant API</h1>'

# Route for getting all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        app.logger.debug("Fetching all restaurants.")
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    except Exception as e:
        app.logger.error(f"Error retrieving restaurants: {e}")
        return jsonify({"error": str(e)}), 500  # Improved error logging

# Route for getting a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    try:
        app.logger.debug(f"Fetching restaurant with ID: {id}")
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            app.logger.warning(f"Restaurant with ID {id} not found.")
            return jsonify(error="Restaurant not found"), 404
        return jsonify(restaurant.to_dict()), 200
    except Exception as e:
        app.logger.error(f"Error retrieving restaurant with ID {id}: {e}")
        return jsonify(error="An error occurred while retrieving the restaurant."), 500

# Route for deleting a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    try:
        app.logger.debug(f"Attempting to delete restaurant with ID: {id}")
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            app.logger.warning(f"Restaurant with ID {id} not found.")
            return jsonify(error="Restaurant not found"), 404
        
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting restaurant with ID {id}: {e}")
        return jsonify(error="An error occurred while deleting the restaurant."), 500

# Route for getting all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    try:
        pizzas = Pizza.query.all()
        if not pizzas:
            app.logger.debug("No pizzas found.")
            return jsonify([]), 200  # Return an empty list if no pizzas found
        return jsonify([pizza.to_dict() for pizza in pizzas]), 200
    except Exception as e:
        app.logger.error(f"Error retrieving pizzas: {e}")
        return jsonify(error="An error occurred while retrieving pizzas."), 500

# Route for creating restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    errors = []

    # Validate incoming data
    if not all(key in data for key in ['restaurant_id', 'pizza_id', 'price']):
        errors.append("validation errors")
    
    price = data.get('price')
    if not isinstance(price, (int, float)) or not (1 <= price <= 30):
        errors.append("validation errors")

    # Ensure the restaurant and pizza exist
    restaurant = Restaurant.query.get(data['restaurant_id'])
    pizza = Pizza.query.get(data['pizza_id'])

    if not restaurant or not pizza:
        errors.append("validation errors")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_restaurant_pizza = RestaurantPizza(
            restaurant_id=data['restaurant_id'],
            pizza_id=data['pizza_id'],
            price=price
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An internal error occurred."]}), 500
