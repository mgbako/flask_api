from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from security import authenticate, identity

# Models
from resources.users import User
from resources.items import Item, ItemList
from resources.storeController import StoreController, StoreListController

app = Flask(__name__)
app.secret_key = 'john'

# For Postresql: 'postgresql://localhost/appdb'
# For SQLite: 'sqlite:///data.db'
postresdb = 'postgresql://localhost/appdb'
sqldb = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = sqldb
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# Create DB Tables
@app.before_first_request
def create_tables():
  db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(StoreController, '/stores/<string:name>')

api.add_resource(ItemList, '/items')
api.add_resource(StoreListController, '/stores')

api.add_resource(User, '/users')


if __name__ == '__main__':
  from db import db
  db.init_app(app)

  # docker
  # app.run(debug=True, port=5000, host='0.0.0.0')

  # Regular
  app.run(debug=True, port=5000, host='0.0.0.0')