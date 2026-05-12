import os
from dotenv import load_dotenv

from src.database.service.mongo_client import MongoDBClient
from src.models.conversation_object import Conversations
from src.util.datetime_helper import get_current_dt_in_milliseconds_precision
from src.util.log_adapter import logger

load_dotenv()

mongodb_client = MongoDBClient()
db_name = str(os.getenv("DB_NAME"))
collection_name = str(os.getenv("COLLECTION_NAME"))

def update_conversations_in_db(data: dict):
    try:
        data = Conversations(
                user_query = data.get('user_query', ''),
                response = data.get('response', ''),
                llm_model= data.get('llm_model', ''),
                tool_used=  data.get('tool_used', []),
                token_count= data.get('token_count', {}),
                createdAt = get_current_dt_in_milliseconds_precision(),
                updatedAt = get_current_dt_in_milliseconds_precision()
            )
        
        mongodb_client.insert_one_item_in_collection(db_name, collection_name, data.model_dump())
    except Exception as e:
        logger.error(f"An error occured in update_conversations_in_db call: {str(e)}")
        raise Exception(f"An error occured in update_conversations_in_db call: {str(e)}")