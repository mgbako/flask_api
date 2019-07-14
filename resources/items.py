from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
items = []


class Item(Resource):
    # this is used to parse the request
    parser = reqparse.RequestParser()

    # define argument that will be parsed
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must belong to a store"
                        )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': "Item not found"}, 404

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An Item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': "An Item with name '{}' doesn't exist.".format(name)}, 400

        item.delete()
        return {'message': "Item Deleted"}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save()

        return item.json()


class ItemList(Resource):
    def get(self):

        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

        # return {'items': [item.json() for item in ItemModel.query.all()]}, 200
