from src.guardrails.caching_provider import CachingMechanism
from src.agents.langchain_agent import AgentProvider
from src.util.log_adapter import logger
from src.database.provider.conversation_provider import update_conversations_in_db
agent = AgentProvider()
caching = CachingMechanism()

def internal_conversations(request):
    try:
        user_query = ""
        response = {}
        data = request.get_json()
        if data:
            user_query = data.get("message", "")
            response: dict = caching.check_cached_response(user_query)
            
            if not response.get("response"):
                response: dict = agent.get_agent_response(user_query)

                
        update_conversations_in_db(response)
        return response
    except Exception as e:
        logger.error(f"An error occured in internal_conversations caller: {str(e)}")
        raise Exception(f"An error occured in internal_conversations caller: {str(e)}")