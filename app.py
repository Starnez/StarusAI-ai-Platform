import streamlit as st

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
            margin-top: -55%;  /* Adjusted the y-axis */
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
            margin-top: 70%
            float: left;
        }
        .name {
            clear: left;
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
    # Here, you'll integrate with Planetscale for authentication
    # For now, let's just check if the fields are filled
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username and password:
        return True
    else:
        st.warning("Please enter your username and password.")
        return False

def show_login_form(session_state):
    st.title("Login to Your Account")

    if session_state.current_page == "login":
        with st.form("login_form"):
            if login_pressed():
                session_state.is_logged_in = True
                session_state.current_page = "dashboard"
            st.form_submit_button("Submit")

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
