from flask import render_template, request, jsonify, Blueprint
import uuid
from src.processor.conversation_flow_processor import internal_conversations
from src.util.log_adapter import logger

conversation_bp = Blueprint("conversation_bp", __name__, static_folder="static", template_folder="templates")


@conversation_bp.route("/chat", methods= ['GET'])
def home():
    try:
        return render_template("chat.html")
    except Exception as e:
        logger.error(f"An error occured in home caller: {str(e)}")
        raise Exception(f"An error occured in home caller: {str(e)}")

@conversation_bp.route("/response", methods=['POST'])
def chat():
    try:
        response = internal_conversations(request)

        return jsonify({
            "status": "success",
            "reply": response.get('response', ''),
            "tokens_used": response.get('current_token_count', 0),
            "is_interrupt": response.get('is_interrupt', False)
        }), 200
    except Exception as e:
        logger.error(f"An error occured in chat caller: {str(e)}")
        raise Exception(f"An error occured in chat caller: {str(e)}")

@conversation_bp.route("/newchat", methods=['POST'])
def newchat():
    try:
        session_id = str(uuid.uuid4())
        return jsonify({
            "status": "success",
            "session_id": session_id
        }), 200
    except Exception as e:
        logger.error(f"An error occured in newchat caller: {str(e)}")
        raise Exception(f"An error occured in newchat caller: {str(e)}")