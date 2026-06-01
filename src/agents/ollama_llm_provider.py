import os
from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import ChatOllama
# from src.util.log_adapter import logger

class LLMProvider:
    def __init__(self):
        self.llm_model_name = str(os.getenv('LLM_MODEL_NAME'))
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
        
    def llm_client(self):
        try:
            llm = ChatOllama(
                model=self.llm_model_name,
                validate_model_on_init=True,
                temperature=self.llm_temperature,
            )
            
            return llm
        except Exception as e:
            # logger.error(f"Error initializing Ollama llm_client", str(e))
            raise Exception(f"Error initializing Ollama llm_client", str(e))

# if __name__ == "__main__":
#     llm_provider = LLMProvider().llm_client().invoke([{"role": "user", "content": "What is the capital of France?"}])
#     print(llm_provider.content)