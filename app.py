from flask import Flask, render_template, request, redirect, url_for
from store_management_system import StoreManagementSystem

app = Flask(__name__)
inventory_file = "inventory.json"
store = StoreManagementSystem(inventory_file)


@app.route("/", methods=["GET"])
def index():
    inventory = store.display_inventory()
    return render_template("index.html", inventory=inventory)


@app.route("/add_item", methods=["POST"])
def add_item():
    item = request.form.get("item", "").strip()
    if not item or not item.isalpha():
        return "Invalid item name. Please enter a valid item name (only letters are allowed).", 400

    quantity = request.form.get("quantity", type=int)
    if quantity is None or quantity <= 0:
        return "Invalid quantity. Please enter a valid positive integer value.", 400

    message = store.add_item(item, quantity)
    return redirect(url_for("index"))


@app.route("/remove_item", methods=["POST"])
def remove_item():
    item = request.form.get("item")
    quantity = request.form.get("quantity", type=int)
    if item and quantity is not None:
        message = store.remove_item(item, quantity)
    return redirect(url_for("index"))


@app.route("/sell_item", methods=["POST"])
def sell_item():
    item = request.form.get("item")
    quantity = request.form.get("quantity", type=int)
    price_per_unit = request.form.get("price_per_unit", type=float)
    if item and quantity is not None and price_per_unit is not None:
        result = store.sell_item(item, quantity, price_per_unit)
        if isinstance(result, dict):
            return render_template("bill.html", result=result)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Driver code to populate initial inventory
    store.add_item("Apple", 10)
    store.add_item("Banana", 5)
    store.add_item("Orange", 8)
    store.add_item("Mango", 12)

    app.run(debug=True)
