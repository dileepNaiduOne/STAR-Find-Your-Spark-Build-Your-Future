import streamlit as st
st.set_page_config(layout="wide")


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

c0, c1, c2= st.columns([0.225, 0.55, 0.225])
# c0, c1, c2= st.columns([0.3, 0.4, 0.3])

# st.session_state.user = {"name" : "Pop"}

with c1:
    try:
        st.markdown(f"""<div style="display:flex; justify-content:center; align-items:center; font-size: 1.5rem; text-decoration: underline;"> Hey! &nbsp<b style='color:maroon;'>{st.session_state.user["name"]}</b>&nbsp 👋 </div>""", unsafe_allow_html=True)
    except AttributeError:
        st.switch_page("frontend/papers/reload_error.py")
    st.write("")
    st.write("")
    st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR%20with%20tag.png")


# resume_feedback = st.button("Résumé Feedback", type="primary")
# if resume_feedback:
#     st.switch_page("frontend/papers/resume_check.py")

# out = st.button("Log Out", type="primary")
# if out:
#     st.switch_page("frontend/papers/login.py")

task = st.pills(label="select", options=["Résumé Feedback", "Log Out"], label_visibility="collapsed")

if task == "Résumé Feedback":
    st.switch_page("frontend/papers/resume_check.py")

if task == "Log Out":
    st.switch_page("frontend/papers/login.py")