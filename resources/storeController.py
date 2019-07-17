from flask_restful import Resource
from models.store import Store


class StoreController(Resource):
    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return item.json(), 201

        return {"message": "Store not found"}, 404

    def post(self, name):
        if Store.find_by_name(name):
            return {"message": "A store with this name '{}' already exists.".format(name)}, 400
        
        store = Store(name)

        try:
            store.save()
        except:
            return {"message": "An error occured inserting the store."}, 500

        return store.json()

    def delete(self, name):
        store = Store.find_by_name(name)
        
        if store is None:
            return {'message': "A Store with name '{}' doesn't exist.".format(name)}, 400
        
        try:
            store.delete()
        except:
            return {'message': "An error occured deleting the store."}, 500

        return {"message": "Store Deleted"}


class StoreListController(Resource):
    def get(self):
        return {'stores': [x.json() for x in Store.find_all()]}, 201