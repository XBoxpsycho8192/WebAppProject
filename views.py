from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from inventory import inventory
from inventory import departments, add_product

# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")


# Alot of these routes are for experiments right now.
# This is the route to the Home Page.
@views.route("/")
def home():
    return render_template("index.html")


@views.route("/profile/")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html",name=name)


@views.route("go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))


# This is the route to the Profile Page.
@views.route("profile_page")
def profile_page():
    return render_template("profile.html")


@views.route("inventory_page")
def inventory_page():
    return render_template("inventory.html", inventory=inventory)


@views.route("/add_product", methods=["GET", "POST"])
def product_add():
    if request.method == "POST":
        name = request.form.get('name')
        price = float(request.form.get('price'))
        department = request.form.get('department')
        quantity = int(request.form.get('quantity'))

        add_product(name, price, department, quantity)

        return redirect(url_for("views.inventory_page"))

    return render_template("add_product.html", departments=departments)



#  Old work I was not using. think it was in development

# @views.route('/search', methods=['POST'])
# def search():
#     input = request.form['input']
#     match = None
#
#     # Search through the array of objects
#     for obj in inventory:
#         if input == obj['name']:
#             match = obj
#             break
#     # fill template with matched object
#     return render_template('results.html', match = match)
#
# # constructor
# class Item:
#     def __init__(self, name, price, department, stock):
#         self.name = name
#         self.price = price
#         self.department = department
#         self.stock = stock
#
# # create objects
# wrench = Item("wrench", 19.99, "hardware", 10)
# shirt = Item("shirt", 5.99, "clothing", 57)
# laptop = Item("laptop", 799.99, "electronics", 12)
# tv = Item("tv", 499.99, "electronics", 9)
# pants = Item("pants", 29.99, "clothing", 22)
#
# # create test array
# inventory = [wrench, shirt, laptop, tv, pants]
#
# @views.route("views/result")
# def result():
#     return render_template("result.html")

