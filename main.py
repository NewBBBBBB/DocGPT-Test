import streamlit as st
from openai import OpenAI
import requests
import PIL.Image
import base64
from io import BytesIO

# Function to fetch and encode image from URL
def fetch_and_encode_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_bytes = response.content
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            return encoded_image
        else:
            st.error("Failed to fetch the image from the URL.")
            return None
    except Exception as e:
        st.error(f"Error fetching image from URL: {str(e)}")
        return None

# Function to analyze text and optionally an image
def analyze_image_and_text(text_description, image_url=None):
    # Prepare the messages list for OpenAI
    messages = [
        {
            "role": "system",
            "content": "You are a medical assistant. You will take the user's description of their symptoms and any provided image analysis to generate an informal diagnosis and advice for medications or homemade remedies. For mental health issues, provide emotional reassurance."
        },
        {
            "role": "user",
            "content": text_description
        }
    ]

    # If image URL is provided, fetch and encode the image
    if image_url:
        image_content = fetch_and_encode_image(image_url)
        if image_content:
            messages.append({
                "role": "user",
                "content": {
                    "text": text_description,
                    "image": {
                        "type": "image/jpeg",
                        "content": image_content
                    }
                }
            })

    try:
        # Generate the medical advice using OpenAI's Chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=400,
            temperature=0.8
        )

        # Extract the generated advice from the response
        advice = response['choices'][0]['message']['content']
        return advice
    except Exception as e:
        st.error(f"An error occurred in OpenAI processing: {str(e)}")
        return None

# Initialize OpenAI client with API key
api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

# Streamlit application
st.title("DocGPT: Your Medical Assistant")
with st.form(key='input_form'):
    st.write('Please provide information for health analysis')
    text_input = st.text_input('Enter symptoms or health concerns')

    image_url_input = st.text_input('Enter image URL (optional)')

    submitted = st.form_submit_button("Submit")
    if submitted and text_input.strip():
        advice = analyze_image_and_text(text_input, image_url_input)
        if advice:
            st.write("Here's your medical advice:")
            st.info(advice)
            st.balloons()
    elif submitted and text_input.strip() == '':
        st.warning('Please enter some symptoms or health concerns.')

st.markdown(
    """
    <div style='display: flex; align-items: center;'>
        <img src='https://img.icons8.com/ios-filled/50/3498db/info.png' 
            alt='Information' 
            style='width: 20px; height: 20px; margin-right: 10px;'/>
        <span style='font-size: 16px; color: #3498db;'>Thank you for using DocGPT!</span>
    </div>
    """, 
    unsafe_allow_html=True
)
