from flask import Flask, request, jsonify
from itsdangerous import URLSafeTimedSerializer
from deta import Deta

app = Flask(__name__)

# Configuration
SECRET_KEY = 'studentbae@gamkers'  # Use a secure key
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Initialize Deta Base
deta = Deta("d0gf5y3r7cm_PsGAAk7Uvp1xp6VBANMCSBnbTLosrxNF")
db = deta.Base("users")

@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Decode the token to get the email
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1 hour expiration

        # Check if the user exists in the database
        user = db.get(email)
        if user:
            # Check if user is already verified
            if user.get('verified') == 'True':
                return jsonify({"error": "Email already verified"}), 400
            
            # Update user record to mark as verified
            db.update({"verified": 'True'}, email)
        else:
            # If the user does not exist
            return jsonify({"error": "Invalid email address"}), 400

        return jsonify({"success": True, "message": "Email verified successfully"})

    except Exception as e:
        # Handle invalid or expired token
        return jsonify({"error": "Invalid or expired token"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
