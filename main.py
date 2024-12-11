import streamlit as st
import pandas as pd
from PIL import Image
import json
from datetime import datetime
from google.oauth2 import service_account

# Import utility functions
from utils import update_produce_data
from generate_pdf import generate_pdf_report

# Set page config
st.set_page_config(page_title="Fresh Produce Analyzer", layout="wide")

hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {display: none !important;}
        header {visibility: hidden;}
        .viewerBadge_container__1QSob {display: none !important;}
        .css-1lsmgbg.egzxvld1 {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session states
if 'produce_data' not in st.session_state:
    st.session_state.produce_data = []

try:
    # Initialize Google Cloud credentials
    credentials_info = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    project_id = st.secrets["GOOGLE_CLOUD_PROJECT"]

    # Initialize Vertex AI
    import vertexai
    vertexai.init(project=project_id, location="us-central1", credentials=credentials)

    # Initialize the model from Vertex AI
    from vertexai.generative_models import GenerativeModel
  
    st.session_state.model = GenerativeModel(st.secrets["GCP_MODEL_CRED"])
    st.success("Model loaded successfully")

except Exception as e:
    st.error(f"Error loading Google Cloud credentials")
    st.stop()

# Import after model is set
from analysis import analyze_image

def main():
    st.title("Fresh Produce Analyzer")
    
    # Image input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_type = st.radio("Choose input method:", ["Upload Image", "Camera Input"])
        
        if input_type == "Upload Image":
            uploaded_file = st.file_uploader("Choose an image of produce", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
        else:
            img_file = st.camera_input("Take a picture of produce")
            if img_file is not None:
                image = Image.open(img_file)
                
        if 'image' in locals():
            # Resize image for display
            max_width = 300
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            resized_image = image.resize(new_size)
            st.image(resized_image, caption="Input Image")
            
            if st.button("Analyze Produce"):
                with st.spinner("Analyzing image..."):
                    analysis = analyze_image(image)
                    if analysis:
                        update_produce_data(analysis)
                        
                        st.subheader("Analysis Results:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"*Produce:* {analysis['Produce']}")
                            st.write(f"*Freshness Score:* {analysis['Freshness']}/10")
                        with col2:
                            st.write(f"*Expected Shelf Life:* {analysis['Expected Lifespan (Days)']} days")
                            if analysis['Visual Indicators']:
                                st.write("*Visual Indicators:*")
                                for indicator in analysis['Visual Indicators']:
                                    st.write(f"- {indicator}")
    
    # Display produce history
    st.subheader("Produce Analysis History")
    if st.session_state.produce_data:
        df = pd.DataFrame(st.session_state.produce_data)
        st.dataframe(df, use_container_width=True)
        
        # Report generation section
        st.subheader("Generate Report")
        if st.button("Generate PDF Report"):
            pdf_filename = f"produce_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            if generate_pdf_report(st.session_state.produce_data, pdf_filename):
                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("PDF report generated successfully!")
    else:
        st.info("No produce analyzed yet.")

if __name__ == "__main__":
    main()
