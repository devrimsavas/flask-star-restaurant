
from app import find_food
import json


#main page 
def test_index_page(client):
    response=client.get("/")
    assert response.status_code==200

#menu page 
def test_menu_page(client):
    response=client.get("/menu")
    assert response.status_code==302
    assert response.headers["Location"]=="/"

#about page 
def test_about_page(client):
    response=client.get("/about")
    assert response.status_code==200
# contact us page
def test_contact_page(client):
    response=client.get("/contactus")
    assert response.status_code==200 

#add new food test 
def test_add_new_food(client):
    response=client.post("/addnewfood", data={
        "newfoodname":"kebab",
        "newfoodprice":20        
    })
    #check status code
    assert response.status_code==302
    #check if this food is added to menu
    assert find_food("kebab") is not None

#update food price 
def test_update_food_price(client):
    response=client.post("/updatefoodprice",data={
        "updatefoodname":"kebab",
        "updatefoodprice":32,
        "food":find_food("kebab")
    })
    assert response.status_code==302
    #really price changed? 
    assert find_food("kebab").food_price==32

#remove food 
def test_delete_food(client):
    response=client.post("/removefood",data={
        "removefoodname":"kebab"
    })
    assert find_food("kebab") is None
    assert response.headers["Location"]=="/"


import json

# ---------- Orders ----------

def test_get_order(client, temp_data):
    orders_file, _ = temp_data
    response = client.post("/getorder", data={
        "customername": "Test User",
        "getordername": "Burger",
        "getorderquantity": "2",
    })
    assert response.status_code == 200
    assert response.get_json()["order"]["total_price"] == 20.0
    # The order was written to the temporary file
    saved = json.loads(orders_file.read_text(encoding="utf-8"))
    assert "Test User" in saved


def test_get_order_without_customer(client, temp_data):
    response = client.post("/getorder", data={
        "customername": "",
        "getordername": "Burger",
        "getorderquantity": "1",
    })
    assert response.status_code == 400


def test_get_order_invalid_quantity(client, temp_data):
    response = client.post("/getorder", data={
        "customername": "Test User",
        "getordername": "Burger",
        "getorderquantity": "0",
    })
    assert response.status_code == 400


def test_get_order_unknown_food(client, temp_data):
    response = client.post("/getorder", data={
        "customername": "Test User",
        "getordername": "Unknown Dish",
        "getorderquantity": "1",
    })
    assert response.status_code == 404


# ---------- Receipt ----------

def test_receipt_after_order(client, temp_data):
    order = client.post("/getorder", data={
        "customername": "Test User",
        "getordername": "Burger",
        "getorderquantity": "1",
    })
    receipt_url = order.get_json()["receipt_url"]
    response = client.get(receipt_url)
    assert response.status_code == 200


def test_receipt_unknown_customer(client, temp_data):
    response = client.get("/receipt/Nobody")
    assert response.status_code == 404


# ---------- Contact ----------

def test_contact_form(client, temp_data):
    _, messages_file = temp_data
    response = client.post("/submit-your-contact-info", data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello!",
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "success"
    saved = json.loads(messages_file.read_text(encoding="utf-8"))
    assert len(saved) == 1


def test_contact_form_missing_fields(client, temp_data):
    response = client.post("/submit-your-contact-info", data={
        "name": "Test User",
        "email": "",
        "message": "",
    })
    assert response.status_code == 400