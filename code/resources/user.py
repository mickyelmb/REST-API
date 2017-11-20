import sqlite3
from flask_restful import  Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")


    def post(self):
       data = UserRegister.parser.parse_args()

       if UserModel.find_by_username(data['username']):
           return {"message": "A user with that username already exists"}, 400

       user = UserModel(**data) #for each of the keys in data get the value
       user.save_to_db()
       # conn = sqlite3.connect('data.db')
       # cursor = conn.cursor()
       #
       # query = "INSERT INTO users  VALUES (NULL, ?, ?)"
       # cursor.execute(query, (data['username'], data['password']))
       #
       # conn.commit()
       # conn.close()
       return {"message": "User created successfully."}, 201