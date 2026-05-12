from src.util.log_adapter import logger

class CachingMechanism:
    def __init__(self):
        self.frequent_questions = {"hi":"Hello! How can I help you today?",
                                   "hello":"Hello! How can I help you today?",
                                  "good morning":"Hello! How can I help you today?",
                                  "good night":"Hello! How can I help you today?",
                                 "how are you?": "Hello! How can I help you today?",
                                 "good afternoon": "Hello! How can I help you today?"}
                                   
        
    async def check_cached_response(self, user_query):
        try:
            response = None
            for i,v  in self.frequent_questions.items():
                if user_query.lower().strip() == i:
                    response = v
                    break
            return response
        except Exception as e:
            logger.error(f"An error occured in check_cached_response caller: {str(e)}")
            raise Exception(f"An error occured in check_cached_response caller: {str(e)}")