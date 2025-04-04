import streamlit as st
from supabase import create_client, Client

# Initialize Supabase
SUPABASE_URL = "https://rclmtlicustpbtjxugyo.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJjbG10bGljdXN0cGJ0anh1Z3lvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDExODg2MDUsImV4cCI6MjA1Njc2NDYwNX0.a_W9en6u71CDZrKFz5XimMUjgubRBkPQxgnIOMWt_HM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    # Custom CSS for login form
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
            padding: 0.5rem;
            border-radius: 0.5rem;
            background-color: #1f77b4;
            color: white;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1668a3;
        }
        .stTextInput>div>div>input {
            border-radius: 0.5rem;
            padding: 0.5rem;
        }
        .main .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h1 style='color: #1f77b4;'>Welcome Back</h1>
                <p style='color: #666;'>Please login to your account</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col2:
                signup_button = st.form_submit_button("Sign Up", use_container_width=True)

            if submit:
                try:
                    auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                    if auth_response.user is None or auth_response.session is None:
                        st.error("Invalid credentials. Please try again.")
                        return
                    
                    st.session_state["user"] = {
                        "email": email,
                        "id": auth_response.user.id
                    }
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

            if signup_button:
                st.session_state["page"] = "signup"
                st.rerun()

if __name__ == "__main__":
    login()
