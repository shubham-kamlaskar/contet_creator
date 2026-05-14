from src.guardrails.caching_provider import CachingMechanism
from src.agents.langchain_agent import AgentProvider
from src.util.log_adapter import logger
from src.database.provider.conversation_provider import update_conversations_in_db
from src.util.prompt_evaluator import calculate_total_token_count
agent = AgentProvider()
caching = CachingMechanism()

def internal_conversations(request):
    try:
        user_query = ""
        response = {}
        data = request.get_json()
        if data:
            user_query = data.get("message", "")
            token_used = int(data.get('tokens_used', 0))
            response: dict = caching.check_cached_response(user_query)
            
            if not response.get("response"):
                response: dict = agent.get_agent_response(user_query)

        current_token_count = 0
        token_count = response.get('token_count', {})
        if token_count:
            current_token_count = token_count.get('total_tokens', 0)

        response['current_token_count'] = calculate_total_token_count(existing_tokens=token_used, total_tokens=current_token_count)
        
        update_conversations_in_db(response)
        return response
    except Exception as e:
        logger.error(f"An error occured in internal_conversations caller: {str(e)}")
        raise Exception(f"An error occured in internal_conversations caller: {str(e)}")