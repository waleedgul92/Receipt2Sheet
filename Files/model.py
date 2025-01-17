import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import streamlit as st
import json
import re
import unicodedata
from googletrans  import Translator 
# Load environment variables for API keys


def clean_item_name_general(name):
    """
    Cleans, normalizes, and translates item names for better readability and translation across languages.

    Args:
        name: The raw item name as a string.

    Returns:
        A cleaned, normalized, and translated string.
    """
    # Normalize Unicode (e.g., split combined characters like 'é' into 'e' + accent)
    name = unicodedata.normalize('NFKC', name)

    # Insert space between lowercase and uppercase letters (e.g., "BioGem" → "Bio Gem")
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)

    # Replace common separators with spaces
    name = re.sub(r'[._\-]', ' ', name)

    # Replace non-alphanumeric characters (but preserve accents and non-Latin scripts)
    name = re.sub(r'[^\w\s]', ' ', name)

    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    # Initialize the Google Translator
    translator = Translator()

    # Translate the cleaned text to English
    try:
        translated = translator.translate(name, dest='en')
        return translated.text  # Return the translated text
    except Exception as e:
        print(f"Translation failed: {e}")
        return name  # If translation fails, return the original cleaned name


def simple_translate(text, target_language='en'):
    """
    Simple translation function to clean and normalize text into English.

    Args:
        text (str): The text to translate.
        target_language (str): The target language for translation ('en' for English).
    
    Returns:
        str: Cleaned and normalized text.
    """
    # Clean and normalize the item name using the general function
    return clean_item_name_general(text)

def extract_info_img(img_paths, language):
    load_dotenv("keys.env")
    google_api_key = os.getenv("Gemini_key")
    images_ = []
    for img_path in img_paths:
        img_ = Image.open(img_path)
        images_.append(img_)
    
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"response_mime_type": "application/json"},
    )
    
    prompt = f'''
1) Extract receipt information from the image, which is in  '''+language +'''.
2) Ensure all item names are written in English. If the items' names are not in English, translate them to English or provide their English equivalents.
3) Extract the following information from the image:
   - **Shop or Mart Name**
   - **Item Names**
   - **Quantities** (if unspecified, assume `1`)
   - **Prices**
   - **Currency Type** (infer from context, using the full name instead of symbols)
4) Structure the extracted information into the following JSON format:
   ```json
   {
     "receipts": [
       {
         "shop": "Shop Name",
         "items": [
           {
             "item": "Item Name",
             "quantity": 1,
             "price": 10.99
           }
           // Additional items...
         ],
         "currency": "Currency Name"
       }
       // Additional receipts...
     ]
   }
'''
    input_model = [prompt]
    for img in images_:
        input_model.append(img)

    # Extract the content using the model
    result = model.generate_content(input_model)
    result_text = result.text  # Assuming the result text is in JSON format.

    # Parse the result into a JSON structure
    try:
        extracted_data = json.loads(result_text)
    except json.JSONDecodeError:
        st.error("Failed to decode JSON response.")
        return None

    # Extract and clean item names
    for receipt in extracted_data.get('receipts', []):
        for item in receipt.get('items', []):
            item['item'] = simple_translate(item.get('item', ''))

    # Return the updated JSON structure
    return json.dumps(extracted_data, ensure_ascii=False, indent=4)
