import pytest
from app import app as flask_app

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