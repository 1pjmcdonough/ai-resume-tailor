import json
import os
from pathlib import Path
import tempfile
import streamlit as st
from job_tailor import JobTailor
from helpers import Model
from streamlit.runtime.uploaded_file_manager import UploadedFile


def main():
    init_session_state()
    render_header()
    tailoring_section()
    uploads_section()
    configs_section()


def init_session_state():
    if "tailor" not in st.session_state:
        st.session_state.tailor = JobTailor()
    if "resume_filename" not in st.session_state:
        st.session_state.resume_filename = ""
    if "job_desc_filename" not in st.session_state:
        st.session_state.job_desc_filename = ""


def render_header():
    st.set_page_config(
        page_title="AI Job Tailor",
        layout="wide"
    )

    st.markdown("""
        <style>
        /* Hide default sidebar search box and nav links */
        section[data-testid="stSidebarNav"] { display: none; }
        input[placeholder="Search pages"] { display: none !important; }

        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1 { text-align: center; margin-bottom: 0.5rem; }
        .stButton button {
            border-radius: 12px;
            font-size: 16px;
            padding: 0.6em 1.2em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("AI Job Tailor")

    st.page_link("homepage.py", label="🏠 Homepage")
    st.page_link("pages/resume_results.py", label="📄 Resume Results")
    st.page_link("pages/cover_letter.py", label="✉️ Cover Letter")


def tailoring_section():
    col1, col2 = st.columns(spec=2)
    with col1:
        st.button(
            label="Tailor Resume",
            type="primary",
            width="stretch",
            disabled=not (st.session_state.resume_filename and st.session_state.job_desc_filename),
            on_click=tailor_resume
        )
    with col2:
        st.button(
            label="Generate Cover Letter",
            type="primary",
            width="stretch",
            disabled=not (st.session_state.resume_filename and st.session_state.job_desc_filename),
            on_click=generate_cover_letter
        )


def tailor_resume():
    with st.spinner("Tailoring your resume..."):
        st.session_state.tailor.tailor_resume()
        st.success("🎉 Resume tailored successfully!")


def generate_cover_letter():
    with st.spinner("Generating your cover letter..."):
        st.session_state.tailor.generate_cover_letter()
        st.success("📨 Cover letter generated successfully!")


def uploads_section():
    st.markdown("## Upload your Files")
    with st.expander("📄 Upload Your Resume", expanded=not st.session_state.resume_filename):
        resume_file = st.file_uploader(
            label="Upload your resume file",
            type=["pdf", "docx", "txt"],
            help="Upload your resume in pdf, docx, or txt format",
            label_visibility="collapsed"
        )
        
        if resume_file:
            if not st.session_state.resume_filename:
                resume_tmp_path = save_temp_file(resume_file)

                try:
                    st.session_state.tailor.upload_resume(resume_tmp_path)
                    st.session_state.resume_filename = resume_file.name
                    st.rerun()
                finally:
                    os.remove(resume_tmp_path)
        else:
            st.session_state.resume_filename = ""

    if st.session_state.resume_filename:
        st.success(f"Job description uploaded: {st.session_state.resume_filename}")
    
    with st.expander("📝 Upload the Job Description", expanded=not st.session_state.job_desc_filename):
        job_desc_file = st.file_uploader(
            label="Upload the job description file",
            type=["pdf", "docx", "txt"],
            help="Upload the job description in pdf, docx, or txt format",
            label_visibility="collapsed"
        )
    
        if job_desc_file:
            if not st.session_state.job_desc_filename:
                job_desc_tmp_path = save_temp_file(job_desc_file)

                try:
                    st.session_state.tailor.upload_job_desc(job_desc_tmp_path)
                    st.session_state.job_desc_filename = job_desc_file.name
                    st.rerun()
                finally:
                    os.remove(job_desc_tmp_path)
        else:
            st.session_state.job_desc_filename = ""

    if st.session_state.job_desc_filename:
        st.success(f"Job description uploaded: {st.session_state.job_desc_filename}")
        

def save_temp_file(uploaded_file: UploadedFile) -> Path:
    """Save uploaded file to a temp path and return path"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
        tmp.write(uploaded_file.read())
        return Path(tmp.name)

    
def configs_section():
    st.markdown("## Set some Configurations")
        
    model = st.selectbox(
        label="Choose a Model",
        options=[model.name for model in Model],
        key="model_selection",
        help="Select the model to use for resume tailoring",
        placeholder="Select a model"
    )
    st.session_state.tailor.set_model(model)
    st.session_state.tailor.configure_client()
    
    guidelines = st.text_area(
        label="Add Custom Guidelines (Optional)",
        placeholder="Enter any other important information...",
        help="Optional: Add specific instructions for how you want your resume tailored"
    )
    st.session_state.tailor.add_user_context(guidelines)


if __name__ == "__main__":
    main()