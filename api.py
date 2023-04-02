from flask import Flask, jsonify,request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)



client = MongoClient('mongodb+srv://shiv_test:test@cluster0.xzzdmgf.mongodb.net/test')
db = client["craft"]
collect = db["products"]






# product apis
@app.route('/products', methods=['GET'])
def get_data():
    data = []
    for doc in collect.find():
        data.append({
            'id': str(doc['_id']),
            'name': doc['name'],
            'price': doc['price'],
            'category': doc['category'],
            'image_link': doc['image_link']

        })
    return jsonify(data)

@app.route('/addProduct', methods=['POST'])
def add_new_document():
    data = request.json
    name = data['name']
    price = data['price']
    category = data['category']
    image = data['image_link']
  
    new_document = {'name': name, 'price': price , 'category':category , 'image_link': image }
    result = collect.insert_one(new_document)
    return jsonify({'message': 'New document added', 'id': str(result.inserted_id)})



@app.route('/prod_update/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = collect.find_one({'_id': ObjectId(product_id)})
    if product:
        product['name'] = request.json['name']
        product['price'] = request.json['price']
        product['category'] = request.json['category']
        product['image_link'] = request.json['image_link']
        collect.update_one({'_id': ObjectId(product_id)}, {'$set': product})
        return jsonify({'message': 'Product updated successfully'})
    else:
        return jsonify({'message': 'Product not found'})


@app.route('/prod_delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = collect.delete_one({'_id': ObjectId(product_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'})
    
@app.route('/prod/<product_id>', methods=['GET'])
def findOne_product(product_id):
        product = collect.find_one({'_id': ObjectId(product_id)})
        if product:
            response = {
                'id': str(product['_id']),
                'name': product['name'],
                'price': product['price'],
                'category': product['category'],
                'image_link': product['image_link']
            }
        else:
            response = {'message': 'Product not found'}
        return jsonify(response)





if __name__ == "__main__":
     app.run(debug=True)


     