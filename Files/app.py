import streamlit as st
import pandas as pd
from io import BytesIO
import os
from PIL import Image
from model import extract_info_img
from data_output import json_to_csv, json_to_xls , get_table_download_link
import time
# Upload multiple images

def create_UI():
    st.set_page_config("Receipt2Sheet", initial_sidebar_state="collapsed")
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateX(-20px); }
            100% { opacity: 1; transform: translateX(0); }
        }

        .welcome-message {
            font-size: 48px; /* Adjust font size */
            text-align: center;
            color: white; /* Text color */
            animation: fadeIn 2.0s ease forwards; /* Apply animation */
            margin-top: 50px; /* Space above the message */
        }

        .stTextInput > div > input {
            height: 100%;  /* Adjust height */
            width: 100%;   /* Adjust width */
            font-size: 14px;  /* Adjust font size */
        }

        div[data-testid="column"] {
            width: fit-content !important;
            flex: unset;
            padding-left: 20px;  /* Left padding */
        }

        div[data-testid="column"] * {
            width: fit-content !important;
            vertical-align: left;  /* Align items to the left */
        }

        /* Styling the file uploader to match button styles */
        .stFileUploader {
            width: 100%;  /* Make the file uploader full width */
            border-radius: 5px;  /* Rounded corners */
            text-align: center;  /* Center text */
        }

        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }

        [data-testid='stFileUploader'] section > input + div {
            display: none;  /* Hide the default uploader text */
        }

        /* Animation for sidebar items */
        .sidebar .stSelectbox, 
        .sidebar .stButton, 
        .sidebar .stFileUploader {
            animation: fadeIn 1s ease forwards; /* Apply animation to sidebar elements */
        }

        .sidebar {
            animation: fadeIn 1s ease forwards; /* Apply animation to sidebar itself */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='welcome-message'>Welcome to Receipt2Sheet !</div>", unsafe_allow_html=True)
    main_placeholder = st.empty()
    st.sidebar.title("Upload PDF(s)")
    uploaded_pdfs = st.sidebar.file_uploader("Upload an PDF File(s)", type=["pdf"],
                                                 help="Upload pdf(s) ", label_visibility="hidden", accept_multiple_files=True)

    st.sidebar.title("Upload Image(s)")
    uploaded_files_images = st.sidebar.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], 
                                                        accept_multiple_files=True, label_visibility="hidden")

    col1, col2, col3, col4 ,col5= st.columns([2.5, 2, 2.4, 3.7,3.4], vertical_alignment="bottom", gap="small",) # Adjust column widths to make button smaller

    with col1:
        option = st.selectbox(
            'Output Format', 
            ('CSV', 'XLS'),
            key="output_format"  # Add a key to avoid duplicate IDs
        )

    with col2:
        enter_button = st.button("Generate")  # Remove use_container_width=True

    with col3:
        downlaod_button=st.download_button("Download", "Download")


    if enter_button and uploaded_files_images:
        output_dir = "outputs"  # Specify the desired output directory name
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        json_output=extract_info_img(uploaded_files_images)
        if option == "CSV":
            json_to_csv(json_output, "outputs/output.csv")
            sucess=st.success("CSV File Saved in Output Folder")
            time.sleep(1)
            sucess.empty()  
           
            
        else:
            json_to_xls(json_output, "outputs/output.xlsx")
            sucess=st.success("XLS File Saved in Outputs Folder")
            time.sleep(1)
            sucess.empty()  
            

if __name__ == "__main__":
    create_UI()