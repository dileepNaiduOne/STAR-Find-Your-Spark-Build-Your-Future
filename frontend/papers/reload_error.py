import streamlit as st
import time


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png", width=70)

st.title("Uh-oh 😟", anchor=False)
st.markdown("### You should not have reloaded the page. <b style='color:maroon;'>Don't Reload Next Time</b>", unsafe_allow_html=True)
st.write("\n")
st.write("\n")
st.write("\n")

a = st.empty()

for i in range(10, 0, -1):
    a.markdown(f"Redirecting to Login page... <b style='color:maroon;'>{i} Seconds left</b>", unsafe_allow_html=True)
    time.sleep(1)

for key in st.session_state.keys():
    del st.session_state[key]

st.switch_page("frontend/papers/login.py")