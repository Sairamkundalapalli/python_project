import json
import os
from datetime import datetime

FILE_NAME = "inventory.json"  # Storage file for all inventory data

# ==================== Helper Functions ====================

def read_inventory():
    """
    Loads inventory data from the JSON file.
    If file doesn't exist, return an empty structure.
    """
    if not os.path.exists(FILE_NAME):
        return {"items": []}  # Default empty inventory
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)

def write_inventory(data):
    """
    Saves the inventory data back to JSON file.
    Overwrites old data completely.
    """
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def get_item_by_code(data, code):
    """
    Searches for a product in the inventory by its unique code.
    Returns the item dictionary if found, else None.
    """
    for item in data["items"]:
        if item["code"] == code:
            return item
    return None

def make_code(name):
    """
    Generates a unique code for a product based on its name.
    Example: "Green Apple" -> "green_apple"
    """
    return name.lower().replace(" ", "_")

# ==================== Product Management ====================

def create_item():
    """
    Adds a new product to the inventory.
    """
    stock_data = read_inventory()
    name = input("Product name: ").strip()
    price = float(input("Price: "))
    qty = int(input("Quantity in stock: "))

    code = make_code(name)
    if get_item_by_code(stock_data, code):
        print("⚠ Product already exists in inventory.")
        return

    stock_data["items"].append({
        "code": code,
        "name": name,
        "price": price,
        "qty": qty
    })
    write_inventory(stock_data)
    print(f"✅ '{name}' added to inventory.")

def list_items():
    """
    Displays all available products in the inventory.
    """
    stock_data = read_inventory()
    if not stock_data["items"]:
        print("ℹ No products available.")
        return
    print("\n--- Inventory ---")
    for item in stock_data["items"]:
        print(f"[{item['code']}] {item['name']} | ₹{item['price']} | Stock: {item['qty']}")
    print("-----------------\n")

def edit_item():
    """
    Allows user to update the details of an existing product.
    """
    stock_data = read_inventory()
    code = input("Enter product code to edit: ").strip()
    item = get_item_by_code(stock_data, code)
    if not item:
        print("❌ Item not found.")
        return

    # Keep existing values if user enters nothing
    new_name = input(f"New name ({item['name']}): ").strip()
    new_price = input(f"New price ({item['price']}): ").strip()
    new_qty = input(f"New quantity ({item['qty']}): ").strip()

    if new_name:
        item["name"] = new_name
        item["code"] = make_code(new_name)
    if new_price:
        item["price"] = float(new_price)
    if new_qty:
        item["qty"] = int(new_qty)

    write_inventory(stock_data)
    print("✅ Product details updated.")

def remove_item():
    """
    Deletes a product from the inventory.
    """
    stock_data = read_inventory()
    code = input("Enter product code to remove: ").strip()
    item = get_item_by_code(stock_data, code)
    if not item:
        print("❌ Item not found.")
        return
    stock_data["items"].remove(item)
    write_inventory(stock_data)
    print("🗑 Product removed from inventory.")

# ==================== Billing ====================

def checkout():
    """
    Handles the sale process:
    - User adds products to cart
    - Stock is updated
    - Final bill is displayed
    """
    stock_data = read_inventory()
    cart = []
    grand_total = 0

    while True:
        code = input("Enter product code (or 'done'): ").strip()
        if code.lower() == "done":
            break
        item = get_item_by_code(stock_data, code)
        if not item:
            print("❌ Product not found.")
            continue

        qty = int(input("Quantity: "))
        if qty > item["qty"]:
            print("⚠ Not enough stock.")
            continue

        # Deduct from stock and calculate line total
        item["qty"] -= qty
        line_total = qty * item["price"]
        grand_total += line_total
        cart.append((item["name"], qty, item["price"], line_total))

    # Save updated stock levels
    write_inventory(stock_data)

    # Print final bill
    print("\n🧾 BILL")
    print("--------------------------")
    for name, qty, price, total in cart:
        print(f"{name} x {qty} @ ₹{price} = ₹{total}")
    print("--------------------------")
    print(f"TOTAL: ₹{grand_total}")
    print("--------------------------\n")

# ==================== Main Menu ====================

def main():
    """
    Main loop for user interaction.
    Displays menu until user exits.
    """
    while True:
        print("=== Grocery Store System ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Checkout / Generate Bill")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_item()
        elif choice == "2":
            list_items()
        elif choice == "3":
            edit_item()
        elif choice == "4":
            remove_item()
        elif choice == "5":
            checkout()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("⚠ Invalid choice.")

if __name__ == "__main__":
    main()
