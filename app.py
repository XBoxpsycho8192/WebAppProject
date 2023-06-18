from flask import Flask, render_template, request

app = Flask(__name__)


inventory = [
    {"name": "Wrench", "price": "24.99", "department": "Hardware", "inv": "0001"},
    {"name": "Shirt", "price": "14.99", "department": "Clothes", "inv": "0001"},
    {"name": "Pants", "price": "34.99", "department": "Clothes", "inv": "0001"},
    {"name": "TV", "price": "699.99", "department": "Electronics", "inv": "0001"},
    {"name": "Laptop", "price": "899.99", "department": "Electronics", "inv": "0001"},
    {"name": "Saw", "price": "14.99", "department": "Hardware", "inv": "0001"},
    {"name": "Blender", "price": "24.99", "department": "Housewares", "inv": "0001"},
    {"name": "Waffle Iron", "price": "29.99", "department": "Housewares", "inv": "0001"},
    {"name": "Socks", "price": "4.99", "department": "Hardware", "inv": "0001"},
    {"name": "Hammer", "price": "24.99", "department": "Hardware", "inv": "0001"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Get the user input from the form
    search = request.form.get("search")

    # Search for matching objects
    match = []
    for obj in inventory:
        if search.lower() in obj["name"].lower():
            match.append(obj)

    return render_template("results.html", match=match)

if __name__ == "__main__":
    app.run(debug=True)
