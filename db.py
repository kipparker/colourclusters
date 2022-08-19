import os

import pymongo
import conf


def get_database(db="sky_colours") -> pymongo.database.Database:
    connstr = f"mongodb+srv://{conf.MONGO_USER}:{conf.MONGO_PASSWD}@cluster0.67zsi.mongodb.net/?retryWrites=true&w=majority"
    client: pymongo.MongoClient = pymongo.MongoClient(connstr)
    return client[db]
