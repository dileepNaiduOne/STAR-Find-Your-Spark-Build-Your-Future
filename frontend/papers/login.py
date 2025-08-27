import streamlit as st
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

c0, c1, c2, c3= st.columns([0.1, 0.5, 0.3, 0.1])

with c1:
    with st.container(key="custom1"):
        with st.container(key="customLogo"):
            st.image(r"frontend\assets\STAR.png")
        with st.container(key="customHeadLine"):
            st.text("HeadLine")
        with st.container(key="customLogin"):
            st.pills(label="select", options=["Sign Up", "Login"], label_visibility="collapsed")



with c2:
    st.image(r"frontend\assets\Home-Stick.png")