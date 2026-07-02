import os
import sys

from controllers.alunos_controller import alunos_bp
from controllers.professores_controller import professores_bp
from controllers.turmas_controller import turmas_bp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import app
from models.BancoSQLite import inicializar_banco
from swagger.swaggerconfig import configure_swagger


inicializar_banco()

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)
configure_swagger(app)


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=app.config.get("DEBUG"),
    )
