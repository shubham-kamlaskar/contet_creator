from src.agents.langchain_agent import AgentProvider
from flask import Flask, render_template, request, jsonify
from src.guardrails.caching_provider import CachingMechanism
from src.util.log_adapter import logger

app = Flask(__name__)

agent = AgentProvider()
caching = CachingMechanism()


@app.route("/", methods= ['GET'])
async def home():
    try:
        return render_template("chat.html")
    except Exception as e:
        logger.error(f"An error occured in home caller: {str(e)}")
        raise Exception(f"An error occured in home caller: {str(e)}")

@app.route("/chat", methods=['POST'])
async def chat():
    try:
        response = None
        data = request.get_json()
        if data:
            user_query = data.get("message", "")
            response = await caching.check_cached_response(user_query)
            if response is None:
                response = await agent.get_agent_response(user_query)
            
        return jsonify({
            "status": "success",
            "reply": response
        })
    except Exception as e:
        logger.error(f"An error occured in chat caller: {str(e)}")
        raise Exception(f"An error occured in chat caller: {str(e)}")

if __name__ == "__main__":
    app.run()

    