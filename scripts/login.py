import streamlit as st
from deta import Deta
from hashlib import sha256

def register():
    st.title("User Registration")

    with st.form("registration_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        # Validate password
        if st.form_submit_button("Validate"):
            if is_strong_password(password):
                st.success("Password meets the strength criteria.")
            else:
                st.error("Password must contain at least 8 characters, including uppercase, lowercase, and special characters.")

    st.subheader("API Key")
    st.markdown("To complete the registration, please provide your OpenAI API key.")
    st.markdown("You can obtain an API key from OpenAI by following these steps:")
    st.markdown("1. Go to the OpenAI website at [https://openai.com](https://openai.com).")
    st.markdown("2. Sign in to your OpenAI account or create a new account if you don't have one.")
    st.markdown("3. Once signed in, navigate to your account settings or dashboard.")
    st.markdown("4. Look for the API Key section or API Key management.")
    st.markdown("5. Generate a new API key for your application.")
    st.markdown("6. Copy the generated API key.")
    st.markdown("7. Return to this registration page.")

    with st.form("api_key_form"):
        api_key = st.text_input("API Key")

        if st.form_submit_button("Register"):
            if username and password and api_key:
                if is_username_available(username):
                    hashed_password = sha256(password.encode("utf-8")).hexdigest()
                    deta = Deta(st.secrets["data_key"])
                    db = deta.Base("USERS")
                    db.put({"username": username, "password": hashed_password, "api_key": api_key})
                    st.success("Registration Successful. Please log in.")
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.warning("Please provide all required details to complete the registration.")


def is_username_available(username):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("USERS")
    db_content = db.fetch().items

    for item in db_content:
        if item["username"] == username:
            return False

    return True


def is_strong_password(password):
    # Password must contain at least 8 characters, including uppercase, lowercase, and special characters
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\W", password):
        return False

    return True


@st.cache
def login():
    global log
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_info = valid_credentials(username, password)
        if user_info:
            st.success("Login Successful!")
            st.session_state.log = True
            return user_info
        else:
            st.error("Incorrect username or password. Please try again.")


def valid_credentials(username, password):
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("USERS")
    db_content = db.fetch().items

    for item in db_content:
        if item["username"] == username and sha256(password.encode("utf-8")).hexdigest() == item["password"]:
            return item

    return None


if __name__ == "__main__":
    # Replace "your_data_key" with your actual Deta application key
    st.set_secret("data_key", "your_data_key")
    if not st.session_state.get("log"):
        register()
    else:
        user_info = login()
