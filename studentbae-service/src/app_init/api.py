from flask import Blueprint
from flask_restx import Api
from src.home.user.controller.UserController import user_ns_v2

blueprint_v1 = Blueprint('api_v1', __name__, url_prefix='/gamkers/api')
api_v1 = Api(blueprint_v1, title='STUDENTBAE API V1', description='V1')
api_v1.add_namespace(user_ns_v2)