from flask_restful import  Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return  item.json()
        return {'message': 'Item not found'}, 404

       # item = next(filter(lambda x: x['name'] == name, items), None)
       # return {'item': item}, 200 if item else 404


    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists. ".format(name)}, 400

        data = Item.parser.parse_args()

       # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item successfully deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
           #item = ItemModel(name, data['price'], data['store_id'])
           item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return  {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # conn = sqlite3.connect('data.db')
        # cursor = conn.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # conn.commit()
        # conn.close()
        # return {'items': items}
