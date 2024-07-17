import streamlit as st
from openai import OpenAI
from io import BytesIO
import PIL.Image
import requests

# Initialize OpenAI client with API key
api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

# Function to analyze text and optionally an image
def analyze_image_and_text(text_description, image_bytes=None):
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

    # If image bytes are provided, add it to the messages list
    if image_bytes:
        messages.append({
            "role": "user",
            "content": {"text": text_description, "image": image_bytes}
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

# Streamlit application
st.title("DocGPT: Your Medical Assistant")
with st.form(key='input_form'):
    st.write('Please provide information for health analysis')
    text_input = st.text_input('Enter symptoms or health concerns')

    uploaded_file = st.file_uploader("Upload an image (JPEG only)", type=["jpg", "jpeg"])

    submitted = st.form_submit_button("Submit")
    if submitted and text_input.strip():
        image_bytes = None
        if uploaded_file is not None:
            image = PIL.Image.open(uploaded_file)
            # Convert image to JPEG bytes
            jpeg_image = BytesIO()
            image.save(jpeg_image, format='JPEG')
            image_bytes = jpeg_image.getvalue()

        advice = analyze_image_and_text(text_input, image_bytes)
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
