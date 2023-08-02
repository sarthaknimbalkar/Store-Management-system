import json

class StoreManagementSystem:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            json.dump(self.inventory, file)

    def add_item(self, item, quantity):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

        self.save_inventory()
        return f"Added {quantity} {item}(s) to the inventory."

    def remove_item(self, item, quantity):
        if item not in self.inventory:
            return f"{item} is not in the inventory."

        if self.inventory[item] < quantity:
            return f"Not enough {item} in the inventory."

        self.inventory[item] -= quantity
        self.save_inventory()
        if self.inventory[item] < 3:
            self.notify_vendor(item)

        return f"Removed {quantity} {item}(s) from the inventory."

    def sell_item(self, item, quantity, price_per_unit):
        if item not in self.inventory:
            return f"{item} is not in the inventory."

        if self.inventory[item] < quantity:
            return f"Not enough {item} in the inventory."

        subtotal = price_per_unit * quantity
        gst = subtotal * 0.18
        total = subtotal + gst

        self.inventory[item] -= quantity
        self.save_inventory()

        if self.inventory[item] < 3:
            self.notify_vendor(item)

        return {
            "item": item,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "subtotal": subtotal,
            "gst": gst,
            "total": total,
        }

    def notify_vendor(self, item):
        return f"Notification: Quantity of {item} is less than 3. Please restock."

    def display_inventory(self):
        return self.inventory
