import streamlit as st
import json
from pathlib import Path
from homepage import render_header


def main():
    render_header()

    with open(Path(Path(__file__).parent.parent.parent, "response_history", "McDonough_Phil_J.pdf_for_job_desc.pdf", "resume_edits.txt")) as f:
        st.session_state.resume_edits = json.loads(f.read())

    if "resume_edits" in st.session_state:
        results_section()
    else:
        st.info("Tailor your resume for results!")


def results_section():
    """Display the resume tailoring results in an organized format"""

    st.markdown("### Overall Fit Assessment")
    st.info(st.session_state.resume_edits["fit_summary"])
    
    tab1, tab2, tab3 = st.tabs(["Keywords", "Additions", "Revisions"])
    
    with tab1:
        display_keywords_section(st.session_state.resume_edits)
    
    with tab2:
        display_additions_section(st.session_state.resume_edits)
    
    with tab3:
        display_revisions_section(st.session_state.resume_edits)


def display_keywords_section(results):
    """Display extracted and missing keywords"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### :green[Extracted Keywords]")

        for keyword in results["extracted_keywords"]:
            st.markdown(f"- {keyword}")
    
    with col2:
        st.markdown("#### :red[Missing Keywords]")

        for keyword in results["missing_keywords"]:
            st.markdown(f"- {keyword}")


def display_additions_section(results):
    """Display suggested additions"""
    st.markdown("#### Suggested Additions")

    for addition in results["suggested_additions"]:
        with st.expander(addition["section"], expanded=True):
            st.markdown(addition["suggestion"])


def display_revisions_section(results):
    """Display suggested revisions"""
    st.markdown("#### Suggested Revisions")
    
    for revision in results["suggested_revisions"]:
        with st.expander(revision["section"], expanded=True):
            st.markdown(f"**Before:**\n\n {revision['before']}")
            st.markdown(f"**After:**\n\n {revision['after']}")


if __name__ == "__main__":
    main()