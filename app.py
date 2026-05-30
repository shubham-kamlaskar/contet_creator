from quart import Quart
import warnings

from src.routes.conversation_route import conversation_bp
from src.routes.leads_routes import leads_management_bp

warnings.filterwarnings("ignore")

app = Quart(__name__)

app.register_blueprint(conversation_bp)

app.register_blueprint(leads_management_bp)

if __name__ == "__main__":
    app.run(debug=True,port=5874,host="0.0.0.0")

    