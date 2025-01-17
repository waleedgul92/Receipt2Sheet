import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import streamlit as st
import json

# Load environment variables for API keys
load_dotenv("keys.env")
google_api_key = os.getenv("Gemini_key")

def simple_translate(text, target_language='en'):
    """
    Simple translation function to translate text into English while handling dots in item names.

    Args:
        text (str): The text to translate.
        target_language (str): The target language for translation ('en' for English).
    
    Returns:
        str: Translated text, with dots preserved in names.
    """
    # Split the text into words and preserve any dots
    words = text.split(" ")
    
    translated_words = []
    for word in words:
        # If the word contains a dot, treat it as a product name or abbreviation and leave it unchanged
        if "." in word:
            translated_words.append(word)
        else:
            # In a full translation system, this would be the place to translate using an API
            translated_words.append(word)  # Placeholder for actual translation logic

    return " ".join(translated_words)

def extract_info_img(img_paths, language):
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
1) Extract receipt information from the image, which is in  ''' +language + ''' .
2) Ensure all item names are written in English. If the items' names are not in English, translate them to English or provide their English equivalents.
3) Extract the following information from the image:
   - **Shop or Mart Name**
   - **Item Names**
   - **Quantities** (if unspecified, assume `1`)
   - **Prices**
   - **Currency Type** (infer from context, using the full name instead of symbols)
   - Any **Schemes** (e.g., "pfab" or similar) along with their associated details.
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

    # Extract item names and translate if needed
    item_names = []
    for receipt in extracted_data.get('receipts', []):
        for item in receipt.get('items', []):
            item_names.append(item.get('item', ''))

    # Translate the item names into English using the simple translation function
    translated_item_names = [simple_translate(item_name) for item_name in item_names]

    # Update item names in the JSON structure with the translated names
    item_index = 0
    for receipt in extracted_data.get('receipts', []):
        for item in receipt.get('items', []):
            item['item'] = translated_item_names[item_index]
            item_index += 1

    # Return the updated JSON structure
    return json.dumps(extracted_data, ensure_ascii=False, indent=4)
