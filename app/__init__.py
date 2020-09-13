from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config

def create_app():
    # A news flask app is created
    # it takes the actual file
    app = Flask(__name__)
    bootstrap =  Bootstrap(app)

    app.config.from_object(Config)

    return app