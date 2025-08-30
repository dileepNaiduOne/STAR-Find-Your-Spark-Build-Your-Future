import streamlit as st
from backend.code.functions import get_feedback_from_llm
import tempfile
import os

st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

user_id = st.session_state.user["user_id"]

c0, c1 = st.columns([0.3, 0.7])
with c0:
    s0, s1, = st.columns([0.3, 0.7])
    with s0:
        st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png")
    st.write("")
    st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)

    upload = st.file_uploader(label="Resume", label_visibility="collapsed")
    st.write("")
    st.write("")
    go = st.button(label="Get Feedback", type="primary")

if go:
    if upload:
        st.divider()
        st.title("Feedback", anchor=False)
        with st.spinner(text="Please, wait. LLM is working on your file...", show_time=True):
            extension = os.path.splitext(upload.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                tmp_file.write(upload.read())
                temp_path = tmp_file.name

            # st.write(f"{upload._file_urls.upload_url}/{upload.name}")
            st.write(get_feedback_from_llm(temp_path))
    else:
        st.html(
            f"""
            <div style="
                color: #A62B1F; 
                font-weight: bold; 
                border: 2px solid #F2F2F2; 
                padding: 10px; 
                border-radius: 5rem; 
                background-color: #F2F2F2;
                display:flex; justify-content:center; align-items:center;
                ">
                Please upload the file
            </div>
            """
        )


