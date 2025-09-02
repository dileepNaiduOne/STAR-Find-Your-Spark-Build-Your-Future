import streamlit as st
from backend.code.functions import extract_text_from_resume, clean_text
import tempfile
import os
import streamlit.components.v1 as components


st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

c0, c1 = st.columns([0.5, 0.5], border=True)

with c0:
    st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)
    upload = st.file_uploader(label="Resume", label_visibility="collapsed", type=["pdf", "doc", "docx"])
    st.write("")
    go = st.button(label="Extract Text", type="primary")

    st.divider()

    if go:
        if upload:
            extension = os.path.splitext(upload.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                tmp_file.write(upload.read())
                temp_path = tmp_file.name

            text = extract_text_from_resume(temp_path)
            st.session_state.user["resume_extracted_text"] = text
            with st.expander(label="Extracted Résumé"):
                st.write(st.session_state.user["resume_extracted_text"])
            cleaned_text = clean_text(st.session_state.user["resume_extracted_text"])
            st.session_state.user["resume_cleaned_text"] = cleaned_text
            st.write(",".join(st.session_state.user["resume_cleaned_text"]))

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



with c1:
    st.write("Paset Description")

# with st.container(key="feedback_buttons"):
#     with st.container():
#         mail = st.button(label="Run", type="primary")
#     if mail:
#         pass
#         # if "feedback" in st.session_state.user.keys():
#         #     # send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
#         #     # st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
#         #     # del st.session_state.user["feedback"]
#         # else:
#         #     st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

#     with st.container(key="myButtons"):
#         back = st.button(label="Back to Home", type="primary")
#     if back:
#         st.switch_page("frontend/papers/home.py")

with st.container(key="buttonsPills"):
    mail = st.button(label="Run", type="primary")
    if mail:
        pass
        # if "feedback" in st.session_state.user.keys():
        #     # send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
        #     # st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
        #     # del st.session_state.user["feedback"]
        # else:
        #     st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

    back = st.button(label="Back to Home", type="primary")
    if back:
        st.switch_page("frontend/papers/home.py")
