import streamlit as st



@st.dialog("Sign Up")
def sign_up():
    if "user" not in st.session_state:
        with st.form("signup_form"):
            secret_sentence = st.text_input("Secret Sentence :", placeholder="Type here. Remember this. Needed for Log In", type="password")
            st.divider()
            name = st.text_input("Name :", placeholder="Enter your name")
            age = st.text_input("Age :", placeholder="Enter your age")
            email = st.text_input("Email Address :", placeholder="Enter your email address")
            gender = st.selectbox(label="Gender", options=["Female", "Male", "Others"], index=None)

            submitted = st.form_submit_button("SIGN UP", type="primary", use_container_width=True)

            if submitted:
                if not secret_sentence or not name or not age or not email or not gender:
                    st.error("All fields are required.")
                if not age.isnumeric():
                    st.error("Age should be a number.")
                else:
                    secret_sentence = secret_sentence.lower().replace(" ", "")
                    # if ckeck_if_ss_in_people(secret_sentence) == 1:
                    #     st.error("Secret Sentence you texted is already using by other user. :red[Use another one]")
                    # else:
                    #     st.success(f"Welcome, {name}! Your account has been created.")
                    #     st.session_state.user = {
                    #             "secret_sentence" : secret_sentence,
                    #             "name" : name,
                    #             "age" : age,
                    #             "email" : email,
                    #             "gender" : gender
                    #     }

                        
                    #     name = name.lower()
                    #     age = int(age)
                    #     gender = gender.lower()

                    #     add_people_data(secret_sentence, name, age, email, gender)

                    #     st.rerun()
    else:
        st.write(f"{st.session_state.user["name"]}, Don't try to cheat me😉.")
        st.write("You have already Signed Up. Do :red[Log In]")



@st.dialog("Login")
def log_in():
    with st.form("login_form"):
        secret_sentence = st.text_input("Secret Sentence :", placeholder="Type here. Remember the Sign Up Sentence", type="password")

        submitted = st.form_submit_button("LOG IN", type="primary", use_container_width=True)

        if submitted:
            if not secret_sentence:
                st.error("All fields are required.")
            else:
                secret_sentence = secret_sentence.lower().replace(" ", "")
                # if ckeck_if_ss_in_people(secret_sentence) == 1:
                #     secret_sentence, name, age, email, gender = get_data_from_people_using_ss(secret_sentence)

                #     st.session_state.user = {
                #             "secret_sentence" : secret_sentence,
                #             "name" : name.upper(),
                #             "age" : age,
                #             "email" : email,
                #             "gender" : gender
                #     }

                #     st.switch_page("papers/home.py")

                # else:
                #     st.error("Your Secret Sentence is not matching with the database. :red[PLEASE CHECK]")