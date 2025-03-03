from flask import Flask
from flask_app.routes import api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/')
    app.secret_key = "super_secreta"
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
