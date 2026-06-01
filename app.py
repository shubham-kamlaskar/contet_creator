from flask import Flask
import warnings

from src.routes.conversation_route import conversation_bp
from src.routes.leads_routes import leads_management_bp
from src.routes.interview_prep_route import interview_bp

warnings.filterwarnings("ignore")

app = Flask(__name__)

app.register_blueprint(conversation_bp)

app.register_blueprint(leads_management_bp)

app.register_blueprint(interview_bp)

if __name__ == "__main__":
    app.run(
    debug=True,
    use_reloader=True,
    port=5874,
    host="0.0.0.0"
)

    