import json
import streamlit as st
import streamlit.components.v1 as components
# from orchestrator import Orchestrator


def main():
    init_session_state()

    header_section()

    configs_section()

    uploads_section()

    tailoring_section()

    results_section()


def init_session_state():
    # Initialize the AI agent
    if 'agent' not in st.session_state:
        st.session_state.agent = ""


def header_section():
    st.set_page_config(
        page_title="AI Resume Tailor",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🤖 AI Resume Tailor")
    st.markdown("Upload your resume and job description to get a tailored resume and cover letter!")


def scroll_to(element_id: str):
    script = (
        "<script>"
        + "var el = window.parent.document.getElementById("
        + json.dumps(element_id)
        + ");"
        + "if (el) { el.scrollIntoView({ behavior: 'smooth' }); }"
        + "</script>"
    )
    components.html(script, height=0)


def configs_section():
    with st.sidebar:
        st.markdown("# Configurations")
        
        # Model selection
        model = st.selectbox(
            label="Model",
            options=["grok-4-0709", "grok-beta", "grok-1"],
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
    if 'resume_data' in st.session_state and 'job_desc' in st.session_state:
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
                        # Smooth scroll to results section
                        scroll_to("results")
                        
                    except Exception as e:
                        st.error(f"❌ Error during resume tailoring: {str(e)}")


def results_section(): #ai_response: json
    st.header("Resume Optimization Suggestions", anchor="results")
    # --- Keywords ---
    st.header("Extracted Keywords from Job Description")
    # st.write(", ".join(ai_response["extracted_keywords"]))

    st.subheader("Missing Keywords")
    # if ai_response["missing_keywords"]:
        # st.write(", ".join(ai_response["missing_keywords"]))
    # else:
        # st.write("✅ No major keywords missing")

    # --- Additions ---
    st.header("Suggested Additions")
    # if ai_response["suggested_additions"]:
        # for add in ai_response["suggested_additions"]:
            # with st.expander(f"Section: {add['section']}"):
                # st.write(add["suggestion"])
    # else:
        # st.write("✅ No additions suggested")

    # --- Revisions ---
    st.header("Suggested Revisions")
    # if ai_response["suggested_revisions"]:
        # for rev in ai_response["suggested_revisions"]:
            # with st.expander(f"Section: {rev['section']}"):
            #     st.markdown(f"**Before:** {rev['before']}")
            #     st.markdown(f"**After:**  :green[{rev['after']}]")
    # else:
    #     st.write("✅ No revisions suggested")

    # ##################
    # #cursor vsersion
    # if 'results' in st.session_state:
    #     st.markdown("---")
    #     st.header("🎯 Results")
        
    #     # Create tabs for different outputs
    #     tab1, tab2, tab3 = st.tabs([
    #         "📄 Tailored Resume", 
    #         "📊 Changes Summary", 
    #         "💡 Recommendations"
    #     ])
        
    #     with tab1:
    #         st.subheader("Tailored Resume")
    #         if st.session_state.results['tailored_resume']:
    #             st.text_area(
    #                 "Tailored Resume Content",
    #                 value=st.session_state.results['tailored_resume'],
    #                 height=400,
    #                 disabled=True
    #             )
                
    #             # Download button
    #             resume_text = st.session_state.results['tailored_resume']
    #             st.download_button(
    #                 label="📥 Download Tailored Resume",
    #                 data=resume_text,
    #                 file_name="tailored_resume.txt",
    #                 mime="text/plain"
    #             )
    #         else:
    #             st.warning("No tailored resume content available.")
        
        
    #     with tab2:
    #         st.subheader("Changes Summary")
    #         if st.session_state.results['changes_summary']:
    #             st.write(st.session_state.results['changes_summary'])
    #         else:
    #             st.warning("No changes summary available.")
            
    #         if st.session_state.results['word_count']:
    #             st.info(st.session_state.results['word_count'])
        
    #     with tab3:
    #         st.subheader("Recommendations")
    #         if st.session_state.results['recommendations']:
    #             st.write(st.session_state.results['recommendations'])
    #         else:
    #             st.warning("No recommendations available.")

if __name__ == "__main__":
    main()