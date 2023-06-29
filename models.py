from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

class Users(db.Model):
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
