import os
from flask import Flask


app = Flask(__name__)
#app.config['HOST'] = '127.0.0.1'
#app.config['HOST'] = 'localhost']
app.config['HOST'] ='0.0.0.0'
app.config['PORT'] = int(os.environ.get('PORT', 5000))
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

# URL base para o ambiente local
if app.config['HOST'] == '0.0.0.0':
    BASE_URL = "http://127.0.0.1:" + str(app.config['PORT'])
else:
    BASE_URL = "http://" + app.config['HOST'] + ':' + str(app.config['PORT'])

# Para o Render, use o seguinte URL
BASE_URL = os.environ.get(
    "GESTAO_API_BASE_URL",
    "https://api-de-gerenciamento-escolar.onrender.com"
)
