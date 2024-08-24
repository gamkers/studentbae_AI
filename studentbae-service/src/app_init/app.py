from flask import Flask, request, jsonify, session
from flask_cors import CORS
import secrets
from datetime import timedelta
from flask_session import Session
from src.app_init.api import blueprint_v1
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(blueprint_v1)
if __name__ == '__main__':
    app.run()