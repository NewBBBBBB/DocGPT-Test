import streamlit as st
from openai import OpenAI
import requests
import PIL.Image

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

    # If an image URL is provided, fetch the image and add it to the messages list
    if image_url is not None :
      r=requests.get(image_url)
      open('image.png','wb').write(r.content)
      image_desc= PIL.Image.open('image.png')
      messages.append({
            "role": "user",
            "content": {"text": text_description, "image": image_desc}
            })

    try:
        # Generate the medical advice using OpenAI's ChatCompletion API (adjust model as per your access)
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
        st.error(f"An error occurred: {str(e)}")
        return None

api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

st.title("DocGPT")
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
