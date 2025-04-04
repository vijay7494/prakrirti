import streamlit as st
from pages import home, assessment, history, profile, settings
from auth import login, signup
from components.navbar import render_navbar

def main():
    st.set_page_config(page_title="Prakriti Identification", layout="wide")

    # Initialize session state
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    # Authentication logic
    if st.session_state["user"] is None:
        if st.session_state["page"] == "login":
            login.login()
        else:
            signup.signup()
        return

    # Render navbar and get current page
    page = render_navbar()

    # Page rendering
    if page == "Home":
        home.show()
    elif page == "Assessment":
        assessment.show()
    elif page == "History":
        history.show()
    elif page == "Profile":
        profile.show()
    elif page == "Settings":
        settings.show()
    elif page == "Logout":
        st.session_state["user"] = None
        st.session_state["page"] = "login"
        st.rerun()

if __name__ == "__main__":
    main()