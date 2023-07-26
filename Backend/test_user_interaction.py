import pytest
from app import app


@pytest.fixture
def client():
    # Create a test client using Flask's test client
    with app.test_client() as client:
        yield client

def test_create_order(client):
    # Test POST /orders endpoint
    data = {
        'customer_name': 'John Doe',
        'items': [
            {'dish_id': 1, 'dish_name': 'Dish 1', 'quantity': 2}
        ]
    }
    response = client.post('/orders', json=data)
    assert response.status_code == 201
    assert response.content_type == 'application/json'

def test_update_order(client):
    # Test PUT /orders/<int:order_id> endpoint
    data = {
        'status': 'Pending'
    }
    response = client.put('/orders/2', json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_get_orders(client):
    # Test GET /orders endpoint
    response = client.get('/orders')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
