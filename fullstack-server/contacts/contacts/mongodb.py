from pymongo import MongoClient
import gridfs

client = MongoClient('mongodb+srv://es:es7666@cluster0.jjxan.mongodb.net/sample_db?retryWrites=true&w=majority&appName=Cluster0')
database = client['sample_db']
contacts_collection = database['contacts']
fs = gridfs.GridFS(database)
