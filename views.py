from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from inventory import inventory, departments, add_product, save_inventory, edit_inventory
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")

# This is the route to the Home Page.
@views.route("/")
@login_required
def home():
    return redirect(url_for("views.inventory_page"))


# This is just a redirect to the home page.
@views.route("go-to-home")
@login_required
def go_to_home():
    return redirect(url_for("views.home"))


# This function will lead users to the login screen, if they are not logged in.
@views.route("login", methods=["POST", "GET"])
def login():
    from app import db
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in Successfully!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again!", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html")


# This function will log out the current user, and display a message.
@views.route("logout")
@login_required
def logout():
    name = current_user.firstName + " " + current_user.lastName
    logout_user()
    flash(f"You have been logged out: {name}", category="success")
    return redirect(url_for("views.login"))


# This function is used to delete users. To delete the user you must enter the accounts firstName.
@views.route("/del_usr", methods=["GET", "POST"])
@login_required
def del_usr():
    from app import db
    if request.method == "POST":
        delUser = request.form.get("delete_user")  # Use get() to retrieve the form input value
        found_user = Users.query.filter_by(firstName=delUser).first()
        if found_user:
            db.session.delete(found_user)
            db.session.commit()
            flash("User deleted successfully!", category="success")
        else:
            flash("User not found!", category="error")
        return redirect(url_for("views.profile_page"))


# This function displays the signup page and controls how new accounts are created.
@views.route("signup", methods=["GET", "POST"])
def signup():
    from app import db
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("This email already exists!", category="error")
        elif len(email) < 4:
            flash("Email is too short. Email must be greater than 3 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name is too short. First name must be greater than 1 character.", category='error')
        elif len(lastName) < 2:
            flash("Last name is too short. Last name must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash("Your passwords do not match.", category='error')
        elif len(password1) < 7:
            flash("Password is too short. Last name must be greater than 8 character.", category='error')
        else:
            new_user = Users(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created", category="success")
            return redirect(url_for("views.home"))
    return render_template("signup.html")


# This is the route to the Profile Page.
# This page lists the users in the db, and has a box to delete users.
@views.route("profile_page")
@login_required
def profile_page():
    from models import Users
    return render_template("profile.html", values=Users.query.all())


# Function that displays the inventory sheet.
@views.route("inventory_page", methods=["GET", "POST"])
@login_required
def inventory_page():
    sort_options = ['name', 'price', 'department', 'sku', 'quantity']
    sorted_inventory = inventory.copy()
    if request.method == 'POST':
        sort_key = request.form.get('sort_key')
        if sort_key in sort_options:
            sorted_inventory.sort(key=lambda product: product[sort_key])
    return render_template('inventory.html', inventory=sorted_inventory, sort_options=sort_options)


# Function to add a new product to the inventory.
@views.route("/add_product", methods=["GET", "POST"])
@login_required
def product_add():
    if request.method == "POST":
        name = request.form.get('name')
        price = float(request.form.get('price'))
        department = request.form.get('department')
        quantity = int(request.form.get('quantity'))

        add_product(name, price, department, quantity)

        flash('Item added successfully!', category='success')
        return redirect(url_for("views.inventory_page"))
    return render_template("add_product.html", departments=departments)


# Function to save the inventory.
@views.route("/save_inventory")
@login_required
def inventory_save():
    save_inventory()
    return redirect(url_for("views.inventory_page"))


# Function to edit the inventory file.
@views.route("/edit_inventory", methods=["GET", "POST"])
@login_required
def inventory_edit():
    if request.method == "POST":
        sku = request.form.get('sku')
        name = request.form.get('name')
        price = request.form.get('price')
        department = request.form.get('department')
        quantity = request.form.get('quantity')
        edit_inventory(sku, name, price, department, quantity)
        flash('Item edited successfully!', category="success")
        return redirect(url_for("views.inventory_page"))
    return render_template("edit_inventory.html", departments=departments)


# search route function
@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        # Get the user input from the form
        search = request.form.get("search")
        # Search for matching objects
        if len(search) != 0:
            match = []
            for obj in inventory:
                if search.lower() in obj["name"].lower():
                    match.append(obj)
            return render_template("results.html", match=match)
    return redirect(url_for("views.inventory_page"))
