import streamlit as st
from frontend.papers.streamlit_dialogs import sign_up, log_in

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

c0, c1, c2, c3, c4= st.columns([0.1, 0.45, 0.1, 0.25, 0.1])

with c1:
    with st.container(key="custom1"):
        # with st.container(key="customLogo"):
        #     s0, s1, = st.columns([0.4, 0.6])
        #     with s0:
        #         st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png")

        st.html(f"""<div><img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png" alt="Image" style="max-width:30%;"></div>""")
        st.write("")
        st.write("")
        with st.container(key="customHeadLine"):
            st.text("Super-App That\nAccelerates Reputation")
        with st.container(key="customHeadTags"):
            st.markdown(
                """AI Résumé Feedback &nbsp;&nbsp;•&nbsp;&nbsp; Career Guide &nbsp;&nbsp;•&nbsp;&nbsp; Predict Role Fit &nbsp;&nbsp;•&nbsp;&nbsp; Roadmap to Learn Next Skill  
                <br><br><br><br>
                <i>An AI app that believes in you and truly cares for your journey</i>""",
                unsafe_allow_html=True
            )
        with st.container(key="customLogin"):
            do = st.pills(label="select", options=["Sign Up", "Login"], label_visibility="collapsed")
            if do == "Sign Up":
                sign_up()
            elif do == "Login":
                log_in()

with c3:
    st.image(r"https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/Home-Stick.png")