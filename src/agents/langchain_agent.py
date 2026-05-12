import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


from src.util.log_adapter import logger
from src.prompt.prompt_store import Prompt
from src.tools.tool_provider import getTools
from src.agents.ollama_llm_provider import LLMProvider
from src.tools.tool_error import handle_tool_errors

debug_mode = os.getenv('AGENT_DEBUG_MODE', 'True')
memory_checkpointer = InMemorySaver()
llm_provider = LLMProvider()

    
class AgentProvider:
    def __init__(self):
        self.ai_agent_name = str(os.getenv('AI_AGENT_NAME'))
        self.ai_agent_version = str(os.getenv("AI_AGENT_VERSION"))
        self.agent = None
        self.session_id = "81d9c347-f032-455e-9805-77e6e9198abc"

    async def get_agent_client(self):
        try:
            agent = create_agent(
                    model=llm_provider.llm_client(),
                    tools=getTools,
                    system_prompt=(Prompt.DEFAULT_SYSTEM_PROMPT + Prompt.RESPONSE_FORMATTING + Prompt.CONTENT_CREATION_GUIDELINES + Prompt.GENERAL_INFO + Prompt.INFO_NOT_AVAILABLE),
                    checkpointer=memory_checkpointer,
                    debug=True,
                    middleware=[handle_tool_errors]
                )
            
            return agent

        except Exception as e:
            logger.error(f"Error initializing agent client: {str(e)}")
            raise Exception(f"Error initializing agent client: {str(e)}")
        
    async def get_agent_response(self, user_query: str):
        try:
            agent = await self.get_agent_client()
                
            response = await agent.ainvoke(
                {
                    "messages": [{"role": "user", "content": user_query}],
                },
                    config ={"configurable": {"thread_id": "self.session_id"}},

            )
            if response:
                messages = response.get("messages", [])

                response_call = messages[-1] if messages else None

                answer = response_call.content
            else:
                answer =  "Failed to generate any response."
                
            return answer   

        except Exception as e:
            logger.error(f"Error getting agent response: {str(e)}")
            raise Exception(f"Error getting agent response: {str(e)}")
