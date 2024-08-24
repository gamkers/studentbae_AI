from flask import jsonify, request
import logging
from flask_restx import Namespace, Resource, Api
import sys
from src.home.user.service.UserService import UserService
from ..DTO.DTO import UserHistory
from ..DTO.InputModel import UserInputModel
api = Api()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

user_ns_v2 = Namespace('user', description='user Service V1 API', path='/user')

user_ns_v2.add_model('ChatHistory', UserInputModel.chat_history(self=None))
user_ns_v2.add_model('History', UserInputModel.chat_history(self=None))
user_input_model = UserInputModel()
chat_history_model = user_input_model.chat_history()
@user_ns_v2.route("/conversations/<string:user>")
class GetConversations(Resource):
    def get(self,user):
        logger.info('GET /user/conversations/')
        try:
            result = UserService.get_conversation_session(self=0, user_id=user)
            return jsonify(result)
        except Exception as e:
            print(e)

@user_ns_v2.route("/conversations/chats")
class GetConversations(Resource):
    @user_ns_v2.doc(
        description='Get user conversations',
        params={
            'X-User-Id': {'in': 'header', 'description': 'User ID', 'required': True},
            'X-Session-Id': {'in': 'header', 'description': 'Session ID', 'required': True, 'type': 'integer'}
        }
    )
    def get(self):
        logger.info('GET /user/conversations/')
        try:
            user_id = request.headers.get("X-User-Id")
            session_id = request.headers.get("X-Session-Id")
            result = UserService.getchat_history(self=0, user_id=user_id, session_id=session_id)
            return jsonify(result)
        except Exception as e:
            print(e)


@user_ns_v2.route("/setHistory")
@user_ns_v2.expect(UserInputModel.chat_history(self=None), validate=False)
class GetConversations(Resource):
    @user_ns_v2.doc(
        description='Get user conversations',
        params={
            'X-User-Id': {'in': 'header', 'description': 'User ID', 'required': True},
            'X-Session-Id': {'in': 'header', 'description': 'Session ID', 'required': True, 'type': 'integer'}
        }
    )
    def post(self):
        logger.info('GET /user/setHistory/')
        inputs = UserHistory().load(request.json)
        user_id = request.headers.get("X-User-Id")
        session_id = request.headers.get("X-Session-Id")
        try:
            result = UserService.add_chat_history(self=0, user_id=user_id, session_id=session_id, history=inputs['history'])
            return jsonify(result)
        except Exception as e:
            print(e)


@user_ns_v2.route("/setTitle")
@user_ns_v2.expect(UserInputModel.chat_history(self=None), validate=False)
class GetConversations(Resource):
    @user_ns_v2.doc(
        description='Get user conversations',
        params={
            'X-User-Id': {'in': 'header', 'description': 'User ID', 'required': True},
            'X-Session-Id': {'in': 'header', 'description': 'Session ID', 'required': True, 'type': 'integer'}
        }
    )
    def post(self):
        logger.info('GET /user/setTitle/')
        inputs = UserHistory().load(request.json)
        user_id = request.headers.get("X-User-Id")
        session_id = request.headers.get("X-Session-Id")
        try:
            result = UserService.set_tite(self=0, user_id=user_id, session_id=session_id, title=inputs['title'])
            return jsonify(result)
        except Exception as e:
            print(e)