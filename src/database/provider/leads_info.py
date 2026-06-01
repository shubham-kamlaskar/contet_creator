import os
from dotenv import load_dotenv
import uuid

from src.database.service.mongo_client import MongoDBClient
from src.models.leads_entry import LeadsEntry
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision

load_dotenv()

class LeadsInfoProvider:
    def __init__(self):
        self.mongo_client = MongoDBClient()
        self.database_name = str(os.getenv("LEADS_DB_NAME"))
        self.collection_name = str(os.getenv("LEADS_COLLECTION_NAME"))
        
    async def get_all_leads(self):
        try:
            leads = self.mongo_client.fetch_all_records_from_collection(self.database_name, self.collection_name)
            return leads
        except Exception as e:
            raise Exception("An error occured in 'get_all_leads' call", str(e))
        
    async def add_leads_entry(self, data: dict):
        try:
            if data:
                update_entry = LeadsEntry(
                id = str(uuid.uuid4()),
                client_name = data.get("client_name", "dummy"),
                request_type = data.get("request_type", "dummy"),
                linkedin_url = data.get("linkedin_url", "dummy"),
                proposal_status= data.get("proposal_status", "dummy"),
                createdAt = get_current_dt_in_milliseconds_precision(),
                )
                
                self.mongo_client.insert_one_item_in_collection(self.database_name, self.collection_name, update_entry.model_dump())
        except Exception as e:
            raise Exception("An error occured in 'add_leads_entry' call", str(e))
        
    async def delete_leads_entry(self, id):
        try:
            self.mongo_client.delete_one_item_from_collection(self.database_name, self.collection_name, {"id": id})
        except Exception as e:
            raise Exception("An error occured in 'delete_leads_entry' call", str(e))
        
    async def find_leads_entry(self, id):
        try:
            entry = self.mongo_client.find_one_item_from_collection(self.database_name, self.collection_name, {"id": id})
            return entry
        except Exception as e:
            raise Exception("An error occured in 'edit_leads_entry' call", str(e))

    async def update_leads_entry(self, id, data: dict):
        try:
            # set updated timestamp
            data = data.copy() if data else {}
            data["updatedAt"] = get_current_dt_in_milliseconds_precision()

            # perform the update
            self.mongo_client.update_one_item_in_collection(self.database_name, self.collection_name, {"id": id}, data)
        except Exception as e:
            raise Exception("An error occured in 'update_leads_entry' call", str(e))
