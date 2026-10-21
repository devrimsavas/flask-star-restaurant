
#main page 
def test_index_page(client):
    response=client.get("/")
    assert response.status_code==200

#menu page 
def test_menu_page(client):
    response=client.get("/menu")
    assert response.status_code==302
    assert response.headers["Location"]=="/"