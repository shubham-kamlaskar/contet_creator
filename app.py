from flask import Flask
import warnings

from src.routes.conversation_route import conversation_bp

warnings.filterwarnings("ignore")

app = Flask(__name__)

app.register_blueprint(conversation_bp)


if __name__ == "__main__":
    app.run(debug=True)

    