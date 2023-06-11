from flask import Blueprint, render_template, request, jsonify,redirect, url_for
# This file serves as a route map. It tells flask which webpage to load.
views = Blueprint(__name__, "views")

# Alot of these routes are for experiments right now.
# This is the route to the Home Page.
@views.route("/")
def home():
    return render_template("index.html",)


@views.route("/profile/")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html",name=name)

@views.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

@views.route("/data")
def  get_data():
    data = request.json
    return jsonify(data)

@views.route("go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

# This is the route to the Profile Page.
@views.route("profile_page")
def profile_page():
    return render_template("profile.html")
