import streamlit as st

def main():
    # Add background image using HTML and CSS
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://raw.githubusercontent.com/Starnez/StarusAI-ai-Platform/main/Background.png');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Starus AI Content Creation Platform")

    # Create a session state to store the form visibility and login status
    session_state = st.session_state

    # Initialize the session state attributes if they don't exist
    if not hasattr(session_state, "show_login_form"):
        session_state.show_login_form = False

    if not hasattr(session_state, "is_logged_in"):
        session_state.is_logged_in = False

    # Load CSS styles
    load_styles()

    # "Login" button
    if not session_state.is_logged_in and st.button("Login", key="login_button", help="Click to login"):
        session_state.show_login_form = True

    if session_state.show_login_form:
        show_login_form()
    elif session_state.is_logged_in:
        show_dashboard()

def load_styles():
    # Center-align the button using CSS
    st.write("<style>div.row-widget.stButton > div{display:flex; justify-content:center;}</style>",
             unsafe_allow_html=True)

    # Increase the button's size
    st.write("<style>div.row-widget.stButton > button{width: auto; padding: 10px 30px;}</style>",
             unsafe_allow_html=True)

    # Margin for the button
    st.write("<style>div.row-widget.stButton > button{margin-top: 50px;}</style>", unsafe_allow_html=True)

def show_login_form():
    st.subheader("Login to your account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        # Here, you'll integrate with Planetscale for authentication
        # For now, let's just check if the fields are filled
        if username and password:
            session_state.is_logged_in = True
            st.success("Logged in successfully!")
        else:
            st.warning("Please enter your username and password.")

def show_dashboard():
    st.subheader("Dashboard")

    # Sidebar for Dashboard
    st.sidebar.title("Dashboard")

    # Placeholder for profile picture
    st.sidebar.image("https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png", width=100)

    # Placeholder for name and company
    st.sidebar.write("John Doe")
    st.sidebar.write("Company, Inc.")

    # Dashboard menu
    st.sidebar.write("Dashboard")
    # Add other menu items here

    # Main content
    st.write("Welcome to the Dashboard!")
    # Add content for the Dashboard page here

if __name__ == "__main__":
    main()
