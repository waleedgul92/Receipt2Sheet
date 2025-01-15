import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Function to convert a dataframe to CSV or Excel
def convert_to_file(df, file_format):
    if file_format == "CSV":
        return df.to_csv(index=False).encode('utf-8')
    elif file_format == "XLS":
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        return output.getvalue()

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
            height: 100%;  /* Adjust height */
            width: 100%;   /* Adjust width */
            font-size: 14px;  /* Adjust font size */
        }

        div[data-testid="column"] {
            width: fit-content !important;
            flex: unset;
            padding-left: 20px;  /* Left padding */
        }

        div[data-testid="column"] * {
            width: fit-content !important;
            vertical-align: left;  /* Align items to the left */
        }

        /* Styling the file uploader to match button styles */
        .stFileUploader {
            width: 100%;  /* Make the file uploader full width */
            border-radius: 5px;  /* Rounded corners */
            text-align: center;  /* Center text */
        }

        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }

        [data-testid='stFileUploader'] section > input + div {
            display: none;  /* Hide the default uploader text */
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
    st.sidebar.title("Upload  PDF(s)")
    uploaded_pdfs = st.sidebar.file_uploader("Upload an PDF File(s)", type=["pdf"],
                                                    help="Upload pdf(s) ", label_visibility="hidden",accept_multiple_files=True)

    st.sidebar.title("Upload Image(s)")
    uploaded_files_images = st.sidebar.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True,label_visibility="hidden")


    option = st.selectbox(
            'Ouput Format', 
                 ('CSV', 'XLS'))
    enter_button=st.button("Generate")
if __name__ == "__main__":
    create_UI()