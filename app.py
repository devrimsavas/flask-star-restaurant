import json
from datetime import datetime
from pathlib import Path
import os

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)

from data import Food, Restaurant

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR))
DATA_DIR.mkdir(parents=True, exist_ok=True)
ORDERS_FILE = DATA_DIR / "orders.json"
MESSAGES_FILE = DATA_DIR / "customers_messages.json"
RESTAURANT_NAME = "STAR RESTAURANT"
CURRENCY = "$"

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# ---------- JSON storage helpers ----------

def load_json(path, default):
    """Read a JSON file, falling back to `default` if it is missing or corrupted."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def init_storage():
    """Make sure both data files exist and contain valid JSON."""
    if not isinstance(load_json(ORDERS_FILE, None), dict):
        save_json(ORDERS_FILE, {})
    if not isinstance(load_json(MESSAGES_FILE, None), list):
        save_json(MESSAGES_FILE, [])


# ---------- Restaurant setup ----------

def create_first_menu(restaurant):
    starter_menu = [
        ("Burger", 10),
        ("Pizza", 12),
        ("Fried Chicken", 9),
        ("Spaghetti", 11),
        ("Salad", 8),
        ("Lasagna", 15),
        ("Sushi", 20),
        ("Tacho", 19),
    ]
    for name, price in starter_menu:
        restaurant.add_an_food_to_menu(Food(name, price))


restaurant = Restaurant(RESTAURANT_NAME)
create_first_menu(restaurant)
init_storage()


def find_food(name):
    return next((food for food in restaurant.menu if food.food_name == name), None)


def parse_price(raw):
    """Return a positive float, or None if the input is not a valid price."""
    try:
        price = float(raw)
    except (TypeError, ValueError):
        return None
    return price if price > 0 else None


@app.context_processor
def inject_globals():
    # Available in every template
    return {"restaurant_name": RESTAURANT_NAME, "currency": CURRENCY}


# ---------- Pages ----------

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Star Restaurant Menu",
        menu=restaurant.display_menu(),
    )


@app.route("/menu")
def menu():
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contactus")
def contactus():
    return render_template("contactus.html")


# ---------- Menu management ----------

@app.route("/addnewfood", methods=["POST"])
def addnewfood():
    name = request.form.get("newfoodname", "").strip()
    price = parse_price(request.form.get("newfoodprice"))

    if not name or price is None:
        flash("Please enter a dish name and a price greater than 0.", "danger")
    elif find_food(name):
        flash(f"'{name}' is already on the menu.", "warning")
    else:
        restaurant.add_an_food_to_menu(Food(name, price))
        flash(f"'{name}' added to the menu.", "success")
    return redirect(url_for("index"))


@app.route("/updatefoodprice", methods=["POST"])
def updatefoodprice():
    name = request.form.get("updatefoodname", "")
    price = parse_price(request.form.get("updatefoodprice"))
    food = find_food(name)

    if food is None:
        flash(f"'{name}' was not found on the menu.", "danger")
    elif price is None:
        flash("Please enter a price greater than 0.", "danger")
    else:
        food.update_food_price(price)
        flash(f"Price of '{name}' updated to {CURRENCY}{price:.2f}.", "success")
    return redirect(url_for("index"))


@app.route("/removefood", methods=["POST"])
def removefood():
    name = request.form.get("removefoodname", "")

    if find_food(name) is None:
        flash(f"'{name}' was not found on the menu.", "danger")
    else:
        restaurant.remove_food_from_menu(name)
        flash(f"'{name}' removed from the menu.", "success")
    return redirect(url_for("index"))


# ---------- Orders ----------

@app.route("/getorder", methods=["POST"])
def getorder():
    customer = request.form.get("customername", "").strip()
    food_name = request.form.get("getordername", "")
    quantity_raw = request.form.get("getorderquantity", "").strip()

    if not customer:
        return jsonify({"error": "Customer name is required."}), 400
    if not quantity_raw.isdigit() or int(quantity_raw) < 1:
        return jsonify({"error": "Quantity must be at least 1."}), 400

    food = find_food(food_name)
    if food is None:
        return jsonify({"error": f"'{food_name}' is not on the menu."}), 404

    quantity = int(quantity_raw)
    unit_price = float(food.food_price)
    order = {
        "item": food.food_name,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": round(unit_price * quantity, 2),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    orders = load_json(ORDERS_FILE, {})
    customer_data = orders.setdefault(customer, {"orders": [], "total_paid": 0})
    customer_data["orders"].append(order)
    customer_data["total_paid"] = round(customer_data["total_paid"] + order["total_price"], 2)
    save_json(ORDERS_FILE, orders)

    return jsonify({
        "customer": customer,
        "order": order,
        "customer_data": customer_data,
        "receipt_url": url_for("receipt", customer=customer),
    })


@app.route("/receipt/<path:customer>")
def receipt(customer):
    customer_data = load_json(ORDERS_FILE, {}).get(customer)
    if customer_data is None:
        abort(404)
    return render_template(
        "receipt.html",
        customer=customer,
        customer_data=customer_data,
        printed_at=datetime.now(),
    )


# ---------- Contact ----------

@app.route("/submit-your-contact-info", methods=["POST"])
def submit_contact_info():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not (name and email and message):
        return jsonify({"error": "Name, email and message are required."}), 400

    messages = load_json(MESSAGES_FILE, [])
    messages.append({
        "id": len(messages) + 1,
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    })
    save_json(MESSAGES_FILE, messages)

    return jsonify({
        "message": "success",
        "name": name,
        "email": email,
        "customer_message": message,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)