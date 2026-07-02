import os
from flask import Flask, jsonify

API_TARGET = os.environ.get("API_TARGET", os.environ.get("APP_ENV", "render")).lower()
USE_LOCAL_APIS = API_TARGET in ("local", "localhost", "dev", "development")

API_BASE_URLS = {
    "render": {
        "GESTAO": "https://api-de-gerenciamento-escolar.onrender.com",
        "RESERVA": "https://api-de-reserva-de-salas.onrender.com",
        "ATIVIDADE": "https://atividade-microservice-api-escolar.onrender.com",
    },
    "local": {
        "GESTAO": "http://127.0.0.1:5000",
        "RESERVA": "http://127.0.0.1:5001",
        "ATIVIDADE": "http://127.0.0.1:5002",
    },
}


def get_api_base_url(service_name):
    env_name = f"{service_name}_API_BASE_URL"
    default_target = "local" if USE_LOCAL_APIS else "render"
    return os.environ.get(env_name, API_BASE_URLS[default_target][service_name]).rstrip("/")


banco_de_dados = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco_de_dados.db"),
)


app = Flask(__name__)
#app.config['HOST'] = '127.0.0.1'
#app.config['HOST'] = 'localhost']
app.config['HOST'] ='0.0.0.0'
app.config['PORT'] = int(os.environ.get('PORT', 5000))
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = os.environ.get(
        "CORS_ALLOW_ORIGIN",
        "*",
    )
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "gestao",
        "api_target": API_TARGET,
        "dependencies": {
            "reserva": RESERVA_API_BASE_URL,
            "atividade": ATIVIDADE_API_BASE_URL,
        },
    })

GESTAO_API_BASE_URL = get_api_base_url("GESTAO")
RESERVA_API_BASE_URL = get_api_base_url("RESERVA")
ATIVIDADE_API_BASE_URL = get_api_base_url("ATIVIDADE")
BASE_URL = GESTAO_API_BASE_URL
