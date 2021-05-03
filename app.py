import os

from flask import Flask
from flask_restful  import Api
from flask_jwt import JWT

from security import authenticate,  identify
from resources.user import UserRegister
from resources.item import Item, Items


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'juniper'
api = Api(app)

jwt = JWT(app, authenticate,  identify) #/auth

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db



    db.init_app(app)
    app.run(port=5000)
