import streamlit as st
from utils import init_supabase, upload_image_to_supabase
from PIL import Image
import io

def show():
    # Minimal and Clean UI Design
    st.markdown("""
        <style>
        .profile-card {
            background-color: #f9f9f9;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .profile-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .profile-header h1 {
            color: #333;
            font-size: 24px;
            margin-bottom: 0.5rem;
        }
        .profile-header p {
            color: #666;
            font-size: 16px;
        }
        .profile-image {
            display: flex;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        .profile-image img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #ddd;
        }
        .info-section {
            margin-bottom: 1.5rem;
        }
        .info-section h3 {
            color: #333;
            font-size: 18px;
            margin-bottom: 1rem;
        }
        .info-item {
            margin-bottom: 0.8rem;
            font-size: 16px;
            color: #555;
        }
        .edit-form button {
            background-color: #007bff;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .edit-form button:hover {
            background-color: #0056b3;
        }
        </style>
    """, unsafe_allow_html=True)

    # Profile Header
    st.markdown("""
        <div class="profile-header">
            <h1>👤 Practitioner Profile</h1>
            <p>View and manage your profile details</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Supabase client
    client = init_supabase()

    # Ensure user is logged in
    if "user" not in st.session_state:
        st.error("Please log in to view profile.")
        return

    # Get the logged-in practitioner's ID
    practitioner_id = st.session_state["user"]["id"]

    # Fetch profile details from Supabase
    response = client.table("practitioners") \
                    .select("name, email, contact, number_of_patients_assessed, profile_picture") \
                    .eq("unique_id", practitioner_id) \
                    .single() \
                    .execute()

    if response.data:
        profile_data = response.data
    else:
        st.error("Error fetching profile details.")
        return

    # Default profile picture if not set
    profile_picture = profile_data.get("profile_picture") or "static/default_profile.png"

    # Create two tabs: View Profile and Edit Profile
    tab1, tab2 = st.tabs(["View Profile", "Edit Profile"])

    with tab1:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="profile-image"><img src="{profile_picture}" alt="Profile Picture"></div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="info-section">
                <h3>📋 Personal Information</h3>
                <div class="info-item"><strong>Name:</strong> {profile_data['name']}</div>
                <div class="info-item"><strong>Email:</strong> {profile_data['email']}</div>
                <div class="info-item"><strong>Contact:</strong> {profile_data['contact']}</div>
                <div class="info-item"><strong>Patients Assessed:</strong> {profile_data['number_of_patients_assessed']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        with st.form("edit_profile_form", clear_on_submit=False):
            st.markdown('<div class="info-section"><h3>🖼️ Profile Picture</h3>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload new profile picture", type=["jpg", "png", "jpeg"])

            st.markdown('<div class="info-section"><h3>📝 Personal Information</h3>', unsafe_allow_html=True)
            name = st.text_input("Name", value=profile_data['name'])
            contact = st.text_input("Contact", value=profile_data['contact'])

            submit = st.form_submit_button("💾 Save Changes")

            if submit:
                try:
                    if uploaded_file:
                        image_bytes = uploaded_file.getvalue()
                        image_url = upload_image_to_supabase(image_bytes, f"profile_{practitioner_id}_{uploaded_file.name}")
                        if image_url:
                            profile_data['profile_picture'] = image_url

                    update_data = {
                        "name": name,
                        "contact": contact,
                        "profile_picture": profile_data.get('profile_picture')
                    }

                    update_response = client.table("practitioners") \
                                            .update(update_data) \
                                            .eq("unique_id", practitioner_id) \
                                            .execute()

                    if update_response.data:
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update profile.")

                except Exception as e:
                    st.error(f"❌ Error updating profile: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show()