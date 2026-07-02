import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJETO_FLASK_DIR = os.path.join(BASE_DIR, "ProjetoFlask")

if PROJETO_FLASK_DIR not in sys.path:
    sys.path.insert(0, PROJETO_FLASK_DIR)

from ProjetoFlask.app import app


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", False),
    )
