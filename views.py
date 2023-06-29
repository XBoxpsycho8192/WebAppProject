from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from inventory import inventory, departments, add_product, save_inventory, edit_inventory
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")

# This is the route to the Home Page.
@views.route("/")
def home():
    return redirect(url_for("views.inventory_page"))


@views.route("go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))





@views.route("login", methods=["POST", "GET"])
def login():
    from app import db
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, None)
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for("views.user",))
    else:
        if "user" in session:
            flash ("Already Logged In!")
            return redirect(url_for("views.user"))
        return render_template("login.html")


@views.route("user", methods=["POST", "Get"])
def user():
    from app import db
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        flash(f"Logged in as: {user}", 'success')
        return render_template("profile.html", email=email, values=Users.query.all())
    else:
        flash("You are not logged in!")
        return redirect(url_for("views.login"))

@views.route("logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        flash(f"You have been logged out: {user}", 'success')
    if "email" in session:
        email = session["email"]
        session.pop("email", None)
        flash(f"Logged email: {email} CLEARED!", 'success')
    return redirect(url_for("views.login"))



@views.route("/del_usr", methods=["GET", "POST"])
def del_usr():
    from app import db
    if request.method == "POST":
        deluser = request.form.get("delete_user")  # Use get() to retrieve the form input value
        found_user = Users.query.filter_by(firstName=deluser).first()
        if found_user:
            db.session.delete(found_user)
            db.session.commit()
            flash("User deleted successfully!", "success")
        else:
            flash("User not found!", "error")
        return redirect(url_for("views.profile_page"))

@views.route("signup", methods=["GET", "POST"])
def signup():
    from app import db
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
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
            flash("Account Created", category="success")
            return redirect(url_for("views.home"))
    return render_template("signup.html")











# This is the route to the Profile Page.
@views.route("profile_page")
def profile_page():
    from models import Users
    return render_template("profile.html", values=Users.query.all())


@views.route("inventory_page", methods=["GET", "POST"])
def inventory_page():
    sort_options = ['name', 'price', 'department', 'sku', 'quantity']
    sorted_inventory = inventory.copy()
    if request.method == 'POST':
        sort_key = request.form.get('sort_key')
        if sort_key in sort_options:
            sorted_inventory.sort(key=lambda product: product[sort_key])
    return render_template('inventory.html', inventory=sorted_inventory, sort_options=sort_options)


@views.route("/add_product", methods=["GET", "POST"])
def product_add():
    if request.method == "POST":
        name = request.form.get('name')
        price = float(request.form.get('price'))
        department = request.form.get('department')
        quantity = int(request.form.get('quantity'))
        add_product(name, price, department, quantity)
        flash('Item added successfully!', 'success')
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
        name = request.form.get('name')
        price = request.form.get('price')
        department = request.form.get('department')
        quantity = request.form.get('quantity')
        edit_inventory(sku, name, price, department, quantity)
        flash('Item edited successfully!', 'success')
        return redirect(url_for("views.inventory_page"))
    return render_template("edit_inventory.html", departments=departments)

# search route
@views.route("/search", methods=["GET", "POST"])
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