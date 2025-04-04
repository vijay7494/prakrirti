import streamlit as st
import supabase

def show():
    st.title("👤 Practitioner Profile")
    st.write("View and manage your profile details.")
    
    # Placeholder: Replace with actual Supabase retrieval
    profile_data = {
        "name": "Dr. Ayurvedic", 
        "email": "doctor@ayurveda.com", 
        "contact": "+91 9876543210",
        "patients_assessed": 25,
        "profile_picture": "static/default_profile.png"
    }
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(profile_data["profile_picture"], width=150)
    
    with col2:
        st.write(f"**Name:** {profile_data['name']}")
        st.write(f"**Email:** {profile_data['email']}")
        st.write(f"**Contact:** {profile_data['contact']}")
        st.write(f"**Patients Assessed:** {profile_data['patients_assessed']}")
    
    st.button("Edit Profile")
