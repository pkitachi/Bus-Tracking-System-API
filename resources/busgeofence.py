from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from decimal import Decimal
from db import query

class BusGeoFence(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        parser.add_argument('latitude',type=str,required=True,help="latitude cannot be left blank!")
        parser.add_argument('longitude',type=str,required=True,help="logitude cannot be left blank!")
        parser.add_argument('pointNum',type=int,required=True,help="pointNum cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO BusGeofence VALUES ( {data['routeId']},{Decimal(data['latitude'])},
                                                    {Decimal(data['longitude'])},{data['pointNum']})""")
        except:
            return {"message" : "An error occurred while updating."}, 500
        return data,201

    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""DELETE FROM BusGeofence WHERE routeId={data['routeId']}""")
        except:
            return {"message" : "An error occurred while deleting."}, 500
        return {"message" : "Deleted successfully."}

    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('routeId',type=int,required=True,help="routeId cannot be left blank!")
        data=parser.parse_args()
        try:
            result=query(f"""SELECT * FROM BusGeofence WHERE routeId={data['routeId']}""",return_json=False)
            result=sorted(result,key=lambda x:x['pointNum'])
            return jsonify([(x['latitude'],x['longitude']) for x in result])
        except:
            return {"message" : "An error occurred while accessing BusGeofence table."}, 500
