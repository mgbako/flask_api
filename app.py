import os 

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
# from flask_sqlalchemy import SQLAlchemy
from security import authenticate, identity

# Models
from resources.users import User, UserList, UserLogin, UserRegister
from resources.items import Item, ItemList
from resources.storeController import StoreController, StoreListController

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# For Postresql: 'postgresql://localhost/appdb'
# For SQLite: 'sqlite:///data.db'
# postresdb = os.getenv('')
sqldb = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This enables JWT Errors to show
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWTManager(app)

# Create DB Tables
@app.before_first_request
def create_table():
  db.create_all()

api.add_resource(Item, '/items/<string:name>')
api.add_resource(StoreController, '/stores/<string:name>')

api.add_resource(ItemList, '/items')
api.add_resource(StoreListController, '/stores')

api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
  from db import db
  db.init_app(app)

  # docker
  # app.run(debug=True, port=5000, host='0.0.0.0')

  # Regular
  app.run(debug=True, port=5000, host='0.0.0.0')