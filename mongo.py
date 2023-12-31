import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI =os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e

# Connect to DB and Collect from DB
conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

coll.update_many({"nationality": "british"}, {"$set": {"hair_color": "red"}})

documents = coll.find({"nationality": "british"})

for doc in documents:
    print(doc)