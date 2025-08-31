# import pdfplumber
# import docx
# from dotenv import load_dotenv
# from io import BytesIO
# import os
from google import genai
from pydantic import BaseModel, Field
import pathlib
from backend.code.shuffle_llm_key import get_a_key
from config import LLM_model
from backend.code.prompts import resume_feedback_prompt
from email_validator import validate_email, EmailNotValidError



class FeedbackOutput(BaseModel):
    soft_skills: list[str] = Field(..., description="List of soft skills extracted from the resume")
    tech_skills: list[str] = Field(..., description="List of technical skills extracted from the resume")
    feedback: str = Field(..., description="Overall feedback summary of the resume")


def get_feedback_from_llm(uploaded_file):

    client = genai.Client(api_key=get_a_key())

    # Retrieve and encode the PDF byte
    file_path = pathlib.Path(uploaded_file)

    # Upload the PDF using the File API
    sample_file = client.files.upload(file=file_path)

    response = client.models.generate_content(
        model=LLM_model,
        contents=[sample_file, resume_feedback_prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": FeedbackOutput
        })
    
    response_json = FeedbackOutput.model_validate_json(response.text)
    
    soft = response_json.soft_skills
    tech = response_json.tech_skills
    feed = response_json.feedback

    return feed


def check_email(email):
    try:
        valid = validate_email(email)  # will throw error if invalid
        return True
    except EmailNotValidError as e:
        return False

# def extract_text_from_resume(uploaded_file):
#     '''Not this this, it is not upto mark. Context is not caputing'''
#     filename = uploaded_file.name
#     ext = os.path.splitext(filename)[1].lower()

#     if ext == ".pdf":
#         with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
#             text = "\n".join(page.extract_text() or "" for page in pdf.pages)
#         return text

#     elif ext in [".docx", ".doc"]:
#         doc = docx.Document(uploaded_file)
#         text = "\n".join(p.text for p in doc.paragraphs)
#         return text

#     else:
#         return None
