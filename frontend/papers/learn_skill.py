import streamlit as st
from backend.code.functions import get_skill_suggest_from_LLM, get_skill_plan_suggest_from_LLM
from backend.code.send_mail import send_an_email
from backend.database.database_tasks import check_if_user_in_profile_data
from dotenv import load_dotenv
from frontend.papers.streamlit_dialogs import add_data
import os
import re

load_dotenv()

st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

try:

    user_id = st.session_state.user["user_id"]

    st.write("")
    st.markdown(f"""<div style="display:flex; align-items:center; justify-content:center; font-size: max(3vw, 3vh); gap:max(2vw, 2vh);"><img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png" alt="logo" style="height:max(3vw, 3vh); width:auto;"><span>| &nbsp; NextSkill with AI</span></div>""", unsafe_allow_html=True)
    st.write("")
    st.write("")

    with st.status(label="Checking if, I have your data...") as status:
        if "proflie_info" not in st.session_state.user.keys():
            row = check_if_user_in_profile_data(st.session_state.user["user_id"])
            if row == None:
                user_id = st.session_state.user["user_id"]
                add_data()
                st.rerun()

            else:
                status.update(label="Got your data!", state="complete")
                if "proflie_info" not in st.session_state.user.keys():
                    st.session_state.user["proflie_info"] = row[2]
                if "profile_skills" not in st.session_state.user.keys():
                    st.session_state.user["profile_skills"] = re.split(r",\s*", re.sub(r"[\'\"\{\}]", "", row[3])) + re.split(r",\s*", re.sub(r"[\'\"\{\}]", "", row[4]))

        st.markdown("## About:", unsafe_allow_html=True)
        st.write(st.session_state.user["proflie_info"])
        st.markdown("## Skills:", unsafe_allow_html=True)
        st.write(", ". join(st.session_state.user["profile_skills"]))

    st.divider()

    st.markdown(f"""<div style="font-size: max(1.5vw, 1.5vh);"> How would you like to choose a skill? </div>""", unsafe_allow_html=True)
    # st.caption(body="Skill suggestions are based on your resume")
    selected = st.pills(label="seledt", label_visibility="collapsed", options=["AI Suggestion", "Enter Skill"], default="AI Suggestion")

    if selected == "Enter Skill":
        user_skill = st.text_input(label="s", label_visibility="collapsed", placeholder="Type in the skill you want to learn...")
    else:
        st.write("AI will recommend the most relevant skill for you, tailored to your profile, to help you grow and advance")


    st.divider()
    go_llm = st.button(label="Go", type="primary")
    if go_llm:
        if selected == "AI Suggestion":
            with st.spinner(text="Just a moment… analyzing your profile to suggest best skill to learn... (≈70 Seconds)", show_time=True):
                plan = get_skill_suggest_from_LLM(st.session_state.user["proflie_info"], st.session_state.user["profile_skills"])
                st.session_state.user["plan"] = plan
                st.write(st.session_state.user["plan"])
        if selected == "Enter Skill":
            with st.spinner(text="Just a moment… analyzing your profile to suggest best plan to learn... (≈70 Seconds)", show_time=True):
                plan = get_skill_plan_suggest_from_LLM(user_skill, st.session_state.user["proflie_info"], st.session_state.user["profile_skills"])
                st.session_state.user["plan"] = plan
                st.write(st.session_state.user["plan"])

    st.divider()
    st.write()



    with st.container(key="buttonsPills"):
        mail = st.button(label="Email me this feedback", type="primary", icon=":material/outgoing_mail:")
        if mail:
            if "plan" in st.session_state.user.keys():
                send_an_email(text=st.session_state.user["plan"], send_to=st.session_state.user["email"])
                st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
                del st.session_state.user["plan"]
            else:
                st.toast("😔 Sorry, no plan. First generate a plan.", duration="short")

        back = st.button(label="Back to Home", type="primary")
        if back:
            del st.session_state.user["proflie_info"]
            del st.session_state.user["profile_skills"]
            st.switch_page("frontend/papers/home.py")

except AttributeError:
    st.switch_page("frontend/papers/reload_error.py")