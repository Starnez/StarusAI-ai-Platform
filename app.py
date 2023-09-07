import os
import mysql.connector
import streamlit as st
import bcrypt

# Retrieve environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Function to connect to the database
def connect_to_db():
    connection = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return connection

def verify_credentials(username, password):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        hashed_password = result['password'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False
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

def login_pressed():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username and password:
        if verify_credentials(username, password):
            return True
        else:
            st.warning("Invalid username or password.")
            return False
    else:
        st.warning("Please enter your username and password.")
        return False


def show_login_form(session_state):
    st.title("Login to Your Account")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Submit"):
            if verify_credentials(username, password):
                session_state.is_logged_in = True
                session_state.current_page = "dashboard"
            else:
                st.warning("Incorrect username or password, please try again.")
                st.experimental_rerun()  # Refresh the page

def show_dashboard(session_state):
    # Main content
    st.write("Welcome to the Dashboard!")
    # Add content for the Dashboard page here

def show_content_generation():
    st.write("Content Generation - Coming Soon")

def show_saved():
    st.write("Saved - Coming Soon")

if __name__ == "__main__":
    main()
