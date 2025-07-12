# Receipt2Sheet

A Python application that extracts information from receipt images and converts it into structured data formats like CSV and XLS.

## Introduction

This application provides a user-friendly interface to upload receipt images, extract relevant information, and generate either a CSV or XLS file. It leverages a generative AI model to accurately extract details such as shop name, item names, quantities, prices, and currency.

## Features

  * **Extracts data from receipt images**: Processes single or multiple receipt images.
  * **Multiple language support**: Can extract information from receipts in various languages, including English, Spanish, French, German, Chinese, Japanese, Korean, Hindi, Urdu, and Arabic.
  * **Multiple output formats**: Generates output in both CSV and XLS formats.
  * **AI-powered data extraction**: Uses the `gemini-1.5-flash` model for accurate and intelligent data extraction.
  * **Data refinement**: Includes a function to refine the extracted data for better accuracy.
  * **User-friendly interface**: Built with Streamlit for a simple and intuitive user experience.

## How to Use

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```
2.  **Create a virtual environment**:
    It is recommended to use a virtual environment with Python 3.10 or higher.
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up API key**:
    Create a file named `keys.env` in the root directory and add your Gemini API key in the following format:
    ```
    Gemini_key=YOUR_API_KEY
    ```
5.  **Run the application**:
    ```bash
    streamlit run Files/app.py
    ```
6.  **Upload receipts**:
      * Open the application in your browser.
      * Select the language of the receipts from the sidebar.
      * Upload one or more receipt images (JPG, PNG, JPEG).
7.  **Generate and download**:
      * Choose the desired output format (CSV or XLS).
      * Click the "Generate" button.
      * Once processed, a "Download" button will appear to save the file.

## Technologies Used

  * **Backend**: Python
  * **Frontend**: Streamlit
  * **AI Model**: Google Generative AI (gemini-1.5-flash)
  * **Data Handling**: Pandas, Openpyxl
  * **Image Processing**: Pillow

## Video Demo

(A video demonstrating the application can be embedded here)
