from flask import Flask, render_template, request, redirect, Blueprint
from inventory_db import *

inventory = Blueprint(__name__, "inventory")



# \\Function to generate a random SKU
def generate_sku():
    sku = ''.join(random.choices('CDEFGHJKLNPRTVWXYZ234679', k=8))
    return sku


# Function to add a new product to the inventory
def add_product():
    # name = input("Enter the product name: ")
    # price = float(input("Enter the price: $"))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        department = request.form['department']
        quantity = int(request.form['quantity'])

        sku = generate_sku()

        product = {
            'name': name,
            'price': price,
            'department': department,
            'sku': sku,
            'quantity': quantity
        }
        inventory.append(product)
        return redirect('/inventory')
    else:
        return render_template('add_product.html', departments=departments)

#     # Prompt the user to choose a department from the pre-generated list
#     print("Choose a department:")
#     for i, department in enumerate(departments):
#         print(f"{i + 1}. {department}")
#     choice = int(input("Enter the department number: "))
#
#     department = departments[choice - 1]
#     sku = generate_sku()
#
#     # Prompt the user to enter the quantity
#     quantity = int(input("Enter the quantity: "))
#
#
#     inventory.append(product)
#     print("Product added successfully!")
#
#
# # Function to save the inventory to a file
# def save_inventory():
#     now = datetime.datetime.now()
#     filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
#     with open(filename, 'w') as file:
#         json.dump(inventory, file)
#     print("Inventory saved successfully!")
#
#
# # Function to load the most recent inventory from a file
# def load_most_recent_inventory():
#     files = glob.glob("*.json")
#     if not files:
#         print("No saved inventory found.")
#         return
#
#     latest_file = max(files, key=lambda f: datetime.datetime.strptime(f, "%Y-%m-%d_%H-%M-%S.json"))
#
#     try:
#         with open(latest_file, 'r') as file:
#             inventory.clear()
#             inventory.extend(json.load(file))
#         print("Inventory loaded successfully!")
#     except FileNotFoundError:
#         print("File not found. Unable to load inventory.")
#
#
# # Function to edit the inventory
# def edit_inventory():
#     sku = input("Enter the SKU of the item to edit: ")
#     for item in inventory:
#         if item['sku'] == sku:
#             new_quantity = int(input("Enter the new quantity: "))
#             if new_quantity == 0:
#                 inventory.remove(item)
#                 print("Item removed from inventory.")
#             else:
#                 item['quantity'] = new_quantity
#                 print("Quantity updated successfully.")
#             return
#     print("Item not found in inventory.")
#
#
# # Load the most recent inventory at the start of the program
# load_most_recent_inventory()
#
# # Main loop
# while True:
#     print("\n=== Inventory Management ===")
#     print("1. Add a product")
#     print("2. View inventory")
#     print("3. Save inventory")
#     print("4. Edit Quantity")
#     print("5. Exit")
#
#     choice = input("Enter your choice (1-5): ")
#
#     if choice == '1':
#         add_product()
#     elif choice == '2':
#         print("\n=== Inventory ===")
#         if len(inventory) == 0:
#             print("No products in inventory.")
#         else:
#             for product in inventory:
#                 print("Name: ", product['name'])
#                 print("Price: $", product['price'])
#                 print("Department: ", product['department'])
#                 print("SKU: ", product['sku'])
#                 print("# of units in stock: ", product['quantity'])
#                 print("----------------------")
#     elif choice == '3':
#         save_inventory()
#     elif choice == '4':
#         edit_inventory()
#     elif choice == '5':
#         break
#     else:
#         print("Invalid choice. Please try again.")
# print("Exiting Inventory Management.")

