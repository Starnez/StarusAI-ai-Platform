from dotenv import load_dotenv
import os
import mysql.connector
import streamlit as st
import bcrypt
import random
import requests
# Load ENV Variables
load_dotenv()


# Retrieve environment variables
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# StackAI Variables
STACK_AI_API_URL = os.getenv('STACK_AI_API_URL')
STACK_AI_AUTH_TOKEN = os.getenv('STACK_AI_AUTH_TOKEN')

headers = {
    'Authorization': STACK_AI_AUTH_TOKEN,
    'Content-Type': 'application/json'
}

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            autocommit=True,
            ssl_ca="C:\Program Files\Git\mingw64\etc\ssl\cert.pem",  # Specify the correct path to your SSL certificate
            ssl_verify_identity=True  # Enable SSL certificate verification
        )
        print("Connected to the database successfully!")  # Debugging statement
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        print(f"Error connecting to the database: {err}")  # Debugging statement
        return None
def verify_credentials(username, password):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password, role FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        hashed_password = result['password'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return result['role']  # Return the role of the user
    return None

def show_login_form(session_state):
    st.title("Login to Your Account")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Submit"):
            user_role = verify_credentials(username, password)
            if user_role:
                session_state.is_logged_in = True
                session_state.user_role = user_role
                session_state.current_page = "dashboard"
                st.experimental_rerun()  # Refresh the page to reflect the changes
            else:
                st.warning("Incorrect username or password, please try again.")

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
    if not hasattr(session_state, "is_logged_in"):
        session_state.is_logged_in = False

    if not hasattr(session_state, "user_role"):
        session_state.user_role = ""

    if not hasattr(session_state, "current_page"):
        session_state.current_page = "homepage"

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
    elif session_state.current_page == "admin_console":
        show_admin_console()

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

    if session_state.user_role == "admin":
        if st.sidebar.button("Admin Console"):
            session_state.current_page = "admin_console"

def generate_id(company_name):
    # Define a mapping of company names to their prefixes
    company_prefixes = {
        "Google": "12345",
        # Add other companies and their prefixes here
    }
    company_prefix = company_prefixes.get(company_name, "00000")  # Default to "00000" if company not found
    employee_number = random.randint(000, 999)
    return int(f"{company_prefix}{employee_number}")
def show_admin_console():
    st.title("Admin Console")

    # Add User Section
    st.subheader("Add User")

    with st.form("add_user_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "user"])  # You can add more roles if needed
        name = st.text_input("Name")
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        ID = st.text_input("ID")  # Assuming ID is a string. If it's a number, use st.number_input

        if st.form_submit_button("Submit"):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            add_user_to_db(ID, name, username, company_name, email, hashed_password, role)

def add_user_to_db(ID, name, username, company_name, email, hashed_password, role):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (ID, name, username, company_name, email, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (ID, name, username, company_name, email, hashed_password, role)
        )
        st.success("User added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error adding user to the database: {err}")
    finally:
        cursor.close()
        conn.close()

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



def show_dashboard(session_state):
    # Main content
    st.write("Welcome to the Dashboard!")
    # Add content for the Dashboard page here

def show_content_generation():
    st.title("GENERATE CONTENT")

    # Initialize session state variable for content generation
    if not hasattr(st.session_state, "content_generated"):
        st.session_state.content_generated = False

    # Create a form for content ideas
    with st.form(key="content_form"):
        user_input = st.text_area("Enter your content ideas or what you're thinking:")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Make an API call to Stack AI with user_input
            generated_content = call_stack_ai(user_input)

            # Display the generated content
            st.subheader("Generated Content:")
            st.write(generated_content)

            # Update session state variable
            st.session_state.content_generated = True

    # Display the Start Again Button only if content has been generated
    if st.session_state.content_generated:
        if st.button("Start Again"):
            # Reset the content_generated session state variable
            st.session_state.content_generated = False
            # Clear the text area and start over
            st.experimental_rerun()

def call_stack_ai(user_input):
    payload = {"in-0": user_input}
    response = requests.post(STACK_AI_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        json_response = response.json()
        return json_response.get("out-0", "Error generating content.")  # Extract content using "out-0" key
    else:
        return f"Error: {response.status_code} - {response.text}"

def show_saved():
    st.write("Saved - Coming REAL Soon")

if __name__ == "__main__":
    main()
