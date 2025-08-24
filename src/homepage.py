import json
import streamlit as st
import streamlit.components.v1 as components
from job_tailor import JobTailor
from helpers import Model


def main():

    header_section()

    configs_section()

    uploads_section()

    tailoring_section()



def init_session_state():
    pass


def header_section():
    st.set_page_config(
        page_title="AI Job Tailor",
        layout="wide"
    )
    
    st.title("AI Job Tailor")
    st.markdown("Upload your resume and job description to get a tailored resume and cover letter!")


def configs_section():
    with st.sidebar:
        st.markdown("# Configurations")
        
        # Model selection
        model = st.selectbox(
            label="Model",
            options=[model.value for model in Model],
            key="model_selection",
            help="Select the model to use for resume tailoring",
            placeholder="Select a model"
        )
        
        # Additional user context
        guidelines = st.text_area(
            label="Custom Guidelines (Optional)",
            placeholder="Enter any specific guidelines for tailoring your resume...",
            help="Optional: Add specific instructions for how you want your resume tailored"
        )
        # Persist guidelines for access in other sections
        st.session_state["guidelines"] = guidelines


def uploads_section():
    st.header(":orange[Upload Files]", anchor="file_uploads")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Resume")
        resume_file = st.file_uploader(
            "Upload your resume file",
            type=["pdf", "docx", "txt"],
            help="Upload your resume in pdf, docx, or txt format"
        )
        
        if resume_file:
            st.success(f"✅ Resume uploaded: {resume_file.name}")

    
    with col2:
        st.markdown("### Job Description")
        job_file = st.file_uploader(
            "Upload the job description file", #eventually a link?
            type=["pdf", "docx", "txt"],
            help="Upload the job description in pdf, docx, or txt format"
        )
        
        if job_file:
            st.success(f"✅ Job description uploaded: {job_file.name}")


def tailoring_section():
    # if 'resume_data' in st.session_state and 'job_desc' in st.session_state:
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Tailor Resume & Generate Cover Letter", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is working on your resume..."):
                try:
                    # Tailor the resume
                    results = st.session_state.agent.tailor_resume(
                        st.session_state.resume_data,
                        st.session_state.job_desc,
                        st.session_state.get("guidelines", "")
                    )
                    
                    st.session_state.results = results
                    st.success("✅ Resume tailored successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error during resume tailoring: {str(e)}")


if __name__ == "__main__":
    main()