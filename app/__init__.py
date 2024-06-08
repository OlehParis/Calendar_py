from flask import Flask
from .routes import bp
import os

def create_app():
    app = Flask(__name__)
    app.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')})
    app.register_blueprint(bp)
    
    return app
