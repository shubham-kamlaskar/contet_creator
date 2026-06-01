from src.agents.langchain_agent import AgentProvider
from src.util.log_adapter import logger

agent = AgentProvider()

async def generate_prep_kit(request):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise ValueError("Invalid JSON payload for prep kit generation.")

    try:
        user_query = f"Generate an interview preparation kit for the following inputs: {data}."
        kit = await agent.get_agent_response(user_query)
        return kit
    except Exception as e:
        logger.error(f"An error occured in generate_prep_kit: {str(e)}")
        raise

