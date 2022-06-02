
import json
from database import Database
from src import environement
Database.initialize()



f = open('Country.json')
Country = json.load(f)



for Polygon in Country[0].get('features'):
    Region = {}
    Region['name']=Polygon.get('properties').get('nom')
    Region['country']="France"
    geometry={}
    geometry['type']=Polygon.get('geometry').get('type')
    geometry['coordinates']=Polygon.get('geometry').get('coordinates')
    Region['geometry']=geometry

    Database.DATABASE[environement.COLLECTION_REGION].insert_one(Region)



print("Regions created ")




