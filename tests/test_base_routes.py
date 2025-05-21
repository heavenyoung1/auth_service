def test_home_page(client):
    """ Тест - подключение GET-запрос к домашнему эндпоинту / """
    response = client.get("/API/v0.1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_test_page(client):
    """ Тест - подключение GET-запрос к эндпоинту /test """
    response = client.get("/API/v0.1/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Test"}

def test_get_session(client):
    """ Тест - подключение к БД """
    response = client.get("/API/v0.1/test_db_session")
    assert response.status_code == 200
    assert response.json()["ok"] == 1