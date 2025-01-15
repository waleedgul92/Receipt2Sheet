import os
from dotenv import load_dotenv
import google.generativeai as genai
import base64
import httpx
from PIL import Image
import streamlit as st

# import PyPDF2
def extract_info_img(img_paths):
    load_dotenv("keys.env")
    google_api_key = os.getenv("Gemini_key")
    images_=[]
    for img_path in img_paths:
        img_=Image.open(img_path)
        images_.append(img_)
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                   generation_config={"response_mime_type": "application/json"},
                                   )  
    prompt = '''extract information from the image like things you bought, quantity, mart or shop name, price of that thing,
  DO NOT INCLUDE IRRELVENT INFO LIKE address, website name 
  IF quantity is not mentioned it is one (1) AND USE NAMES OF CURRENCY NOT SYMBOLS,and translate extracted info to english language if not in english language
  and return in JSON FORMAT. Sample json format is as follows:
  "receipts": [
    {
      "shop": str,
      "items": [
        {
          "item": str,
          "quantity": int,
          "price": float
        },
        # ... (other items)
      ],
      "currency": str,
    },  ... other receipts
  ]
  return json object'''
    input_model=[prompt]
    for img in images_:
        input_model.append(img)
    response = model.generate_content(input_model)
    return response.text