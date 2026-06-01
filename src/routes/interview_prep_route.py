from flask import render_template, Blueprint, jsonify, request
from src.util.log_adapter import logger
from src.processor.interview_prep_processor import generate_prep_kit

interview_bp = Blueprint("interview_bp", __name__, static_folder="static", template_folder="templates")


@interview_bp.route("/interview", methods= ['GET'])
def interview():
    try:
        return render_template("interview-prep.html")
    except Exception as e:
        logger.error(f"An error occured in interview caller: {str(e)}")
        raise Exception(f"An error occured in interview caller: {str(e)}")
    
@interview_bp.route("/prep_kit", methods=['POST'])
def prep_kit():
    try:
        result = generate_prep_kit(request)

        if not isinstance(result, dict):
            return jsonify({
                "status": "error",
                "message": "Invalid prep kit response format from processor."
            }), 500

        return jsonify({
            "status": "success",
            "reply": result.get("response", ""),
            "data": result,
        }), 200
    except ValueError as ve:
        logger.error(f"Invalid request in prep_kit caller: {str(ve)}")
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except Exception as e:
        logger.error(f"An error occured in prep_kit caller: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error generating prep kit: {str(e)}"
        }), 500