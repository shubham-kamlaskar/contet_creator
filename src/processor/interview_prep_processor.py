from src.agents.langchain_agent import AgentProvider
from src.util.log_adapter import logger
from src.agents.ollama_llm_provider import LLMProvider

agent = AgentProvider()
llm_provider = LLMProvider()

def generate_prep_kit(request):
    data = request.get_json(silent=True)
    print(data)
    if not data or not isinstance(data, dict):
        raise ValueError("Invalid JSON payload for prep kit generation.")

    try:
        user_query = f"Generate an interview preparation kit for the following inputs: {data}."
        messages = [
            # {"role": "system","content":"""You need to generate an interview preparation kit based on the user's input.\n
            #  The kit should include a list of potential interview questions, key topics to focus on, and recommended resources for preparation.\n
            #  You need to ensure that the generated kit is comprehensive, relevant to the user's input and provides actionable insights for interview preparation.\n
            #  The reponse should be in a structured format with clear sections for questions, topics and resources in json format only.\n
            #  Give me below sections in response:\n
            #  1. Interview Questions\n
            #  2. Answer framework & strategy\n
            #  3. Key concepts to reviese\n
            #  4. Do's and Dont's\n
            #  5. Sample answer to walkthrough\n
            #  6. 7-days preparation plan"""},
             {"role": "user", "content": user_query},
        ]
        llm_client = llm_provider.llm_client()
        response_kit = llm_client.invoke(messages)
        if response_kit:
            return response_kit.content
        else:
            return {
                "response": "Failed to generate interview preparation kit. Please try again later."
            }
    except Exception as e:
        logger.error(f"An error occured in generate_prep_kit: {str(e)}")
        raise

