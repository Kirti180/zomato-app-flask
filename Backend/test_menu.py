import pytest
from app import app


@pytest.fixture
def client():
    # Create a test client using Flask's test client
    with app.test_client() as client:
        yield client

def test_get_dishes(client):
    # Test GET /dishes endpoint
    response = client.get('/dishes')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_get_dish(client):
    # Test GET /dishes/<int:dish_id> endpoint
    response = client.get('/dishes/1')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_create_dish(client):
    # Test POST /dishes endpoint
    data = {
        'name': 'New Dish',
        'price': 15.0,
        'availability': True
    }
    response = client.post('/dishes', json=data)
    assert response.status_code == 201
    assert response.content_type == 'application/json'

def test_update_dish(client):
    # Test PUT /dishes/<string:dish_id> endpoint
    data = {
        'name': 'Updated Dish',
        'price': 20.0,
        'availability': False
    }
    response = client.put('/dishes/1', json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_delete_dish(client):
    # Test DELETE /dishes/<int:dish_id> endpoint
    response = client.delete('/dishes/1')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
