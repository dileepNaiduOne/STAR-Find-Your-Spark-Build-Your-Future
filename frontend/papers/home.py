import streamlit as st
st.set_page_config(layout="wide")
st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; align-items:center;">
        <img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR%20Logo.png" 
             alt="User Image" style="max-width:20%;">
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")
st.write("")
try:
    st.markdown(f"""<div style="display:flex; justify-content:center; align-items:center; font-size: 400%;"> Hey! &nbsp<b style='color:#262626;'>{st.session_state.user["name"]}</div>""", unsafe_allow_html=True)
except AttributeError:
    st.switch_page("frontend/papers/reload_error.py")


st.write("")
st.write("")

with st.container(key="pills1"):
    task = st.pills(label="select", options=["Résumé Feedback", "Log Out"], label_visibility="collapsed")

if task == "Résumé Feedback":
    st.switch_page("frontend/papers/resume_check.py")

if task == "Log Out":
    for key in st.session_state.keys():
        del st.session_state[key]
    st.switch_page("frontend/papers/login.py")