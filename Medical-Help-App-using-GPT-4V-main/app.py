import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
from PIL import Image
import os
import io
load_dotenv()
def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
os.environ['GOOGLE_API_KEY'] = "AIzaSyCEqvAzAJGDK9VEZ_wxmXEACf8Nwe7UeSs"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
st.image("C:/Users/91983/Downloads/limitlesshackathon/logo.png", width=200)
st.write("")
gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])
def generate_medical_report(image_prompt, uploaded_file):
    model = genai.GenerativeModel("gemini-pro-vision")
    if uploaded_file is not None:
        if image_prompt != "":
            image = Image.open(uploaded_file)
            response = model.generate_content(
                glm.Content(
                    parts=[
                        glm.Part(text=image_prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type="image/jpeg",
                                data=image_to_byte_array(image)
                            )
                        )
                    ]
                )
            )
            response.resolve()
            return response.text
        else:
            return ":red[Please Provide a prompt]"
    else:
        return ":red[Please Provide an image]"
def main():
    with gemini_pro:
        st.header("Interact with Gemini Pro")
        st.write("")
        prompt = st.text_input("prompt please...", placeholder="Prompt", label_visibility="visible")
        model = genai.GenerativeModel("gemini-pro")
        if st.button("SEND", use_container_width=True):
            response = model.generate_content(prompt)
            st.write("")
            st.header(":blue[Response]")
            st.write("")
            st.markdown(response.text)
    with gemini_vision:
        st.header("Interact with Gemini Pro Vision")
        st.write("")
        image_prompt = st.text_area("Image Analysis Prompt",
                                    "You are a medical practitioner and an expert in analyzing medical-related images working for a very reputed hospital. You will be provided with images, and you need to identify any anomalies, diseases, or health issues. Write down all the detailed findings, next steps, recommendations, etc. Respond only if the image is related to the human body and health issues. If certain aspects are not clear from the image, state, 'Unable to determine based on the provided image.' Disclaimer: Consult with a doctor before making any decisions.")
        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])
        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)
            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
        if st.button("GET RESPONSE", use_container_width=True):
            result = generate_medical_report(image_prompt, uploaded_file)
            st.write("")
            st.header(":blue[Medical Report]")
            st.write("")
            st.markdown(result)
if __name__ == "__main__":
    main()