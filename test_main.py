from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Book API!"}


def test_create_book():
    book_data = {
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "address": {
            "street": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
        },
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    assert response.json() == book_data
