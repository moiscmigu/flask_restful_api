from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Can be any db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  #Turns off flask modification tracker, but not the SQLAlchemy mod tracker
app.secret_key = "jose"
api = Api(app)  # Can easily add resources to this "app"




"""
    CONFIGURING FLASK-JWT 
"""
# app.config['JWT_AUTH_URL_RULE'] = '/login'  # Changes the authentication endpoint /your_name
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # config JWT to expire within half an hour
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # config JWT auth key name to be 'email' instead of default 'username'


jwt = JWT(app, authenticate, identity)


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

