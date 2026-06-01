import os
from dotenv import load_dotenv
load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



class MongoDBClient:
    def __init__(self):
        self.uri = os.getenv('MONGODB_CONNECTION_STRING')
        
    def get_mongo_client(self):
        try:
            # Create a new client and connect to the server
            client = MongoClient(self.uri, server_api=ServerApi('1'))
            return client
        except Exception as e:
            raise Exception("An error occured in get_mongo_client call", str(e))
        
    def get_collection_client(self, database_name: str, collection_name: str):
        client = self.get_mongo_client()
        db = client[database_name]
        collection = db.get_collection(collection_name) 
        return collection
    
    def insert_one_item_in_collection(self, database_name: str, collection_name: str, data: dict):
        collection = self.get_collection_client(database_name, collection_name)
        collection.insert_one(data)
        
    def insert_many_item_in_collection(self, database_name: str, collection_name: str, data: list[dict]):
        collection = self.get_collection_client(database_name, collection_name)
        collection.insert_many(data)
        
    def update_one_item_in_collection(self, database_name: str, collection_name: str, filter_items: dict, update_data: dict):
        collection = self.get_collection_client(database_name, collection_name)
        collection.update_one(filter_items, {"$set": update_data})
        
    def find_one_item_from_collection(self, database_name: str, collection_name: str, filter_items: dict):
        collection = self.get_collection_client(database_name, collection_name)
        data = collection.find_one(filter_items)
        return data
    
    def find_many_item_from_collection(self, database_name: str, collection_name: str, filter_items: dict):
        collection = self.get_collection_client(database_name, collection_name)
        data = collection.find(filter_items)
        return data
    
    def delete_one_item_from_collection(self, database_name: str, collection_name: str, filter_items: dict):
        collection = self.get_collection_client(database_name, collection_name)
        collection.delete_one(filter_items)
        
    def count_item_from_collection(self, database_name: str, collection_name: str, filter_items: dict):
        collection = self.get_collection_client(database_name, collection_name)
        count_item = collection.count_documents(filter_items)
        return count_item
        
    def fetch_all_records_from_collection(self, database_name: str, collection_name: str):
        collection = self.get_collection_client(database_name, collection_name)
        data = collection.find()
        return data
    
    def count_all_records_from_collection(self, database_name: str, collection_name: str):
        collection = self.get_collection_client(database_name, collection_name)
        data = collection.count_documents({})
        return data