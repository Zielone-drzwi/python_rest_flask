#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///fejkowa.db')
app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from fejkowa") # This line performs query and returns json result
        return {'id': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        data = request.json['data']
        lat = request.json['lat']
        lon = request.json['lon']
        kompas = request.json['kompas']
        napiecie = request.json['napiecie']
        pochylenie = request.json['pochylenie']
        przechylenie = request.json['przechylenie']

    

        query = conn.execute("insert into fejkowa values(null,'{1}','{2}','{3}', \
                             '{4}','{5}','{6}',{7})".format(data,lat,lon,
                             kompas, napiecie, pochylenie, przechylenie))
        return {'status':'ok'}

    
class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select data, lat, lon, kompas from fejkowa;")
        result = {'dane': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    
class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from fejkowa where id =%d "  %int(employee_id))
        result = {'dane': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run()
