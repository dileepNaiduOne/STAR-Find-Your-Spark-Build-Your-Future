import pdfplumber
import docx
from dotenv import load_dotenv
from io import BytesIO
import os
from google import genai
from pydantic import BaseModel, Field
import pathlib
from backend.code.shuffle_llm_key import get_a_key
from config import LLM_model, LLM_model_for_skills_extraction
from backend.code.prompts import resume_feedback_prompt, role_fit_prompt
from backend.database.database_tasks import add_new_user_to_profile_data
from email_validator import validate_email, EmailNotValidError
from sentence_transformers import SentenceTransformer, util
import streamlit as st
import spacy
import fitz
import re
nlp = spacy.load("en_core_web_sm")





class FeedbackOutput(BaseModel):
    user_profile: str = Field(..., description="Synthesize a professional and learning profile of the candidate in a single paragraph")
    soft_skills: list[str] = Field(..., description="List of soft skills extracted from the resume")
    tech_skills: list[str] = Field(..., description="List of technical skills extracted from the resume")
    feedback: str = Field(..., description="Overall feedback summary of the resume")


class RoleFitSkillsList(BaseModel):
    llm_resume_skills: list[str] = Field(..., description="List of skills extracted from the resume")
    llm_desc_skills: list[str] = Field(..., description="List of skills extracted from the job description")


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

    user_profile = response_json.user_profile
    soft = response_json.soft_skills
    tech = response_json.tech_skills
    feed = response_json.feedback

    add_new_user_to_profile_data(user_id=st.session_state.user["user_id"], profile=user_profile, soft_skills=soft, tech_skills=tech)
    

    return feed


def get_skills_list_from_llm(resume_cleaned_text, desc_cleaned):
    # Build the prompt
    full_prompt = role_fit_prompt(resume_cleaned_text, desc_cleaned)
    # Clean hidden characters but preserve line breaks
    full_prompt = full_prompt.replace("\t", "").replace("\r", "").strip()
    # print(full_prompt)  # Debug only

    # Initialize client
    client = genai.Client(api_key=get_a_key())

    # Send request
    response = client.models.generate_content(
        model=LLM_model_for_skills_extraction,
        contents=[full_prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": RoleFitSkillsList
        }
    )

    # Parse response JSON using Pydantic schema
    response_json = RoleFitSkillsList.model_validate_json(response.text)

    llm_resume_skills = response_json.llm_resume_skills
    llm_desc_skills = response_json.llm_desc_skills

    return llm_resume_skills, llm_desc_skills


def check_email(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError as e:
        return False


def extract_text_from_resume(file_path):
    st.write(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    st.write(ext)

    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text

    elif ext in [".docx", ".doc"]:
        doc = docx.Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return text

    else:
        return None
    

def extract_with_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
    
    

def clean_text(text):
    doc = nlp(text.lower())

    return [
        token.text
        for token in doc
        if token.is_alpha and not token.is_stop
    ]


def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0 

def cosine_similarity(lis1, list2):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create embeddings for each keyword
    resume_emb = model.encode(lis1, convert_to_tensor=True)
    job_emb = model.encode(list2, convert_to_tensor=True)

    # Option 1: Average embeddings → one vector per set
    resume_avg = resume_emb.mean(dim=0)
    job_avg = job_emb.mean(dim=0)

    cos_sim = util.cos_sim(resume_avg, job_avg).item()
    return cos_sim
    # print(f"Cosine Similarity: {cos_sim*100:.2f}%")

    # Option 2 (optional): Pairwise max similarity for skill matching
    # pairwise = util.cos_sim(resume_emb, job_emb)
    # best_matches = pairwise.max(dim=1).values.mean().item()
    # print(f"Pairwise Skill Match: {best_matches*100:.2f}%")


if __name__ == "__main__":
    a = "apple"
    b = "pineapple"

    print(role_fit_prompt(a, b))