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

# This code was replaced by the add_product code above

# # Function to add a new product to the inventory
# def add_product():
#     # name = input("Enter the product name: ")
#     name = request.form.get('name')
#     # price = float(input("Enter the price: $"))
#     price = float(request.form.get('price'))
#
#     # Prompt the user to choose a department from the pre-generated list
#     # print("Choose a department:")
#     # for i, department in enumerate(departments):
#     #     print(f"{i + 1}. {department}")
#     # choice = int(input("Enter the department number: "))
#
#     # department = departments[choice - 1]
#     department = request.form.get('department')
#     quantity = int(request.form.get('quantity'))
#
#     sku = generate_sku()
#
#     # Prompt the user to enter the quantity
#     quantity = int(input("Enter the quantity: "))
#
#     product = {
#         'name': name,
#         'price': price,
#         'department': department,
#         'sku': sku,
#         'quantity': quantity
#     }
#
#     inventory.append(product)
#     print("Product added successfully!")


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
def edit_inventory(sku_input, quantity_input):
    sku = sku_input
    for item in inventory:
        if item['sku'] == sku:
            new_quantity = quantity_input
            if new_quantity == 0:
                inventory.remove(item)
                print("Item removed from inventory.")
            else:
                item['quantity'] = new_quantity
                print("Quantity updated successfully.")
            return
    print("Item not found in inventory.")

def search():
    # Get the user input from the form
    

    # Search for matching objects
    match = []
    for obj in inventory:
        if search.lower() in obj["name"].lower():
            match.append(obj)


# Load the most recent inventory at the start of the program
load_most_recent_inventory()

# Main loop
def main():
    while True:
        print("\n=== Inventory Management ===")
        print("1. Add a product")
        print("2. View inventory")
        print("3. Save inventory")
        print("4. Edit Quantity")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_product()
        elif choice == '2':
            print("\n=== Inventory ===")
            if len(inventory) == 0:
                print("No products in inventory.")
            else:
                for product in inventory:
                    print("Name: ", product['name'])
                    print("Price: $", product['price'])
                    print("Department: ", product['department'])
                    print("SKU: ", product['sku'])
                    print("# of units in stock: ", product['quantity'])
                    print("----------------------")
        elif choice == '3':
            save_inventory()
        elif choice == '4':
            edit_inventory()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
print("Exiting Inventory Management.")

