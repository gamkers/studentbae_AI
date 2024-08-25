from flask import Flask, request, jsonify, session
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import secrets
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from deta import Deta


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Necessary for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
# Initialize CORS
CORS(app, supports_credentials=True)

# Initialize Deta Base
deta = Deta("d0gf5y3r7cm_PsGAAk7Uvp1xp6VBANMCSBnbTLosrxNF")
db = deta.Base("users")

import random

def generate_random_session_id(start=1, end=9999):
    return random.randint(start, end)




def get_model():
    """Lazy initialization of the ChatGroq model."""
    llm = ChatGroq(
            model="mixtral-8x7b-32768",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            groq_api_key="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"
        )

    return llm

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user already exists
    existing_user = db.get(email)
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Store user in the database
    db.put({"key": email, "password": hashed_password,"verified":'Flase'})
    return jsonify({"success": True, "message": "verification Mail sent to your mail id. Please verify "})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    verified = user.get('verified')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Fetch user from the database
    user = db.get(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid email or password"}), 400
    
    if verified == 'False':
        return jsonify({"error": "Please Verify your mail id"}), 400

    # Set session
    if 'user' not in session:
            session['user'] = []

        # Append the new message to the history
    session['user'].append("True")
    
    return jsonify({"success": True, "message": "Login successful"})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route('/check_auth', methods=['GET'])
def check_auth():
    if 'user' in session and session['user']:
        return jsonify({"authenticated": True, "user": session['user']}), 200
    return jsonify({"authenticated": False}), 401

import requests

@app.route('/chat', methods=['POST'])
def chat():
    # if 'True' not in session['user']:
    #     return jsonify({"error": "Unauthorized"}), 401

    if 'session_id' not in session:
        session['session_id'] = generate_random_session_id()

    try:
        input_message = request.json.get('message')
        if not input_message:
            return jsonify({"error": "No message provided"}), 400

        # Initialize or retrieve conversation history
        if 'history' not in session:
            session['history'] = []
    
        # Append the new message to the history
        session['history'].append(("human", input_message))

        if len(session['history']) > 4:
            session['history'] = session['history'][-4:]

        # Create the prompt template with dynamic variables
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful teacher for your students. You will explain the questions whatever students ask. You will also remember the {previous_context}, but you don't need to mention the history every time."),
                ("human", "{input_message}"),
            ]
        )

        llm = get_model()
        # Combine prompt and model
        chain = prompt | llm

        # Invoke the chain with the input message and history
        result = chain.invoke({"input_message": input_message, "previous_context": session['history']})
        result_content = result.content

        # Append the model's response to the history
        session['history'].append(("ai", result_content))

        if len(session['history']) > 4:
            session['history'] = session['history'][-4:]

        # Log the result for debugging
        print(result_content)

        # Send the history to the API
        history_payload = {
            "title": input_message,  # You can dynamically set this title
            "history": {"AI": result_content, "human": input_message} 
        }

        headers = {
            "accept": "application/json",
            "X-User-Id": "1",  # Replace with actual user ID
            "X-Session-Id": str(session['session_id']),
            "Content-Type": "application/json"
        }

        response = requests.post(
            'http://127.0.0.1:5000/gamkers/api/user/setHistory',
            json=history_payload,
            headers=headers
        )
        
        # Handle the API response
        if response.status_code == 200:
            print("History sent successfully!")
        else:
            print(f"Failed to send history. Status code: {response.status_code}, Response: {response.text}")

        if len(session['history']) == 2:
            # Set the title using the first question asked by the user
            title_payload = {
                "title": input_message,
                "history": {}
            }

            headers = {
                "accept": "application/json",
                "X-User-Id": "1",  # Replace with actual user ID
                "X-Session-Id": str(session['session_id']),
                "Content-Type": "application/json"
            }
            Title_response = requests.post(
                    'http://127.0.0.1:5000/gamkers/api/user/setTitle',
                    json=title_payload,
                    headers=headers
                )

                # Handle the API response
            if Title_response.status_code == 200:
                print("Title set successfully!")
            else:
                print(f"Failed to set title. Status code: {response.status_code}, Response: {response.text}")

        # Return the result as JSON response
        return jsonify({"reply": result_content})

    except Exception as e:
        # Handle any errors that occur
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True,port=5001)
