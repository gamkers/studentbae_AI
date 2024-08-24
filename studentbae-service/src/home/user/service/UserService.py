from src.DB.db_conn import chat_history
import logging
import sys
from src.common.api_response import success_response, unsuccess_response
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
class UserService:
    def add_chat_history(self, user_id, session_id, history ):
        try:
            record = chat_history().fetch({"userid": user_id, "sessionid": int(session_id)}).items
            print(record)
            if record:
                print('in')
                logger.info("session exist appending history")
                record[0]['history'].append(history)
                chat_history().update({"history": record[0]['history']},key=record[0]['key'])

            else:
                logger.info("new session entry")
                chat_history().put({"userid": user_id, "sessionid": int(session_id), "history": [history]})
            return success_response()
        except Exception as e:
            logger.error(f"Exception occur!! {e}", exc_info=True)


    def set_tite(self, user_id, session_id, title):
        try:
            record = chat_history().fetch({"userid": user_id, "sessionid": int(session_id)}).items
            if record:
                record[0]['title'] = title
                chat_history().put(record[0])
                return success_response()
            else:
                return unsuccess_response()
        except Exception as e:
            logger.error(f"Exception occur!! {e}", exc_info=True)

    def get_conversation_session(self, user_id):
        try:
            logger.info("fetching chat history")
            records = chat_history().fetch({"userid":user_id})
            result = [{"sessionid": record.get("sessionid"), "title": record.get("title")}for record in records.items]
            return success_response(result)
        except Exception as e:
            logger.error("error fetching chat history ", exc_info=True)


    def getchat_history(self, user_id, session_id):
        try:
            logger.info("fetching chat history")
            records = chat_history().fetch({"userid":user_id, "sessionid": int(session_id)})

            if records.items:
                result = records.items[0]['history']
            else:
                result = []
            return success_response(result)
        except Exception as e:
            logger.error("error fetching chat history ", exc_info=True)


