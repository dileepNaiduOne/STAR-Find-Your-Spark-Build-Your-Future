import streamlit as st
from backend.database.database_tasks import ckeck_if_email_in_user_data, add_new_user_to_user_data, ckeck_if_user_in_user_data



@st.dialog("Sign Up")
def sign_up():
    if "user" not in st.session_state:
        with st.form("signup_form"):
            name = st.text_input("Name :", placeholder="Enter your name")
            email = st.text_input("Email Address :", placeholder="Enter your email address")
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
                    else:
                        secret_sentence = secret_sentence.lower().replace(" ", "")
                        email = email.lower().replace(" ", "")
                        pin = pin.strip()
                        with st.spinner(text="Signing up...", show_time=True):
                            if ckeck_if_email_in_user_data(email) == 1:
                                st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Email you texted is already using by other user. Use another email </div>""")
                            else:
                                add_new_user_to_user_data(name, email, age, gender, pin, secret_sentence)

                                st.toast(f"Welcome, {name}! Your account has been created.")
                                
                                user = ckeck_if_user_in_user_data(email, pin)
                                if user == None:
                                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Your credentials is not matching with the database. PLEASE CHECK </div>""")
                                elif len(user) == 7:
                                    st.session_state.user = {
                                                    "user_id" : user[0],
                                                    "name" : user[1],
                                                    "email" : user[2]
                                            }

                                    st.switch_page("frontend/papers/home.py")

                            st.rerun()
    else:
        st.write(f"{st.session_state.user["name"]}, Don't try to cheat me😉.")
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
                    user = ckeck_if_user_in_user_data(email, pin)
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