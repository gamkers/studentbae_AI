import jwt  # PyJWT library
from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = 'studentbae@gamkers'  # Use a secure key
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_verification_token(email):
    return serializer.dumps(email, salt='email-confirm')
