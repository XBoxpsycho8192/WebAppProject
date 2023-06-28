import random
import json
import glob
import datetime

# Pre-generated list of departments
departments = ['','Electronics', 'Clothing', 'Office Supplies', 'Sports', 'Books','Grocery']
# Inventory database
inventory = []


# \\Function to generate a random SKU
def generate_sku():
    sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
    return sku

#This is called by the add_product page.
def add_product(name, price, department, quantity):
    sku = generate_sku()

    product = {
        'name': name,
        'price': price,
        'department': department,
        'sku': sku,
        'quantity': quantity
    }

    inventory.append(product)


# Function to save the inventory to a file
def save_inventory():
    now = datetime.datetime.now()
    filename = "inventoryData.json"
    with open(filename, 'w') as file:
        json.dump(inventory, file)
    print("Inventory saved successfully!")


# Function to load the most recent inventory from a file
def load_most_recent_inventory():
    files = glob.glob("*.json")
    if not files:
        print("No saved inventory found.")
        return

    latest_file = max(files, key=lambda f: datetime.datetime.strptime(f, "inventoryData.json"))

    try:
        with open(latest_file, 'r') as file:
            inventory.clear()
            inventory.extend(json.load(file))
        print("Inventory loaded successfully!")
    except FileNotFoundError:
        print("File not found. Unable to load inventory.")


# Function to edit the inventory
def edit_inventory(sku_input, name_input, price_input, department_input, quantity_input):
    sku = sku_input
    for item in inventory:
        if item['sku'] == sku:
            new_name = name_input
            new_price = price_input
            new_department = department_input
            new_quantity = quantity_input

            if new_name:
                item['name'] = new_name
            if new_price:
                item['price'] = float(new_price)
            if new_department:
                item['department'] = new_department
            if new_quantity:
                new_quantity = int(new_quantity)
                if new_quantity == 0:
                    # item['quantity'] = 0
                    inventory.remove(item)
                else:
                    item['quantity'] = new_quantity
            return


# Load the most recent inventory at the start of the program
load_most_recent_inventory()

