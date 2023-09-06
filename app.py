import streamlit as st


def main():
    st.title("Starus AI Content Creation Platform")

    # Display background image
    st.image("Background.png",use_column_width=True)

    # Login button
    if st.button("Login"):
        show_login_form()


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