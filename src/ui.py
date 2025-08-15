import streamlit as st
import io
from tailor_resume import TailorResume, ResumeData, JobDescription

def main():
    st.set_page_config(
        page_title="AI Resume Tailor",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("🤖 AI Resume Tailor")
    st.markdown("Upload your resume and job description to get a tailored resume and cover letter!")
    
    # Initialize the AI agent
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = TailorResume()
            st.success("AI Agent initialized successfully!")
        except Exception as e:
            st.error(f"Failed to initialize AI Agent: {str(e)}")
            st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model = st.selectbox(
            "AI Model",
            ["grok-4-0709", "grok-beta", "grok-1"],
            help="Select the AI model to use for resume tailoring"
        )
        
        # Guidelines input
        guidelines = st.text_area(
            "Custom Guidelines",
            placeholder="Enter any specific guidelines for tailoring your resume...",
            help="Optional: Add specific instructions for how you want your resume tailored"
        )
        
        # Job details
        st.subheader("Job Information")
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
        company = st.text_input("Company", placeholder="e.g., Tech Corp Inc.")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📄 Upload Resume")
        resume_file = st.file_uploader(
            "Choose your resume file",
            # type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format"
        )
        
        if resume_file:
            st.success(f"✅ Resume uploaded: {resume_file.name}")
            
            # Parse resume
            try:
                resume_data = st.session_state.agent.parse_resume_file(
                    resume_file.read(), 
                    resume_file.type
                )
                
                # Display resume stats
                st.info(f"📊 Resume Statistics:")
                st.write(f"- **Word Count:** {resume_data.word_count}")
                st.write(f"- **Estimated Pages:** {resume_data.page_estimate:.1f}")
                
                # Show extracted sections
                if resume_data.sections:
                    st.subheader("📋 Resume Sections Detected:")
                    for section, content in resume_data.sections.items():
                        with st.expander(f"{section.title()}"):
                            st.text(content[:200] + "..." if len(content) > 200 else content)
                
                st.session_state.resume_data = resume_data
                
            except Exception as e:
                st.error(f"❌ Error parsing resume: {str(e)}")
    
    with col2:
        st.header("💼 Upload Job Description")
        job_file = st.file_uploader(
            "Choose job description file",
            # type=["pdf", "docx", "txt"],
            help="Upload the job description in PDF, DOCX, or TXT format"
        )
        
        if job_file:
            st.success(f"✅ Job description uploaded: {job_file.name}")
            
            # Parse job description
            try:
                job_desc = st.session_state.agent.parse_job_description(
                    job_file.read(),
                    job_file.type
                )
                
                # Display extracted information
                st.info(f"🔍 Job Analysis:")
                st.write(f"- **Keywords Found:** {len(job_desc.keywords)}")
                st.write(f"- **Requirements:** {len(job_desc.requirements)}")
                st.write(f"- **Responsibilities:** {len(job_desc.responsibilities)}")
                
                # Show keywords
                if job_desc.keywords:
                    st.subheader("🔑 Key Skills & Technologies:")
                    st.write(", ".join(job_desc.keywords))
                
                # Show requirements
                if job_desc.requirements:
                    st.subheader("📋 Requirements:")
                    for req in job_desc.requirements[:5]:  # Show first 5
                        st.write(f"• {req}")
                
                st.session_state.job_desc = job_desc
                
            except Exception as e:
                st.error(f"❌ Error parsing job description: {str(e)}")
    
    # Process button
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
                            guidelines
                        )
                        
                        st.session_state.results = results
                        st.success("✅ Resume tailored successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during resume tailoring: {str(e)}")
    
    # Display results
    if 'results' in st.session_state:
        st.markdown("---")
        st.header("🎯 Results")
        
        # Create tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Tailored Resume", 
            "✉️ Cover Letter", 
            "📊 Changes Summary", 
            "💡 Recommendations"
        ])
        
        with tab1:
            st.subheader("Tailored Resume")
            if st.session_state.results['tailored_resume']:
                st.text_area(
                    "Tailored Resume Content",
                    value=st.session_state.results['tailored_resume'],
                    height=400,
                    disabled=True
                )
                
                # Download button
                resume_text = st.session_state.results['tailored_resume']
                st.download_button(
                    label="📥 Download Tailored Resume",
                    data=resume_text,
                    file_name="tailored_resume.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No tailored resume content available.")
        
        with tab2:
            st.subheader("Cover Letter")
            if st.session_state.results['cover_letter']:
                st.text_area(
                    "Cover Letter Content",
                    value=st.session_state.results['cover_letter'],
                    height=400,
                    disabled=True
                )
                
                # Download button
                cover_text = st.session_state.results['cover_letter']
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_text,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No cover letter content available.")
        
        with tab3:
            st.subheader("Changes Summary")
            if st.session_state.results['changes_summary']:
                st.write(st.session_state.results['changes_summary'])
            else:
                st.warning("No changes summary available.")
            
            if st.session_state.results['word_count']:
                st.info(st.session_state.results['word_count'])
        
        with tab4:
            st.subheader("Recommendations")
            if st.session_state.results['recommendations']:
                st.write(st.session_state.results['recommendations'])
            else:
                st.warning("No recommendations available.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by AI | 📄 Resume Tailoring Made Easy</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
