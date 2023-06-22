from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from inventory import inventory
from inventory import departments, add_product, save_inventory, edit_inventory

# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")


# Alot of these routes are for experiments right now.
# This is the route to the Home Page.
@views.route("/")
def home():
    return render_template("index.html")


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


@views.route("/save_inventory")
def inventory_save():
    save_inventory()
    return redirect(url_for("views.inventory_page"))


@views.route("/edit_inventory", methods=["GET", "POST"])
def inventory_edit():
    if request.method == "POST":
        sku = request.form.get('sku')
        quantity = int(request.form.get('quantity'))
        edit_inventory(sku, quantity)
        return redirect(url_for("views.inventory_page"))
    return render_template("edit_inventory.html")

# search route
@views.route("/search", methods=["POST"])
def search():
    # Get the user input from the form
    search = request.form.get("search")

    # Search for matching objects
    match = []
    for obj in inventory:
        if search.lower() in obj["name"].lower():
            match.append(obj)

    return render_template("results.html", match=match)
