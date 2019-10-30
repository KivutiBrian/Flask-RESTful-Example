from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) #api works with Resourses which must be a class

items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)

        # for item in items:
        #     if item['name'] == name:
        #         return item
        return {'item':item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x : x['name'] == name, items), None):
            return {'message': "Item with the name '{}' already exist".format(name)},400

        data = request.get_json() #force true means you dont need the content type header - its dangerous
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=5000)
