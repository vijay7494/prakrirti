import streamlit as st
from utils import init_supabase
from PIL import Image
import requests
from io import BytesIO

def show():
    st.title("📜 Assessment History")
    st.write("View past assessments conducted on patients.")

    # Initialize Supabase client
    client = init_supabase()

    # Ensure user is logged in
    if "user" not in st.session_state:
        st.error("Please log in to view history.")
        return

    # Get the logged-in practitioner's ID
    practitioner_id = st.session_state["user"]["id"]

    # Fetch patients assessed by this practitioner
    response = client.table("patients") \
                     .select("*") \
                     .eq("assessed_by_id", practitioner_id) \
                     .order("created_at", desc=True) \
                     .execute()

    if response.data:
        for record in response.data:
            with st.expander(f"{record['name']} - {record['prakriti_type']}"):
                # Create columns for better layout
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display patient image if available
                    if record.get('image_link'):
                        try:
                            # Fetch image from URL
                            img_response = requests.get(record['image_link'])
                            img = Image.open(BytesIO(img_response.content))
                            st.image(img, caption="Patient Image", use_container_width=True)
                        except Exception as e:
                            st.error(f"Failed to load image: {str(e)}")
                
                with col2:
                    # Display patient details
                    st.write("### Patient Details")
                    st.write(f"**Name:** {record['name']}")
                    st.write(f"**Age:** {record['age']}")
                    st.write(f"**Contact:** {record['contact']}")
                    st.write(f"**Prakriti Type:** {record['prakriti_type']}")
                    st.write(f"**Assessment Date:** {record['created_at'][:10]}")
                    
                    # Add a delete button with confirmation
                    if st.button("Delete Record", key=f"delete_{record['id']}"):
                        if st.warning("Are you sure you want to delete this record? This action cannot be undone."):
                            try:
                                delete_response = client.table("patients").delete().eq("id", record['id']).execute()
                                if delete_response.data:
                                    st.success("Record deleted successfully!")
                                    st.rerun()  # Refresh the page
                                else:
                                    st.error("Failed to delete record.")
                            except Exception as e:
                                st.error(f"Error deleting record: {str(e)}")
    else:
        st.info("No past assessments found.")

if __name__ == "__main__":
    show()



# import streamlit as st
# import supabase

# def show():
#     st.title("📜 Assessment History")
#     st.write("View past assessments conducted on patients.")
    
#     # Placeholder: Replace with actual Supabase retrieval
#     assessments = [
#         {"name": "John Doe", "prakriti": "Vata", "date": "2025-03-01"},
#         {"name": "Jane Smith", "prakriti": "Pitta", "date": "2025-03-02"}
#     ]
    
#     if not assessments:
#         st.info("No past assessments found.")
#     else:
#         for record in assessments:
#             with st.expander(f"{record['name']} - {record['prakriti']}"):
#                 st.write(f"**Date:** {record['date']}")
#                 st.write(f"**Prakriti Type:** {record['prakriti']}")
#                 st.button("View Details", key=record['name'])
