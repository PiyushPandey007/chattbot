import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
# Set your Gemini API key (replace with your actual key)
genai.configure(api_key="GEMINI_API_KEY")

def get_image_and_text_response(image_bytes=None, text_prompt=None):
    model = genai.GenerativeModel("gemini-2.5-flash")

    parts = []
    if image_bytes:
        parts.append({
            "mime_type": "image/png",  # match file type
            "data": image_bytes
        })
    if text_prompt:
        parts.append({"text": text_prompt})

    contents = [{"role": "user", "parts": parts}]

    response = model.generate_content(contents=contents)
    return response.text



st.set_page_config(page_title="        सेवक AI 🩺", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .big-font {
            font-size: 42px !important;
            color: #FFFFFF;
            font-weight: bold;
            text-align: center;           /* Center align text */
            width: 100%;                 /* Make sure full container width */
            margin-bottom: 0.5rem;       /* Optional spacing */
        }
        .header-text {
            text-align: center;
            color: #FFFFFF;
            margin-top: 0;
            font-size: 20px;
            font-weight: 500;
        }
        .chatbot-bubble {
            background-color: #000000;
            border: 1.5px solid #007965;
            border-radius: 10px;
            padding: 16px;
            margin: 12px 0;
            font-size: 18px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Centered title
st.markdown('<p class="big-font">👨🏼‍⚕️सेवक AI 🩺</p>', unsafe_allow_html=True)

# Centered header below title
st.markdown('<p class="header-text">Upload a health-related image and/or type your question to get AI-powered insights.</p>', unsafe_allow_html=True)




uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
user_text = st.text_input("Or type your health question:")

image_bytes = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to bytes for API
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    image_bytes = img_byte_arr.getvalue()

if uploaded_file or user_text:
    with st.spinner("Analyzing..."):
        answer = get_image_and_text_response(image_bytes=image_bytes, text_prompt=user_text)
    st.markdown(f'<div class="chatbot-bubble"><b>Chatbot:</b> {answer}</div>', unsafe_allow_html=True)



