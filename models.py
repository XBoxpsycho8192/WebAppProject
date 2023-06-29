from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
# This file contains the class for the database.

db = SQLAlchemy()
DB_NAME = "database.db"

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))

    def __init__(self, email, password, firstName, lastName):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(100))
    department = db.Column(db.String(100))
    sku = db.Column(db.String(100), unique=True)
    quantity = db.Column(db.Integer)

    def __init__(self, name, price, department, quantity):
        self.name = name
        self.price = price
        self.department = department
        self.sku = generate_sku()
        if self.sku == "error occurred":
            self.sku == generate_sku()
        self.quantity = quantity

def generate_sku():
    sku = str()
    sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
    found_sku = Inventory.query.filter_by(sku=sku).first()
    if found_sku:
        sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
        found_sku = Inventory.query.filter_by(sku=sku).first()
        if found_sku:
            sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
            found_sku = Inventory.query.filter_by(sku=sku).first()
            if found_sku:
                sku = "error occurred"
    return sku


