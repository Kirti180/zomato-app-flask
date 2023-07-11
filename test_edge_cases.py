import pytest
from app import app


@pytest.fixture
def client():
    # Create a test client using Flask's test client
    with app.test_client() as client:
        yield client

def test_invalid_dish_id(client):
    # Test GET /dishes/<int:dish_id> with invalid dish ID
    response = client.get('/dishes/invalid_id')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json['error'] == 'Invalid dish ID'

def test_invalid_order_id(client):
    # Test PUT /orders/<int:order_id> with invalid order ID
    data = {
        'status': 'completed'
    }
    response = client.put('/orders/invalid_id', json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json['error'] == 'Invalid order ID'
