from deta import Deta
from src.common import  constants
deta = Deta(constants.DB_API_KEY)

def chat_history():
    return deta.Base("USER_HISTORY")


