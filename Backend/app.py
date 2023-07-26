import json
import pymongo
from json import dumps
from flask import Flask, jsonify, request
from flask_cors import CORS
from bson.errors import InvalidId
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
app.secret_key = 'Kirti@1807'

# MongoDB configuration
cluster0 = MongoClient('mongodb+srv://kirti:kirti@cluster0.xxyu7.mongodb.net/zomato?retryWrites=true&w=majority')
db = cluster0['zomato']
dishes_collection = db['dishes']
orders_collection = db['orders']
# Schema definitions
dishes_schema = {
    'id': {'type': 'int'},
    'name': {'type': 'string'},
    'price': {'type': 'float'},
    'availability': {'type': 'bool'}
}

orders_schema = {
    'id': {'type': 'int'},
    'customer_name': {'type': 'string'},
    'status': {'type': 'string', 'default': 'received'},
    'items': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'dish_id': {'type': 'int'},
                'dish_name': {'type': 'string'}
            }
        }
    },
    'total_price': {'type': 'float', 'nullable': True}
}

def validate_data(data, schema):
    # Function to validate data against the given schema
    # You can use a library like 'cerberus' for schema validation
    pass

def get_next_order_id():
    # Function to get the next order ID
    # You can modify this function based on your requirements
    max_id = orders_collection.find_one(sort=[('id', -1)])
    return max_id['id'] + 1 if max_id else 1

def get_dish_by_id(dish_id):
    # Function to get a dish by its ID
    dish = dishes_collection.find_one({'id': dish_id})
    return dish

@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes = list(dishes_collection.find())
    return json_util.dumps(dishes)


@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = get_dish_by_id(dish_id)
    if dish:
        return json_util.dumps(dish)
    else:
        return jsonify({'error': 'Dish not found'}), 404


@app.route('/dishes', methods=['POST'])
def create_dish():
    data = request.json
    validate_data(data, dishes_schema)

    # Get the highest ID value from the dishes collection
    max_id = dishes_collection.find_one(sort=[('id', -1)])
    new_id = max_id['id'] + 1 if max_id else 1

    dish = {
        'id': new_id,
        'name': data['name'],
        'price': data['price'],
        'availability': data['availability'],
    }

    result = dishes_collection.insert_one(dish)
    inserted_id = str(result.inserted_id)
    dish['_id'] = inserted_id
    return jsonify(dish), 201



from bson import ObjectId
@app.route('/dishes/<string:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    data = request.json
    validate_data(data, dishes_schema)

    try:
        object_id = ObjectId(dish_id)
    except bson.errors.InvalidId:
        return jsonify({'error': 'Invalid dish ID'}), 400

    dish = get_dish_by_id(object_id)

    if dish:
        dish['name'] = data.get('name', dish['name'])
        dish['price'] = data.get('price', dish['price'])
        dish['availability'] = data.get('availability', dish['availability'])
        dishes_collection.update_one({'_id': object_id}, {'$set': dish})

        # Retrieve the updated dish from the database
        updated_dish = get_dish_by_id(object_id)

        # Convert the ObjectId to a string
        updated_dish['_id'] = str(updated_dish['_id'])

        return jsonify(updated_dish)
    else:
        return jsonify({'error': 'Dish not found'}), 404



@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = get_dish_by_id(dish_id)
    if dish:
        dishes_collection.delete_one({'id': dish_id})
        return jsonify({'message': 'Dish deleted', 'dish_id': dish_id})

    return jsonify({'error': 'Dish not found'}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    validate_data(data, orders_schema)
    order_id = get_next_order_id()
    data['id'] = order_id
    data['status'] = 'received'
    total_price = 0
    for item in data['items']:
        dish = get_dish_by_id(item['dish_id'])
        if dish:
            total_price += dish['price'] * item['quantity']
    data['total_price'] = total_price
    orders_collection.insert_one(data)
    return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    new_status = request.json.get('status', '')
    order = orders_collection.find_one({'id': order_id})
    if order:
        order['status'] = new_status
        orders_collection.update_one({'id': order_id}, {'$set': order})
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    if status:
        orders = list(orders_collection.find({'status': status}))
    else:
        orders = list(orders_collection.find())
    return json_util.dumps(orders)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
