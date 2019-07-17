from flask_restful import Resource, Api, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from password import hashing, compare

# You need to perse the request
user_parser = reqparse.RequestParser()

# Define argument that will be parsed
user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        
        if not user:
            return {"message": "User with the id {} does not exist".format(user_id)}, 404

        return user.json(), 201

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User with the id {} does not exist".format(user_id)}, 404

        user.delete()
        return {'message': "User Deleted"}, 200

class UserList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.find_all()]}, 201

class UserRegister(Resource):
  
    def post(self):
        data = user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
    
        user = UserModel(data['username'], data['password'])
        
        user.save()

        return {"message": "User created successfully.", 'data': user.json()}, 201

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        # Get data from parser
        data = user_parser.parse_args()

        # Find User from the database
        user = UserModel.find_by_username(data['username'])

        # Check password
        if user and user.password_is_valid(data['password']):
            return {
                'access_token': create_access_token(identity=user.id, fresh=True),
                'refresh_token': create_refresh_token(user.id)
            }, 200

        return {"message": "Invalid Credentials"}