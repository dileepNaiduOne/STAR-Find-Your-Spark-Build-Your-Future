import streamlit as st
from backend.database.database_tasks import check_if_email_in_user_data, add_new_user_to_user_data, check_if_user_in_user_data
from backend.code.functions import check_email, jaccard_similarity, cosine_similarity, get_skills_list_from_llm
from backend.code.functions import get_feedback_from_llm
import tempfile
import os

@st.dialog("Sign Up")
def sign_up():
    if "user" not in st.session_state:
        with st.form("signup_form"):
            name = st.text_input("Name :", placeholder="Enter your name")
            email = st.text_input("Email Address :", placeholder="Enter your working email address, STAR will mail you the feedback")
            age = st.text_input("Age :", placeholder="Enter your age")
            gender = st.selectbox(label="Gender", options=["Female", "Male", "Others"], index=None)
            st.divider()
            pin = st.text_input("PIN :", placeholder="Enter your 4 digit PIN", type="password", max_chars=4)
            st.divider()
            secret_sentence = st.text_input("Secret Sentence :", placeholder="Need this for credentials recovery")
            submitted = st.form_submit_button("Sign Up", type="primary")

            if submitted:
                if not secret_sentence or not name or not age or not email or not gender or not pin:
                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> All fields are required </div>""")
                else:
                    if not age.isnumeric():
                        st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Age should be a number </div>""")
                    if not pin.isnumeric():
                        st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> PIN should be a number </div>""")
                    if len(pin) != 4:
                        st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> PIN should have 4 numbers </div>""")
                    if not check_email(email):
                        st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Type in a valid email </div>""")
                    else:
                        secret_sentence = secret_sentence.lower().replace(" ", "")
                        email = email.lower().replace(" ", "")
                        pin = pin.strip()
                        with st.spinner(text="Signing up...", show_time=True):
                            if check_if_email_in_user_data(email) == 1:
                                st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Email you texted is already using by other user. Use another email </div>""")
                            else:
                                add_new_user_to_user_data(name, email, int(age), gender, pin, secret_sentence)

                                st.toast(f"Welcome, {name}! Your account has been created.")
                                
                                user = check_if_user_in_user_data(email, pin)
                                if user == None:
                                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Your credentials is not matching with the database. PLEASE CHECK </div>""")
                                elif len(user) == 7:
                                    st.session_state.user = {
                                                    "user_id" : user[0],
                                                    "name" : user[1],
                                                    "email" : user[2]
                                            }

                                    st.switch_page("frontend/papers/home.py")
    else:
        st.write(f"{st.session_state.user['name']}, Don't try to cheat me😉.")
        st.html("You have already Signed Up. Do <b style='color:maroon;'>Log In</b>")



@st.dialog("Login")
def log_in():
    with st.form("login_form"):
        email = st.text_input("Email Address :", placeholder="Enter your email address")
        pin = st.text_input("PIN :", placeholder="Enter your 4 digit PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if not email or not pin:
                st.error("All fields are required")
            else:
                with st.spinner(text="Logging in...", show_time=True):
                    email = email.lower().replace(" ", "")
                    pin = pin.strip()
                    user = check_if_user_in_user_data(email, pin)
                    if user == None:
                        st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Your credentials is not matching with the database. PLEASE CHECK </div>""")
                    elif len(user) == 7:
                        st.session_state.user = {
                                        "user_id" : user[0],
                                        "name" : user[1],
                                        "email" : user[2]
                                }

                        st.switch_page("frontend/papers/home.py")

                # else:
                #     st.error("Your Secret Sentence is not matching with the database. :red[PLEASE CHECK]")


@st.dialog("Role Fit")
def role_fit(resume_text, desc_text):
    d0, d1, d2, d3, d4 = st.columns([0.10, 0.30, 0.20, 0.30, 0.10])

    with st.spinner(text="Please wait, Extracting skills from Resume & Job Description (≈80 Seconds)", show_time=True):
        resume_list, desc_list = get_skills_list_from_llm(resume_text, desc_text)
        resume_text_set = set(k.lower() for k in resume_list)
        desc_text_set = set(k.lower() for k in desc_list)

        with d1:
            st.metric(label="Keyword Match", value=f"{jaccard_similarity(resume_text_set, desc_text_set)*100:.2f}%")
            st.caption(body="Checks if exact words appear in both resume and job description")

        with d3:
            st.metric(label="Semantic Match", value=f"{cosine_similarity(sorted(resume_text_set), sorted(desc_text_set))*100:.2f}%")
            st.caption(body="Finds meaning-based similarities, even if the words are different")

    st.title("Skills the job wants, but not found in your resume", anchor=False)
    # st.pills(label="Skills the job wants, but not found in your resume", options=list(desc_text_set - resume_text_set))
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(desc_text_set - resume_text_set), unsafe_allow_html=True)



@st.dialog("Add Your Data")
def add_data():

    st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)
    upload = st.file_uploader(label="Resume", label_visibility="collapsed", type=["pdf", "doc", "docx"])
    go = st.button(label="Get Feedback", type="primary")
    st.divider()
    if go:
        if upload:
            st.title("Feedback", anchor=False)
            with st.spinner(text="Please, wait. LLM is working on your file... (≈40 Seconds)", show_time=True):
                extension = os.path.splitext(upload.name)[1]

                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                    tmp_file.write(upload.read())
                    temp_path = tmp_file.name

                feedback = get_feedback_from_llm(temp_path)
                st.session_state.user["feedback"] = feedback
                st.switch_page("frontend/papers/learn_skill.py")
        else:
            st.html(
                f"""
                <div style="
                    color: #A62B1F; 
                    font-weight: bold; 
                    border: 2px solid #F2F2F2; 
                    padding: 10px; 
                    border-radius: 5rem; 
                    background-color: #F2F2F2;
                    display:flex; justify-content:center; align-items:center;
                    ">
                    Please upload the file
                </div>
                """
            )
