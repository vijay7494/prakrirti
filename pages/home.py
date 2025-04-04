import streamlit as st

def show():
    st.title("🔬 Prakriti Identification Platform")
    st.subheader("Unlock the Power of Ayurveda with AI")
    
    st.write(
        "This platform helps Ayurvedic practitioners identify a patient's Prakriti "
        "using facial recognition and AI-based analysis. Easily upload images, assess "
        "Prakriti types, and maintain patient records."
    )
    
    st.image("static/hero_image.jpg", use_column_width=True)
    
    st.markdown("### How It Works:")
    st.markdown("1. Upload a patient’s image.")
    st.markdown("2. Our AI model analyzes facial features.")
    st.markdown("3. Get an instant Prakriti assessment.")
    
    st.markdown("---")
    
    if st.button("🚀 Get Started"):
        st.switch_page("pages/assessment.py")
