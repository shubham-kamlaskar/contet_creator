from flask import Blueprint, render_template, request, jsonify
from src.database.provider.leads_info import LeadsInfoProvider
from src.util.log_adapter import logger

leads_management_bp = Blueprint('leads_management_bp', __name__, static_folder="static", template_folder="templates")

leads_info_provider = LeadsInfoProvider()

@leads_management_bp.route('/', methods=['GET'])
async def lead():
    try:
        leads = await leads_info_provider.get_all_leads()
        return render_template('home.html', leads=leads)
    except Exception as e:
        logger.error(f"An error occured in lead caller: {str(e)}")
        return render_template('home.html', leads=[])


# Add lead
@leads_management_bp.route("/add_lead", methods=["POST"])
async def add_lead():
    try:
        data = await request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": f"Unable to save the data"
            }), 400
        
        await leads_info_provider.add_leads_entry(data)
        
        return jsonify({
            "status": "success",
            "message": "Lead added successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"An error occured in add_lead caller: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error adding lead: {str(e)}"
        }), 500


# Delete lead
@leads_management_bp.route("/delete_lead/<id>", methods=["DELETE"])
async def delete_lead(id):
    try:
        if not id:
            return jsonify({
                "status": "error",
                "message": "Lead ID is required"
            }), 400
        
        await leads_info_provider.delete_leads_entry(id)
        
        return jsonify({
            "status": "success",
            "message": "Lead deleted successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"An error occured in delete_lead caller: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error deleting lead: {str(e)}"
        }), 500


# Edit lead
@leads_management_bp.route("/edit_lead/<id>", methods=["PUT"])
async def edit_lead(id):
    try:
        if not id:
            return jsonify({
                "status": "error",
                "message": "Lead ID is required"
            }), 400
        
        data = await request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        await leads_info_provider.update_leads_entry(id, data)
        
        return jsonify({
            "status": "success",
            "message": "Lead updated successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"An error occured in edit_lead caller: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error editing lead: {str(e)}"
        }), 500


# Get single lead (used by frontend to populate edit form)
@leads_management_bp.route("/get_lead/<id>", methods=["GET"])
async def get_lead(id):
    try:
        if not id:
            return jsonify({
                "status": "error",
                "message": "Lead ID is required"
            }), 400
        
        entry = await leads_info_provider.find_leads_entry(id)
        if not entry:
            return jsonify({
                "status": "error",
                "message": "Lead not found"
            }), 404
        
        # Format createdAt properly
        created_at = entry.get("createdAt")
        if hasattr(created_at, "isoformat"):
            created_at = created_at.isoformat()
        
        fetch_lead = {
            "id": entry.get("id") or str(entry.get("_id")),
            "client_name": entry.get("client_name") or "",
            "request_type": entry.get("request_type") or "",
            "proposal_status": entry.get("proposal_status") or "",
            "work_status": entry.get("work_status") or "",
            "fees": entry.get("fees") or "",
            "currency": entry.get("currency") or "",
            "payment_status": entry.get("payment_status") or "",
            "linkedin_url": entry.get("linkedin_url") or "",
            "createdAt": created_at
        }
        
        return jsonify(fetch_lead), 200
        
    except Exception as e:
        logger.error(f"An error occured in get_lead caller: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error fetching lead: {str(e)}"
        }), 500