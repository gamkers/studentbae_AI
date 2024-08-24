from flask_restx import Api, fields
api = Api()

class UserInputModel:

    def chat_history(self):
        # Define the nested history model


        # Define the overall chat history model
        chat_history_model = api.model("ChatHistory", {
            "title": fields.String(),
            "history": fields.Raw()
        })

        return chat_history_model


