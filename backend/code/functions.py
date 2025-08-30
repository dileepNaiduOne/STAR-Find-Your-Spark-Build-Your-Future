# import pdfplumber
# import docx
# from dotenv import load_dotenv
# from io import BytesIO
# import os
from google import genai
import pathlib
from backend.code.shuffle_llm_key import get_a_key
from config import LLM_model


def get_feedback_from_llm(uploaded_file):

    client = genai.Client(api_key=get_a_key())

    # Retrieve and encode the PDF byte
    file_path = pathlib.Path(uploaded_file)

    # Upload the PDF using the File API
    sample_file = client.files.upload(file=file_path)

    response = client.models.generate_content(
    model=LLM_model,
    contents=[sample_file, "Summarize this document"])
    return response.text

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
