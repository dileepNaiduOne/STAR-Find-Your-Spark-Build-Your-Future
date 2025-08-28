import streamlit as st

st.set_page_config(layout="wide")

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

login_page = st.Page(
    page="frontend/papers/login.py", 
    title="STAR - Welcome"
)

pg = st.navigation(pages=[login_page], position="hidden")

pg.run()
