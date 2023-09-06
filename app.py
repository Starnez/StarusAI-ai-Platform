import streamlit as st

def main():
    st.title("Starus AI Content Creation Platform")

    # Create a session state to store the form visibility
    session_state = st.session_state

    if not session_state.get("show_login_form"):
        session_state.show_login_form = False

    # Login button
    if st.button("Login"):
        session_state.show_login_form = True

    if session_state.show_login_form:
        show_login_form()

    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("C:\\Users\\Stokley\\StarusAI-ai-Platform\\Background.png"
);
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_login_form():
    st.subheader("Login to your account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        # Here, you'll integrate with Planetscale for authentication
        # For now, let's just check if the fields are filled
        if username and password:
            st.success("Logged in successfully!")
        else:
            st.warning("Please enter your username and password.")

if __name__ == "__main__":
    main()
