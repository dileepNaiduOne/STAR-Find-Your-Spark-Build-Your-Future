import streamlit as st
st.set_page_config(layout="wide")
st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; align-items:center;">
        <img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR%20Logo.png" 
             alt="User Image" style="max-width:max(17vw, 17vh);">
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

with st.container(key="coffee"):
    st.write("")
    st.write("")
    st.divider()
    st.write("")
    st.markdown(f"""<div style="display:flex; justify-content:center; align-items:center; font-size: max(1vw, 1vh);"> If this Star App made a difference in your career, a coffee is the perfect thank you </div>""", unsafe_allow_html=True)
    # st.caption("If this Star made a difference, a coffee is the perfect thank you")
    st.write("")
    st.html('''<div style="display:flex; justify-content:center; align-items:center;" > <a href="https://www.buymeacoffee.com/dileepnaidu" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=dileepnaidu&button_colour=FAED7D&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff" /></a> </div>''')

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
