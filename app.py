from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import io
import base64
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision') ## importing required for the app
    response = model.generate_content([input,pdf_content[0],prompt]) 
    return response.text
    
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit app
st.set_page_config(page_title="ATS Resume Checker")
st.header("ATS Tracker")
input_text = st.text_area("Job Description:", key ="input")
uploaded_file =st.file_uploader("Upload Your Resume in pdf format", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
submit1 = st.button("Tell Me About The Resume")
##submit2 = st.button("Provide Missing Keywords")
##submit3 = st.button("Enhance my Resume")
submit4 = st.button("Percentage Match")

input_prompt1 = """
you are an experienced HR with technical experience in the field of Software Development , Data Science , Big Data Engineering, DEVOPS,Data analyst, Sailpoint Engineer/Developer, Full stack web development, your task is to review the provided resume for the given job description.
please share your professional evaluation on whether the applicant's profile aligns with the job description.
Highlight the strength and weaknesses of the applicant in relation to the specific job role
"""
##input_prompt2 = """
##As an advanced ATS (Applicant Tracking System) with expertise in the tech industry, specifically in areas such as Software Development, 
##Data Science, Big Data Engineering, DevOps, Data Analysis, and Full Stack Web Development, review the uploaded resume in light of the 
##job description provided. Offer actionable suggestions on how the applicant can enhance their resume. Focus on additional skills to acquire, 
##certifications, experiences to gain, or specific achievements to highlight that would make the resume more attractive for this role. 
##Provide guidance on how to structure the resume to better reflect the applicant's qualifications for the job.
##"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Software Development , Data Science , Big Data Engineering, DEVOPS,Data analyst, Sailpoint Engineer/Developer, Full stack web development  and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then last final thoughts.
"""

##input_prompt4 = """
##As a highly experienced ATS with an intricate understanding of recruitment processes in tech industries, 
##including Software Development, Data Science, Big Data Engineering, DevOps, Data Analysis, and Full Stack Web Development, 
##your task is to meticulously analyze the uploaded resume against the provided job description. Your goal is to identify any 
##critical skills, keywords, or qualifications mentioned in the job description that are not present in the resume. List these 
##missing elements in a clear and structured format, providing straightforward feedback that the applicant can use to align their 
##resume more closely with the job expectations. This analysis will help the candidate understand which areas of expertise or 
##keywords they might need to highlight or add to their resume to improve their chances of being noticed and considered for the role.

##"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload your Resume")
##elif submit2:
 ##   if uploaded_file is not None:
  ##      pdf_content = input_pdf_setup(uploaded_file)
   ##     response = get_gemini_response(input_prompt4, pdf_content, input_text)
   ##     st.subheader("Missing Words Analysis")
   ##     st.write(response)
   ## else:
    ##    st.write("Please upload your Resume.")

##elif submit3:
##    if uploaded_file is not None:
 ##       pdf_content = input_pdf_setup(uploaded_file)
 ##       response = get_gemini_response(input_prompt2, pdf_content, input_text)
 ##       st.subheader("Resume Enhancement Suggestions")
 ##       st.write(response)
 ##   else:
 ##       st.write("Please upload your resume to get enhancement suggestions.")

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload your Resume")


    


