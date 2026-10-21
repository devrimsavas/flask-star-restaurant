import pytest
from app import app as flask_app
import app as app_module

@pytest.fixture()
def app():    
    flask_app.config.update({
        "TESTING":True,
    })
    #other setup
    yield flask_app
    #clean up 

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def temp_data(tmp_path,monkeypatch):
    #temporary JSON file for test 
    orders_file=tmp_path /"orders.json"
    messages_file=tmp_path /"customers_messages.json"
    monkeypatch.setattr(app_module, "ORDERS_FILE", orders_file)
    monkeypatch.setattr(app_module, "MESSAGES_FILE", messages_file)
    return orders_file, messages_file