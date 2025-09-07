import streamlit as st
from backend.code.functions import get_feedback_from_llm
from backend.code.send_mail import send_an_email
import tempfile
import os
import streamlit.components.v1 as components


st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

user_id = st.session_state.user["user_id"]

st.write("")
st.markdown(f"""<div style="display:flex; align-items:center; justify-content:center; font-size: max(3vw, 3vh); gap:max(2vw, 2vh);"><img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png" alt="logo" style="height:max(3vw, 3vh); width:auto;"><span>| &nbsp; StarRésumé with AI</span></div>""", unsafe_allow_html=True)
st.write("")

c0, c1 = st.columns([0.5, 0.5])
with c0:
    st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)

    upload = st.file_uploader(label="Resume", label_visibility="collapsed", type=["pdf", "doc", "docx"])
    st.write("")
    st.write("")
    go = st.button(label="Get Feedback", type="primary")

st.divider()
# s1 = st.empty()
# s2 = st.empty()
# s3 = st.empty()
# s1.write("")
# s2.write("")
# s3.write("")

if go:
    if upload:
        st.toast("Scroll down and wait for a moment.", icon=":material/arrow_circle_down:", duration="long")
        st.title("Feedback", anchor=False)
        with st.spinner(text="Please, wait. LLM is working on your file... (≈40 Seconds)", show_time=True):
            extension = os.path.splitext(upload.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                tmp_file.write(upload.read())
                temp_path = tmp_file.name

            # st.write(f"{upload._file_urls.upload_url}/{upload.name}")

            feedback = get_feedback_from_llm(temp_path)
            st.session_state.user["feedback"] = feedback
            st.write(feedback)
        st.divider()
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

with st.container(key="buttonsPills"):
    mail = st.button(label="Email me this feedback", type="primary", icon=":material/outgoing_mail:")
    if mail:
        if "feedback" in st.session_state.user.keys():
            send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
            st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
            del st.session_state.user["feedback"]
        else:
            st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

    back = st.button(label="Back to Home", type="primary")
    if back:
        st.switch_page("frontend/papers/home.py")




# with st.container(key="feedback_buttons"):
#     with st.container():
#         mail = st.button(label="Email me this feedback", type="primary", icon=":material/outgoing_mail:")
#     if mail:
#         if "feedback" in st.session_state.user.keys():
#             send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
#             st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
#             del st.session_state.user["feedback"]
#         else:
#             st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

#     with st.container(key="myButtons"):
#         back = st.button(label="Back to Home", type="primary")
#     if back:
#         st.switch_page("frontend/papers/home.py")