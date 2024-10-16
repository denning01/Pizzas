#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # Clear out existing data, starting with RestaurantPizza due to foreign key constraints
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Creating new data
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='123 Karen Lane')
    bistro = Restaurant(name="Sanjay's Pizza", address='456 Sanjay Ave')
    palace = Restaurant(name="Kiki's Pizza", address='789 Kiki Blvd')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizza relationships...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=12)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=15)
    restaurant_pizzas = [pr1, pr2, pr3]

    # Add all records to the database and commit the session
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")
