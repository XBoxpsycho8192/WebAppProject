from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models import Users, Inventory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")
departments = ['', 'Automotive', 'Books', 'Clothing', 'Electronics', 'Grocery', 'Seasonal', 'Office Supplies', 'Pharmacy', 'Sports', 'Tools']


# This is the route to the Home Page (The inventory page = Home Page).
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
    if request.method == "POST":
        email = request.form.get("email")  # Get email from user.
        password = request.form.get("password")  # Get password from user.

        user = Users.query.filter_by(email=email).first()  # Look up user by email provided.
        if user:
            if check_password_hash(user.password, password):  # Check password hash for auth.
                login_user(user, remember=True)  # Login
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
    logout_user()  # Logout user function.
    flash(f"You have been logged out: {name}", category="success")
    return redirect(url_for("views.login"))


# This function is used to delete users. To delete the user the admin must enter the accounts email.
@views.route("/del_usr", methods=["GET", "POST"])
@login_required
def del_usr():
    from app import db
    if request.method == "POST":
        delUser = request.form.get("delete_user")  # Use get() to retrieve the form input value
        found_user = Users.query.filter_by(email=delUser).first()  # Check if email exists in database.
        if found_user:
            if current_user.role == 'admin' and found_user.role == 'user':  # Checks to see if the admin account was found. Cannot delete admin.
                db.session.delete(found_user)
                db.session.commit()
                flash("Profile deleted successfully!", category="success")
            else:
                flash("The admin account cannot be deleted!", category="error")
        else:
            flash("Profile not found!", category="error")
        return redirect(url_for("views.profile_page"))


# This function displays the signup page and controls how new accounts are created.
@views.route("signup", methods=["GET", "POST"])
def signup():
    from app import db
    if request.method == "POST":
        email = request.form.get("email")  # Get all info that is needed to create a user account. The default role is "user".
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = Users.query.filter_by(email=email).first()  # Checks to see if user already exists in database. Email must be unique.
        if user:
            flash("This email already exists!", category="error")
        elif len(email) < 4:
            flash("Email is too short. Email must be greater than 3 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name is too short. First name must be greater than 1 character.", category='error')
        elif len(lastName) < 2:
            flash("Last name is too short. Last name must be greater than 1 character.", category='error')
        elif password1 != password2:  # Passwords must match.
            flash("Your passwords do not match.", category='error')
        elif len(password1) < 7:
            flash("Password is too short. Last name must be greater than 8 character.", category='error')
        else:
            new_user = Users(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='scrypt'))  # Calls constructor in Class Users.
            db.session.add(new_user)
            db.session.commit()  # Save new user
            login_user(new_user, remember=True)  # Login new user account.
            flash("Account Created", category="success")
            return redirect(url_for("views.home"))
    return render_template("signup.html")


# This is the route to the Profile Page.
# This page lists the users in the database, and has a box to delete users. This page can only be accessed by the admin account.
@views.route("profile_page")
@login_required
def profile_page():
    from models import Users
    if current_user.role != 'admin':  # Check to see if the active account has the role of "admin".
        flash("Access denied. Only admin users can access this page.", "error")
        return redirect(url_for("views.home"))
    return render_template("profile.html", values=Users.query.all())


# Function to edit the inventory file.
@views.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    from app import db
    user = Users.query.get(current_user.id)  # This loads logged-in user info, and that info is passed to the html form.
    if request.method == "POST":
        email = request.form.get('email')  # Email is needed to retrieve the user info to be edited.
        old_password = request.form.get('old_password')  # Password is needed to authenticate the edit.
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')  # These password values must match.
        password2 = request.form.get('password2')
        user_found = Users.query.filter_by(email=email).first()
        if user_found:
            if email == user.email or user.role == "admin":  # Users can edit their own profile. Admin can edit anybody.
                if check_password_hash(user_found.password, old_password) or user.role == "admin":  # Users enter their old password. Admin can edit anybody.
                    new_firstName = firstName
                    new_lastName = lastName
                    new_password1 = password1
                    new_password2 = password2
                    if new_firstName:
                        user_found.firstName = new_firstName
                    if new_lastName:
                        user_found.lastName = new_lastName
                    if new_password1:
                        if len(new_password1) > 7:
                            if new_password2:
                                if new_password1 == new_password2:
                                    user_found.password = generate_password_hash(password1, method='scrypt')
                                else:
                                    flash("New passwords do not match.", category="error")
                                    return render_template("edit_user.html", user=user)
                            else:
                                flash("Please re-enter the new password.", category="error")
                                return render_template("edit_user.html", user=user)
                        else:
                            flash("New password must be at least 8 characters long.", category="error")
                            return render_template("edit_user.html", user=user)

                    if new_firstName or new_lastName or (new_password1 and new_password2):  # If any change forms were filled out, and the profile password is authenticated, the database saves.
                        db.session.commit()
                        flash('Profile edited successfully!', category="success")
                        return redirect(url_for("views.home"))
                else:
                    flash("Incorrect current password.", category="error")
            else:
                flash("Only an admin can edit another users profile!", category="error")
    return render_template("edit_user.html", user=user)


# Function that displays the inventory sheet.
@views.route("inventory_page", methods=["GET", "POST"])
@login_required
def inventory_page():
    sort_options = ['name', 'price', 'department', 'sku', 'quantity']
    inventory = Inventory.query.all()
    if request.method == 'POST':
        sort_key = request.form.get('sort_key')
        if sort_key in sort_options:    # These if statements check for a sort key, if one is found the data on screen is sorted accordingly.
            if sort_key == 'name':
                inventory.sort(key=lambda product: product.name)
            elif sort_key == 'price':
                inventory.sort(key=lambda product: product.price)
            elif sort_key == 'department':
                inventory.sort(key=lambda product: product.department)
            elif sort_key == 'sku':
                inventory.sort(key=lambda product: product.sku)
            elif sort_key == 'quantity':
                inventory.sort(key=lambda product: product.quantity)
            inventory = Inventory.query.order_by(sort_key).all()
    return render_template('inventory.html', inventory=inventory, sort_options=sort_options)


# Function to add a new product to the inventory.
@views.route("/add_product", methods=["GET", "POST"])
@login_required
def product_add():
    from app import db
    if request.method == "POST":
        name = request.form.get('name')  # Get all data required from users through the html forms.
        price = float(request.form.get('price'))
        department = request.form.get('department')
        quantity = int(request.form.get('quantity'))
        new_Inv = Inventory(name=name, price=price, department=department, quantity=quantity)  # Call constructor in Inv Class to create a new database entry.
        db.session.add(new_Inv)
        db.session.commit()  # Save Database
        flash('Item added successfully!', category='success')
        return redirect(url_for("views.inventory_page"))
    return render_template("add_product.html", departments=departments)


# Function to edit the inventory file.
@views.route("/edit_inventory", methods=["GET", "POST"])
@login_required
def inventory_edit():
    from app import db
    if request.method == "POST":
        sku = request.form.get('sku')   # Get all data the user enters into the html form.
        name = request.form.get('name')
        price = request.form.get('price')
        department = request.form.get('department')
        quantity = request.form.get('quantity')
        sku_found = Inventory.query.filter_by(sku=sku).first()  # Use the sku entered to see if the product exists in the database.
        if sku_found:
            new_name = name
            new_price = price
            new_department = department
            new_quantity = quantity
            if new_name:            # If statements check to see if data needs to be updated based on the input received.
                sku_found.name = name
            if new_price:
                sku_found.price = price
            if new_department:
                sku_found.department = department
            if new_quantity:
                new_quantity = int(new_quantity)
                if new_quantity == 0:
                    db.session.delete(sku_found)
                else:
                    sku_found.quantity = quantity
        if new_name or new_price or new_department or new_quantity or new_quantity == 0:
            db.session.commit()     # If changes save database.
            flash('Item edited successfully!', category="success")
            return redirect(url_for("views.inventory_page"))
    return render_template("edit_inventory.html", departments=departments)


# search route function
@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        # Get the user input from the form
        search = request.form.get("search")  # Get search info from html form.
        # Search for matching objects
        if len(search) != 0 and search != ' ':
            # Start Query on the database to look for item name, department, or sku? This can be used as a product lookup.
            match = Inventory.query.filter(
                (Inventory.name.ilike(f"%{search}%")) |
                (Inventory.department.ilike(f"%{search}%")) |
                (Inventory.sku.ilike(f"%{search}%"))
            ).all()
            return render_template("results.html", match=match)
    return redirect(url_for("views.inventory_page"))
