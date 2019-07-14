from flask_restful import Resource, Api, reqparse
from models.user import UserModel


class User(Resource):

    # You need to perse the request
    parser = reqparse.RequestParser()

    # Define argument that will be parsed
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    def post(self):
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save()

        return {"message": "User created successfully."}, 201

    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
