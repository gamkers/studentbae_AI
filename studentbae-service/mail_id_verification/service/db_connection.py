from deta import Deta
deta = Deta('d0gf5y3r7cm_PsGAAk7Uvp1xp6VBANMCSBnbTLosrxNF')

def chat_history():
    return deta.Base("USER_HISTORY")