import streamlit as st

st.set_page_config(layout="wide")
st.set_page_config(page_icon="frontend/assets/STAR Logo.png")


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

login_page = st.Page(
    page="frontend/papers/login.py", 
    title="STAR"
)

home_page = st.Page(
    page="frontend/papers/home.py", 
    title=f"STAR - Namaste!"
)

reload_page = st.Page(
    page="frontend/papers/reload_error.py", 
    title=f"Mistake!"
)

resume_check_page = st.Page(
    page="frontend/papers/resume_check.py", 
    title=f"Improve!"
)
pg = st.navigation(pages=[login_page, home_page, reload_page, resume_check_page], position="hidden")

pg.run()
