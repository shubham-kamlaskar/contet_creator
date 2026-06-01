import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


from src.util.log_adapter import logger
from src.prompt.prompt_store import Prompt
from src.models.conversation_object import IntervisionObject
from src.tools.tool_provider import getTools
from src.agents.ollama_llm_provider import LLMProvider
from src.tools.tool_error import handle_tool_errors
from langchain.agents.middleware import HumanInTheLoopMiddleware

memory_checkpointer = InMemorySaver()
llm_provider = LLMProvider()

  
class AgentProvider:
    def __init__(self):
        self.ai_agent_name = str(os.getenv('AI_AGENT_NAME'))
        self.ai_agent_version = str(os.getenv("AI_AGENT_VERSION"))
        self.agent = None
        self.session_id = "81d9c347-f032-455e-9805-77e6e9198abc"
        

    def get_agent_client(self):
        try:
            if self.agent is None:  
                self.agent = create_agent(
                    model= llm_provider.llm_client(),
                    tools=getTools,
                    system_prompt=(Prompt.DEFAULT_SYSTEM_PROMPT + Prompt.RESPONSE_FORMATTING + Prompt.CONTENT_CREATION_GUIDELINES + Prompt.GENERAL_INFO + Prompt.INFO_NOT_AVAILABLE),
                    checkpointer=memory_checkpointer,
                    debug=True,
                    middleware=[handle_tool_errors]
                )

        except Exception as e:
            logger.error(f"Error initializing agent client: {str(e)}")
            raise Exception(f"Error initializing agent client: {str(e)}")
        
    def get_agent_response(self, user_query: str, session_id: str):
        try:
            if self.agent is None:
                self.get_agent_client()
                
            output = self.agent.invoke(
                {
                    "messages": [{"role": "user", "content": user_query}],
                },
                    config ={"configurable": {"thread_id": session_id}},
                    version="v2"
            )
            return self._generated_response(user_query, output)
            
        except Exception as e:
            logger.error(f"Error getting agent response: {str(e)}")
            raise Exception(f"Error getting agent response: {str(e)}")
        
    
    def _generated_response(self, user_query, output):
        if output:
                is_interrupts = output.interrupts
                human_intervisions = []
                if is_interrupts:
                    for i in is_interrupts:
                        value = i.value
                        actions_requests = value.get('action_requests', [])
                        if len(actions_requests) > 0:
                            for request in actions_requests:
                                args = request.get("args", {})
                                content = args.get("content")
                        review_configs = value.get('review_configs', [])
                        if len(review_configs) > 0:
                            for review in review_configs:
                                allowed_decisions = review.get('allowed_decisions')
                                action_name = review.get('action_name')
                        human_intervisions.append(IntervisionObject(
                            content = content,
                            allowed_actions= allowed_decisions,
                            action_name= action_name
                        ))
                        
                    response = {
                        "user_query": user_query,
                        "response": human_intervisions[0].content,
                        "is_interrupt": True,
                        "tool_used": [human_intervisions[0].action_name],
                        "llm_model": "qwen3.5",
                        "token_count": {}
                    }
                
                else:
                    value = output.value
                    messages = value.get("messages", [])
                    tool_calls = []
                    if messages:
                        response_call = messages[-1] if messages else None
                        answer = response_call.content
                        tool_calls = messages[-2].name
                        if tool_calls is None:
                            tool_calls = []
                        metadata = response_call.response_metadata
                        llm_model = metadata.get('model', '')
                        token_count = response_call.usage_metadata
                    else:
                        answer =  "Failed to generate any response."
                    
                    response = {
                        "user_query": user_query,
                        "response": answer,
                        "is_interrupt": False,
                        "tool_used": tool_calls,
                        "llm_model": llm_model,
                        "token_count": token_count
                    }
                
        return response   
