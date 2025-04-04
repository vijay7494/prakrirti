import streamlit as st
from PIL import Image
import io
from model.inference import predict_prakriti
from utils import upload_image_to_supabase, init_supabase, create_bucket

def show():
    st.title("📸 Prakriti Identification")

    # Check if user is logged in
    if "user" not in st.session_state:
        st.error("Please log in to access this page.")
        return

    # Get the logged-in doctor's ID
    doctor_id = st.session_state["user"]["id"]

    # Initialize Supabase client
    client = init_supabase()
    if not client:
        st.error("Failed to initialize Supabase! Check connection.")
        return

    # Check if bucket exists, create if it doesn't
    if not create_bucket():
        st.error("Failed to initialize storage bucket! Please check your Supabase permissions.")
        return

    # Form for Patient Details & Image Upload
    with st.form("patient_form"):
        name = st.text_input("Full Name", max_chars=100)
        age = st.number_input("Age", min_value=1, max_value=120)
        contact = st.text_input("Contact Number")
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("Submit & Analyze")

    if submitted:
        if not name or not age or not contact or not uploaded_file:
            st.error("Please fill all fields and upload an image!")
            return

        try:
            # Read the image bytes
            image_bytes = uploaded_file.getvalue()
            file_name = uploaded_file.name
            
            # Display image
            st.image(Image.open(uploaded_file), caption="Uploaded Image", use_column_width=True)

            # Process image for prediction
            with st.spinner("Processing Image..."):
                prakriti_type = predict_prakriti(image_bytes)
                if prakriti_type == "Error" or prakriti_type == "Model unavailable":
                    st.error("Failed to process image. Please try again.")
                    return

            # Upload image to Supabase
            with st.spinner("Uploading image..."):
                # Create a unique filename to avoid conflicts
                unique_filename = f"{name}_{file_name}"
                image_url = upload_image_to_supabase(image_bytes, unique_filename)
                
                if not image_url:
                    st.error("Failed to upload image. Please try again.")
                    return

            # Save patient data
            try:
                data = {
                    "name": name,
                    "age": age,
                    "contact": contact,
                    "prakriti_type": prakriti_type,
                    "image_link": image_url,
                    "assessed_by_id": doctor_id  # Add the doctor's ID
                }
                response = client.from_("patients").insert(data).execute()

                if response.data:
                    st.success(f"Predicted Prakriti Type: {prakriti_type}")
                    st.write("### About This Prakriti Type")
                    st.write("(Detailed explanation of the prakriti type here)")
                else:
                    st.error("Failed to save patient data!")
            except Exception as e:
                st.error(f"Failed to save patient data: {str(e)}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    show()

    # if submitted:
    #     if not name or not age or not contact or not uploaded_file:
    #         st.error("Please fill all fields and upload an image!")
    #         return

    #     try:
    #         # Read the image file and display it
    #         image = Image.open(uploaded_file)
    #         st.image(image, caption="Uploaded Image", use_column_width=True)

    #         with st.spinner("Processing Image..."):
    #             # Predict the Prakriti type
    #             prakriti_type = predict_prakriti(uploaded_file)  # Use the uploaded file's bytes for prediction

    #         # Upload image to Supabase (Bucket: "Images")
    #         image_url = upload_image_to_supabase(uploaded_file)