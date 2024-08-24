from marshmallow import Schema, validate, fields

class HisSchema(Schema):
    AI = fields.Str(required=True)
    human = fields.Str(required=True)

# Define the user history schema
class UserHistory(Schema):
    title = fields.Str()
    history = fields.Raw()
