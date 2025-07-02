# src/main.py

from flask import Flask
from web.controllers import api_bp # Importa o Blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api') # Registra o Blueprint com um prefixo /api
    return app

if __name__ == '__main__':
    app = create_app()
    # Para rodar em desenvolvimento, use o modo debug.
    # Em produção, você usaria um servidor WSGI como Gunicorn ou uWSGI.
    app.run(debug=True, host='0.0.0.0', port=5000)