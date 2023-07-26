import pytest
from app import validate_data, dishes_schema, orders_schema


def test_dishes_schema():
    # Test the dishes schema definition
    data = {
        'id': 1,
        'name': 'Dish 1',
        'price': 10.0,
        'availability': True
    }
    assert validate_data(data, dishes_schema) == True

    # Test invalid dish schema
    invalid_data = {
        'id': '1',
        'name': 'Invalid Dish',
        'price': '10.0',
        'availability': 'True'
    }
    assert validate_data(invalid_data, dishes_schema) == False

def test_orders_schema():
    # Test the orders schema definition
    data = {
        'id': 1,
        'customer_name': 'John Doe',
        'status': 'received',
        'items': [
            {'dish_id': 1, 'dish_name': 'Dish 1'}
        ],
        'total_price': 20.0
    }
    assert validate_data(data, orders_schema) == True

    # Test invalid order schema
    invalid_data = {
        'id': '1',
        'customer_name': 'John Doe',
        'status': 'received',
        'items': [
            {'dish_id': '1', 'dish_name': 'Invalid Dish'}
        ],
        'total_price': '20.0'
    }
    assert validate_data(invalid_data, orders_schema) == False
