import streamlit as st
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

c0, c1, c2, c3, c4= st.columns([0.1, 0.45, 0.1, 0.25, 0.1])

with c1:
    with st.container(key="custom1"):
        with st.container(key="customLogo"):
            s0, s1, = st.columns([0.2, 0.8])
            with s0:
                st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png")
        with st.container(key="customHeadLine"):
            st.text("A Personalized Guide\nto Your Future")
        with st.container(key="customHeadTags"):
            st.markdown("""Résumé Feedback &nbsp;&nbsp;•&nbsp;&nbsp; Career Guide &nbsp;&nbsp;•&nbsp;&nbsp; Role Judge &nbsp;&nbsp;•&nbsp;&nbsp; Step-by-Step Skill Path &nbsp;&nbsp;•&nbsp;&nbsp; A Friend Who Believes in You""")
        with st.container(key="customLogin"):
            st.pills(label="select", options=["Sign Up", "Login"], label_visibility="collapsed")



with c3:
    st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/Home-Stick.png")