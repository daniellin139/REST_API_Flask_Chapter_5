import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"messages": "The item with name {} already exists.".format(name)}, 400

        #data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {"message":"An error occurred inserting the item."}, 500
        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"messages": "Item deleted"}

    def put(self, name):
        #data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel(name, data['price'])
        if item is None:
            update_item.insert()
        else:
            update_item.update()
        return update_item.json()


class Items(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        connection.close()
        return {'items': items}, 200
