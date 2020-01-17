__author__ = "Fabio Barbieri"

import pymongo, os

class Database(object):
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize(database_name):
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data, check_keys=True):
        Database.DATABASE[collection].insert(data, check_keys=check_keys)

    @staticmethod
    def find(collection, query=None):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, key, data):
        return Database.DATABASE[collection].update_one(key, {"$set": data}, upsert=True)

    @staticmethod
    def replace_one(collection, key, data):
        return Database.DATABASE[collection].replace_one(key, data)

    @staticmethod
    def delete(collection, query):
        pass