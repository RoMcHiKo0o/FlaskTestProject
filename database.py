from pymongo import MongoClient


conn_str = 'mongodb+srv://RoMcHiKo0o:uYnmaFzV5T8FALT@cluster0.8qdm82y.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(conn_str)

db = client.test_database
