import streamlit as st
from backend.code.functions import extract_text_from_resume, clean_text, extract_with_pymupdf, jaccard_similarity, cosine_similarity, get_skills_list_from_llm
import tempfile
import os
import streamlit.components.v1 as components
from frontend.papers.streamlit_dialogs import role_fit

st.set_page_config(menu_items={"About":"Dileep Naidu"})

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


try:
    st.write("")
    st.markdown(f"""<div style="display:flex; align-items:center; justify-content:center; font-size: max(3vw, 3vh); gap:max(2vw, 2vh);"><img src="https://raw.githubusercontent.com/dileepNaiduOne/STAR-Find-Your-Spark-Build-Your-Future/refs/heads/main/frontend/assets/STAR.png" alt="logo" style="height:max(3vw, 3vh); width:auto;"><span>| &nbsp; AI-Powered Role Fit Matcher </span></div>""", unsafe_allow_html=True)
    st.write("")
    st.write("")

    with st.container(key="rolefit"):

        c0, c1 = st.columns([0.5, 0.5], border=True)

        with c0:
            st.markdown(f"""<div style="font-size: 1.5rem;">Upload Your Résumé</div>""", unsafe_allow_html=True)
            st.write("")
            upload = st.file_uploader(label="Resume", label_visibility="collapsed", type=["pdf", "doc", "docx"])
            st.write("")
            go = st.button(label="Extract Text", type="primary")
            st.session_state.user["clicked_go"] = False
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
                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;"> Please upload the file </div> """)

            if st.session_state.get("got_text") and "resume_cleaned_text" in st.session_state.user:
                    st.markdown(f"""<div style="font-size: 1.5rem;">Cleaned Résumé</div>""", unsafe_allow_html=True)
                    st.write("")
                    st.html(f"""<div style="max-height: 310px; overflow-y: scroll; padding: 10px;border-radius: 8px;border: 2px solid rgba(38,38,38,0.6); ">{", ".join(st.session_state.user["resume_cleaned_text"])}</div>""")
                    # st.write(", ".join(st.session_state.user["resume_cleaned_text"]))
                    with st.expander(label="RAW Extracted Résumé"):
                        st.write(st.session_state.user["resume_extracted_text"])

        with c1:
            st.markdown(f"""<div style="font-size: 1.5rem;">Job Description</div>""", unsafe_allow_html=True)
            st.write("")
            description = st.text_area(label="None", label_visibility="collapsed", placeholder="Copy paste the Job Description....", height=150)
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
                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;">Please type/paste role description</div>""")

            if st.session_state.get("got_desc") and "desc_cleaned" in st.session_state.user:
                    st.markdown(f"""<div style="font-size: 1.5rem;">Cleaned Description</div>""", unsafe_allow_html=True)
                    st.write("")
                    st.html(f"""<div style="max-height: 310px; overflow-y: scroll; padding: 10px;border-radius: 8px;border: 2px solid rgba(38,38,38,0.6); ">{", ".join(st.session_state.user["desc_cleaned"])}</div>""")
                    with st.expander(label="RAW Description"):
                        st.write(st.session_state.user["description_text"])

        with st.container(key="buttonsPills"):
            fit = st.button(label="Check Role Fit", type="primary")
            if fit:
                a = st.session_state.get("got_text", default=None)
                b = st.session_state.get("got_desc", default=None)
                if (a != None) and (b != None):
                    resume_cleaned_text = ", ".join(st.session_state.user["resume_cleaned_text"])
                    desc_cleaned = ", ".join(st.session_state.user["desc_cleaned"])
                    
                    role_fit(resume_cleaned_text, desc_cleaned)

                elif a == None:
                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;">Please click on "Extract Text"</div>""")
                elif b == None:
                    st.html(f"""<div style="color: #A62B1F; font-weight: bold; border: 2px solid #F2F2F2; padding: 10px; border-radius: 5rem; background-color: #F2F2F2;display:flex; justify-content:center; align-items:center;">Please click on "Clean Description"</div>""")


            back = st.button(label="Back to Home", type="primary")
            if back:
                # Safely remove keys from nested dict
                st.session_state.user.pop("resume_extracted_text", None)
                st.session_state.user.pop("resume_cleaned_text", None)
                st.session_state.user.pop("description_text", None)
                st.session_state.user.pop("desc_cleaned", None)

                # Safely remove keys from session_state itself
                st.session_state.pop("got_text", None)
                st.session_state.pop("got_desc", None)

                st.switch_page("frontend/papers/home.py")

except AttributeError:
    st.switch_page("frontend/papers/reload_error.py")
