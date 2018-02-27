from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required="True",
                        help="This field can not be left empty"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required="True",
                        help="Every store needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {"Message": "Item not found"}




    def post(self, name):

        if ItemModel.find_by_name(name):
            return {"Message": "An Item with the name {} already exit".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"Message": "An error occurred while inserting an item"}, 500  # Internal server error

        return item.json(), 201  # 201 is status code for created





    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {"Message": "Item Has been deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]


        item.save_to_db()

        return item.json()


class ItemList(Resource):

    def get(self):

        # return {"Items": list(map(lambda x: x.json(), ItemModel.query.all()))}  # Could use a lambda function

        return {"items": [item.json() for item in ItemModel.query.all()]}  # List comprehension