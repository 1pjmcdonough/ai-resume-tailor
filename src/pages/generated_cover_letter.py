import streamlit as st
from pathlib import Path


def main():
    header_section()

    


def header_section():
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.page_link("homepage.py", label="Homepage")
    # with col2:
    #     st.page_link("pages/tailored_resume_results.py", label="Tailored Resume Results") #move to only be available once results are ready (move to tailoring section)
    # with col3:
    #     st.page_link("pages/generated_cover_letter.py", label="Generated Cover Letter") # same as above but for cover letter
        
    st.set_page_config(
        page_title="Generated Cover Letter",
        layout="wide"
    )
    
    st.title("AI Job Tailor")
    st.divider()


if __name__ == "__main__":
    main()