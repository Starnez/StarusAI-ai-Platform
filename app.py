import streamlit as st
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env file

# Now you can access the variables using os.getenv
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USERNAME")  # Updated to match .env file
db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def create_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    return connection

def register_user(username, plain_password):
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
    connection.commit()
    cursor.close()
    connection.close()


def authenticate_user(username, plain_password):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    stored_hashed = cursor.fetchone()
    cursor.close()
    connection.close()
    if stored_hashed and bcrypt.checkpw(plain_password.encode('utf-8'), stored_hashed[0].encode('utf-8')):
        return True
    return False

def show_login_form(session_state):
    st.title("Login to Your Account")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if authenticate_user(username, password):
                session_state.is_logged_in = True
                session_state.current_page = "dashboard"
                st.success("Logged in successfully!")
            else:
                st.warning("Incorrect username or password. Please try again.")
                # Refresh the page to allow the user to reenter their information
                st.experimental_rerun()

def show_registration_form():
    st.title("Register a New Account")

    with st.form("registration_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_button = st.form_submit_button("Register")

        if register_button:
            if password == confirm_password:
                register_user(username, password)
                st.success("Account created successfully!")
            else:
                st.warning("Passwords do not match.")

def main():
    # Add background image using HTML and CSS
    st.markdown(
        """
        <style>
        body {
            background-image: url('your_image_url_here');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a session state to store the current page and login status
    session_state = st.session_state

    # Initialize the session state attributes if they don't exist
    if not hasattr(session_state, "current_page"):
        session_state.current_page = "homepage"

    if not hasattr(session_state, "is_logged_in"):
        session_state.is_logged_in = False

    if session_state.is_logged_in:
        create_sidebar(session_state)

    if session_state.current_page == "homepage":
        show_homepage(session_state)
    elif session_state.current_page == "login":
        show_login_form(session_state)
    elif session_state.current_page == "dashboard":
        show_dashboard(session_state)
    elif session_state.current_page == "content_generation":
        show_content_generation()
    elif session_state.current_page == "saved":
        show_saved()

def create_sidebar(session_state):
    # Sidebar for Dashboard

    # Profile picture, name, and company name at the top of the sidebar
    st.sidebar.markdown(
        """
        <style>
        /* Make the profile picture circular */
        .circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            overflow: hidden;
            margin-top: -27%;  /* Adjusted the y-axis */
            float: left;
            margin-right: 10px;
        }
        .circle img {
            width: 100%;
            height: 100%;
        }
        /* Style for name and company */
        .profile-info {
            font-size: 50%;
            margin-left: 22%;
            margin-top: -26%;
            float: left;
        }
        .name {
            clear: left;
            margin-top: -33%;
            font-size: 150%;
        }
        /* Thin line separator */
        .separator {
            border-top: 1px solid gray;
            margin: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Placeholder for profile picture
    st.sidebar.markdown(
        '<div class="circle"><img src="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"></div>',
        unsafe_allow_html=True
    )

    # Name and company name to the right of the picture
    st.sidebar.markdown('<div class="profile-info name">John Doe</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="profile-info">Company, Inc.</div>', unsafe_allow_html=True)

    # Thin line separator
    st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # Display the name of the current page
    st.sidebar.header(session_state.current_page.capitalize())

    if st.sidebar.button("Dashboard"):
        session_state.current_page = "dashboard"

    if st.sidebar.button("Content Generation"):
        session_state.current_page = "content_generation"

    if st.sidebar.button("Saved"):
        session_state.current_page = "saved"

def show_homepage(session_state):
    st.title("Welcome to Starus Content Generator")
    st.subheader("Your Content Creation Platform")

    if st.button("Login"):
        session_state.current_page = "login"

def show_dashboard(session_state):
    # Main content
    st.write("Welcome to the Dashboard!")
    # Add content for the Dashboard page here

def show_content_generation():
    st.write("Content Generation - Coming Soon")

def show_saved():
    st.write("Saved - Coming Soon")


if __name__ == "__main__":
    try:
        connection = create_connection()
        st.write("Connected to the database successfully!")
        connection.close()

        # Register the user after confirming the connection
        register_user("testuser", "testpassword")
        st.write("User registered SO successfully!")
    except Exception as e:
        st.write(f"Error: {e}")