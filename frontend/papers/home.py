import streamlit as st
st.set_page_config(layout="wide")
st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; align-items:center;">
        <img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR%20Logo.png" 
             alt="User Image" style="max-width:max(20vw, 20vh);">
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")
st.write("")
try:
    st.markdown(f"""<div style="display:flex; justify-content:center; align-items:center; font-size: max(5vw, 5vh);"> Hey! &nbsp<b style='color:#262626;'>{st.session_state.user["name"]}</div>""", unsafe_allow_html=True)
except AttributeError:
    st.switch_page("frontend/papers/reload_error.py")


st.write("")
st.write("")


with st.container(key="buttonsPills"):

    feedback_button = st.button(label="Résumé Feedback", type="primary")
    if feedback_button:
        st.switch_page("frontend/papers/resume_check.py")

    rolefit_button = st.button(label="Role Fit", type="primary")
    if rolefit_button:
        st.switch_page("frontend/papers/role_fit.py")

    logout_button = st.button(label="Log Out", type="primary")
    if logout_button:
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("frontend/papers/login.py")


# with st.container(key="pills1"):
#     task = st.pills(label="select", options=["Résumé Feedback", "Role Fit", "Log Out"], label_visibility="collapsed")

# if task == "Résumé Feedback":
#     st.switch_page("frontend/papers/resume_check.py")

# if task == "Role Fit":
#     st.switch_page("frontend/papers/role_fit.py")

# if task == "Log Out":
#     for key in st.session_state.keys():
#         del st.session_state[key]
#     st.switch_page("frontend/papers/login.py")
