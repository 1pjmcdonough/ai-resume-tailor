import json
import os
from pathlib import Path
import tempfile
import streamlit as st
import streamlit.components.v1 as components
from job_tailor import JobTailor
from helpers import Model


def main():
    init_session_state()

    header_section()

    configs_section()

    uploads_section()

    tailoring_section()


def init_session_state():
    if "tailor" not in st.session_state:
        st.session_state.tailor = JobTailor()


def header_section():
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.page_link("homepage.py", label="Homepage")
    # with col2:
    #     st.page_link("pages/tailored_resume_results.py", label="Tailored Resume Results") #move to only be available once results are ready (move to tailoring section)
    # with col3:
    #     st.page_link("pages/generated_cover_letter.py", label="Generated Cover Letter") # same as above but for cover letter

    st.set_page_config(
        page_title="AI Job Tailor",
        layout="wide"
    )

    st.title("AI Job Tailor")
    st.divider()


def configs_section():
    with st.sidebar:
        st.markdown("# Configurations")
        
        model = st.selectbox(
            label="Model",
            options=[model.name for model in Model],
            key="model_selection",
            help="Select the model to use for resume tailoring",
            placeholder="Select a model"
        )
        st.session_state.tailor.set_model(model)
        st.session_state.tailor.configure_client()
        
        guidelines = st.text_area(
            label="Custom Guidelines (Optional)",
            placeholder="Enter any other important information...",
            help="Optional: Add specific instructions for how you want your resume tailored"
        )
        st.session_state.tailor.add_user_context(guidelines)


def uploads_section():
    st.markdown("### 1. Upload your resume")
    resume_file = st.file_uploader(
        label="Upload your resume file",
        type=["pdf", "docx", "txt"],
        help="Upload your resume in pdf, docx, or txt format",
        label_visibility="collapsed"
    )
    
    if resume_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.name).suffix) as tmp:
            tmp.write(resume_file.read())
            tmp_path = Path(tmp.name)

        try:
            st.session_state.resume_uploaded = st.session_state.tailor.upload_resume(tmp_path)
            st.success(f"Resume uploaded: {resume_file.name}")
        finally:
            os.remove(tmp_path)

        st.markdown("### 2. Upload the job description")
        job_desc_file = st.file_uploader(
            "Upload the job description file",
            type=["pdf", "docx", "txt"],
            help="Upload the job description in pdf, docx, or txt format"
        )
    
        if job_desc_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(job_desc_file.name).suffix) as tmp:
                tmp.write(job_desc_file.read())
                tmp_path = Path(tmp.name)

            try:
                st.session_state.job_desc_uploaded = st.session_state.tailor.upload_job_desc(tmp_path)
                st.success(f"Job description uploaded: {job_desc_file.name}")
            finally:
                os.remove(tmp_path)
        else:
            st.session_state.job_desc_uploaded = False
    else:
        st.session_state.resume_uploaded = False


#TODO: add caution to not forget to check configurations before running
def tailoring_section():
    if st.session_state.resume_uploaded and st.session_state.job_desc_uploaded:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(label="Tailor Resume", type="primary", width="stretch"):
                with st.spinner("Tailoring your resume..."):
                    st.session_state.tailor.tailor_resume()
                    st.success("Resume tailored successfully!")
                    
            if st.button(
                label="Generate Cover Letter", type="primary", width="stretch"):
                with st.spinner("Generating your cover letter..."):
                    st.session_state.tailor.generate_cover_letter()
                    st.success("Cover letter generated successfully!")

if __name__ == "__main__":
    main()