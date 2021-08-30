from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

# initial_args = reqparse.RequestParser()
# initial_args.add_argument("ix_id", type=str)
# initial_args.add_argument("net_id", type=str)

def read_json(file_name):
  with open(file_name, 'r', encoding='utf8') as f:
      return json.load(f)


class HelloWorld(Resource):
  def get(self):
    return {"message": "Hello World"}

class Ix(Resource):
  def get(self):
    netjson = read_json('ix.json')
    return {"data": netjson}

class IxNets(Resource):
  def get(self, ix_id):
    netjson = read_json('netixlan.json')['data']
    res = []
    for ix in netjson:
      if ix['ix_id'] == int(ix_id):
        res.append(ix['net_id'])
      # print('esse eh o ix',ix)
    return {"message": "This is a Ix Net", "data": res, "len": len(res)}

class NetName(Resource):
  def get(self, net_id):
    netjson = read_json('net.json')['data']
    res = []
    for ix in netjson:
      if ix['id'] == int(net_id):
        res.append(ix['name'])
        print('entrei')
      # print('esse eh o ix',ix)
    return {"message": "This is a NetName", "data": res}

api.add_resource(HelloWorld, '/')
api.add_resource(Ix, '/api/ix')
api.add_resource(IxNets, '/api/ixnets/<string:ix_id>')
api.add_resource(NetName, '/api/netname/<string:net_id>')



if __name__ == "__main__":
  app.run(debug=True)