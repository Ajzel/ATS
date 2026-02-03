import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_bg("background.png")  # change name if needed


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel("gemini-2.5-flash")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page=images[0]
        
        #Convert to Byte
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit App

st.set_page_config(page_title="ATS Resume Analyzer")
st.header("ATS Tracker")
input_text=st.text_area("Enter Job Description",key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("Pdf Uploaded Successfully")
    
    
submit1=st.button("Tell me about my Resume")

#submit2=st.button("How can I improve my skills")

submit3=st.button("Percentage Match with Job Description")

input_prompt1 = """
You are an experienced  HR with Tech Experience in the field of any one job role from Data Science,Artificial Intelligence,Big Data Engineering,DEVOPS,Data Analyst,
your task is to review the resume provided against the job Description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt2 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science,Artificial Intelligence,Big Data Engineering,DEVOPS,Data Analyst,
your role is to scrutize the resume provided in light of the job Description provided.
Share your insights on the cndidate's suitability for the role. from an HR perspective.
Additionaly,offer advice on enhancing the candidate's skills and identify areas for improvement to better match the job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with deep understanding of Data Science,Artificial Intelligence,Big Data Engineering,DEVOPS,Data Analyst roles and deep ATS functionality,
your task is to evaluate the resume against the job Description provided.  give me the percentage match if the resume matches the Job Description. First the Output should come as percentage and then the Keywords missing from the resume to match the Job Description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")