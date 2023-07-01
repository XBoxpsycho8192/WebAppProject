from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
# This file contains the classes for the database.

db = SQLAlchemy()
DB_NAME = "database.db"


# Defines the columns for the users database table.
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')

# Constructor that is called to create a new user.
# The admin account is hard coded into the database.
    def __init__(self, email, password, firstName, lastName):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.role = 'user'


# Defines the columns for the product inventory database table.
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(100))
    department = db.Column(db.String(100))
    sku = db.Column(db.String(100), unique=True)
    quantity = db.Column(db.Integer)

# Constructor that is called to create a product.
    def __init__(self, name, price, department, quantity):
        self.name = name
        self.price = price
        self.department = department
        self.sku = generate_sku()
        self.quantity = quantity


# This function's purpose is to generate a random sku for a product.
# The function queries the database for a match, if a match is found the sku is regenerated until a match is not found.
def generate_sku():
    sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
    found_sku = Inventory.query.filter_by(sku=sku).first()
    while found_sku is not None:
        sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
        found_sku = Inventory.query.filter_by(sku=sku).first()
    return sku


