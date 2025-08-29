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
                    st.error("All fields are required.")
                else:
                    if not age.isnumeric():
                        st.error("Age should be a number.")
                    if not pin.isnumeric():
                        st.error("PIN should be a number.")
                    if len(pin) != 4:
                        st.error("PIN should have 4 numbers.")
                    else:
                        secret_sentence = secret_sentence.lower().replace(" ", "")
                        email = email.lower().replace(" ", "")
                        pin = pin.strip()
                        if ckeck_if_email_in_user_data(email) == 1:
                            st.error("Email you texted is already using by other user. Use another email")
                        else:
                            add_new_user_to_user_data(name, email, age, gender, pin, secret_sentence)

                            st.success(f"Welcome, {name}! Your account has been created.")
                            
                            user = ckeck_if_user_in_user_data(email, pin)
                            if user == None:
                                st.error("Your credentials is not matching with the database. PLEASE CHECK")
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
        st.write("You have already Signed Up. Do <b style='color:maroon;'>Log In</b>")



@st.dialog("Login")
def log_in():
    with st.form("login_form"):
        email = st.text_input("Email Address :", placeholder="Enter your email address")
        pin = st.text_input("PIN :", placeholder="Enter your 4 digit PIN", type="password", max_chars=4)

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if not email or not pin:
                st.error("All fields are required.")
            else:
                email = email.lower().replace(" ", "")
                pin = pin.strip()
                user = ckeck_if_user_in_user_data(email, pin)
                if user == None:
                    st.error("Your credentials is not matching with the database. PLEASE CHECK")
                elif len(user) == 7:
                    st.session_state.user = {
                                    "user_id" : user[0],
                                    "name" : user[1],
                                    "email" : user[2]
                            }

                    st.switch_page("frontend/papers/home.py")

                # else:
                #     st.error("Your Secret Sentence is not matching with the database. :red[PLEASE CHECK]")