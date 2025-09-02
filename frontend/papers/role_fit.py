import streamlit as st
from backend.code.functions import extract_text_from_resume, clean_text, extract_with_pymupdf
import tempfile
import os
import streamlit.components.v1 as components


st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with st.container(key="rolefit"):

    c0, c1 = st.columns([0.5, 0.5], border=True)

    with c0:
        st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)
        st.write("")
        upload = st.file_uploader(label="Resume", label_visibility="collapsed", type=["pdf", "doc", "docx"])
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        go = st.button(label="Extract Text", type="primary")
        st.session_state.user["clicked_go"] = False
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.divider()

        if go:
            if upload:
                extension = os.path.splitext(upload.name)[1]

                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                    tmp_file.write(upload.read())
                    temp_path = tmp_file.name

                text = extract_with_pymupdf(temp_path)
                # text = extract_text_from_resume(temp_path)
                st.session_state.user["resume_extracted_text"] = text
                cleaned_text = clean_text(st.session_state.user["resume_extracted_text"])
                st.session_state.user["resume_cleaned_text"] = cleaned_text
                st.session_state["got_text"] = True


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

        if st.session_state.get("got_text") and "resume_cleaned_text" in st.session_state.user:
                st.markdown(f"""<div style="font-size: 1.5rem;">Cleaned Résumé</div>""", unsafe_allow_html=True)
                st.write("")
                st.html(
                    f"""
                    <div style="
                        max-height: 310px; 
                        overflow-y: scroll; 
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid rgba(38,38,38,0.6); 
                    ">
                        {", ".join(st.session_state.user["resume_cleaned_text"])}
                    </div>
                    """
                )
                # st.write(", ".join(st.session_state.user["resume_cleaned_text"]))
                with st.expander(label="RAW Extracted Résumé"):
                    st.write(st.session_state.user["resume_extracted_text"])

    with c1:
        st.markdown(f"""<div style="font-size: 1.5rem;">Job Description</div>""", unsafe_allow_html=True)
        st.write("")
        description = st.text_area(label="None", label_visibility="collapsed", placeholder="Copy paste the Job Description....", height=200)
        st.write("")
        go_desc = st.button(label="Clean Description", type="primary")
        st.session_state.user["clicked_go"] = False

        st.divider()

        if go_desc:
            if description:
                
                st.session_state.user["description_text"] = description
                cleaned_desc = clean_text(st.session_state.user["description_text"])
                st.session_state.user["desc_cleaned"] = cleaned_desc
                st.session_state["got_desc"] = True


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
                        Please type/paste role description
                    </div>
                    """
                )

        if st.session_state.get("got_desc") and "desc_cleaned" in st.session_state.user:
                st.markdown(f"""<div style="font-size: 1.5rem;">Cleaned Description</div>""", unsafe_allow_html=True)
                st.write("")
                st.html(
                    f"""
                    <div style="
                        max-height: 310px; 
                        overflow-y: scroll; 
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid rgba(38,38,38,0.6); 
                    ">
                        {", ".join(st.session_state.user["desc_cleaned"])}
                    </div>
                    """
                )
                # st.write(", ".join(st.session_state.user["resume_cleaned_text"]))
                with st.expander(label="RAW Description"):
                    st.write(st.session_state.user["description_text"])





    with st.container(key="buttonsPills"):
        fit = st.button(label="Check Role Fit", type="primary")
        if fit:
            pass
            # if "feedback" in st.session_state.user.keys():
            #     # send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
            #     # st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
            #     # del st.session_state.user["feedback"]
            # else:
            #     st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

        back = st.button(label="Back to Home", type="primary")
        if back:
            del st.session_state.user["resume_extracted_text"]
            del st.session_state.user["resume_cleaned_text"]
            del st.session_state["got_text"]
            del st.session_state.user["description_text"]
            del st.session_state.user["desc_cleaned"]
            del st.session_state["got_desc"]

            st.switch_page("frontend/papers/home.py")


    # with st.container(key="feedback_buttons"):
    #     with st.container():
    #         mail = st.button(label="Run", type="primary")
    #     if mail:
    #         pass
    #         # if "feedback" in st.session_state.user.keys():
    #         #     # send_an_email(text=st.session_state.user["feedback"], send_to=st.session_state.user["email"])
    #         #     # st.toast(body=f"👍 Email sent to {st.session_state.user["email"]}", duration="long")
    #         #     # del st.session_state.user["feedback"]
    #         # else:
    #         #     st.toast("😔 Sorry, no feedback. First generate a feedback.", duration="short")

    #     with st.container(key="myButtons"):
    #         back = st.button(label="Back to Home", type="primary")
    #     if back:
    #         st.switch_page("frontend/papers/home.py")
