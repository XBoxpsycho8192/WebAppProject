from flask import Blueprint, render_template, request

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("results")
def results():
    return render_template("results.html")

@views.route("/search", methods=["POST"])
def search():
    input = request.form["input"]
    match = None

    # Search through the array of objects
    for obj in inventory:
        if input == obj["name"]:
            match = obj
            break
    # fill template with matched object
    return render_template("views/results.html", match = match)

# constructor
class Item:
    def __init__(self, name, price, department, stock):
        self.name = name
        self.price = price
        self.department = department
        self.stock = stock

# create objects
wrench = Item("wrench", 19.99, "hardware", 2929)
shirt = Item("shirt", 5.99, "clothing", 5722)
laptop = Item("laptop", 799.99, "electronics", 1222)
tv = Item("tv", 499.99, "electronics", 9222)
pants = Item("pants", 29.99, "clothing", 2212)

# create test array
inventory = [wrench, shirt, laptop, tv, pants]

