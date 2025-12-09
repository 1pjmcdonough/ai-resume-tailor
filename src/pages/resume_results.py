import streamlit as st
from homepage import render_header


def main():
    render_header()

    if "resume_edits" in st.session_state:
        results_section()
    else:
        st.info("Tailor your resume for results!")


def results_section():
    """Display the resume tailoring results in an organized format with tabs and download option."""
    
    st.markdown("### Overall Fit Assessment")
    st.info(st.session_state.resume_edits["fit_summary"])

    tab1, tab2, tab3 = st.tabs([
        "Keywords", 
        "Additions", 
        "Revisions"
        ])
    
    # Display keywords analysis in first tab
    with tab1:
        display_keywords_section(st.session_state.resume_edits)
    
    # Display suggested additions in second tab
    with tab2:
        display_additions_section(st.session_state.resume_edits)
    
    # Display suggested revisions in third tab
    with tab3:
        display_revisions_section(st.session_state.resume_edits)
    
    # Download button for summary report
    st.divider()
    st.download_button(
        label="⬇ Download Summary Report",
        data=generate_summary_report(st.session_state.resume_edits),
        file_name="resume_analysis_summary.txt",
        mime="text/plain",
        type="primary"
    )


def display_keywords_section(results):
    """Display extracted and missing keywords.
    
    Args:
        results (dict): The resume edits dictionary containing keyword information.
    """
    col1, col2 = st.columns(2)
    
    # Display found keywords in the left column
    with col1:
        extracted_keywords = results.get("extracted_keywords", [])
        st.markdown(f"#### Keywords Found")
        st.markdown(f"*Found {len(extracted_keywords)} Keyword(s) already in your resume*")
        
        if extracted_keywords:
            # Create styled HTML badges for each found keyword
            keywords_html = ""
            for keyword in extracted_keywords:
                keywords_html += f'<span style="background-color: #d4edda; color: #155724; padding: 4px 8px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 0.9em;">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)
    
    # Display missing keywords in the right column
    with col2:
        missing_keywords = results.get("missing_keywords", [])
        st.markdown(f"#### Keywords Missing")
        st.markdown(f"*Found {len(missing_keywords)} Keyword(s) to strengthen your resume*")
        
        if missing_keywords:
            # Create styled HTML badges for each missing keyword
            keywords_html = ""
            for keyword in missing_keywords:
                keywords_html += f'<span style="background-color: #f8d7da; color: #721c24; padding: 4px 8px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 0.9em;">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)


def display_additions_section(results):
    """Display suggested additions.
    
    Args:
        results (dict): The resume edits dictionary containing suggested additions.
    """
    additions = results.get("suggested_additions", [])
    
    if not additions:
        st.info("No additions suggested - your resume looks complete!")
        return
    
    st.markdown(f"#### Suggested Additions")
    st.markdown(f"*Found {len(additions)} suggestion(s) to strengthen your resume*")
    
    # Display each addition in an expandable section
    for addition in additions:
        with st.expander(f"{addition['section']}"):
            st.markdown(addition["suggestion"])

def display_revisions_section(results):
    """Display suggested revisions with side-by-side comparison.
    
    Args:
        results (dict): The resume edits dictionary containing suggested revisions.
    """
    revisions = results.get("suggested_revisions", [])
    
    if not revisions:
        st.info("No revisions suggested - your content looks great!")
        return
    
    st.markdown("#### Suggested Revisions")
    st.markdown(f"*Found {len(revisions)} revision(s) to improve your resume*")
    
    # Display each revision with before/after comparison
    for revision in revisions:
        with st.expander(f"{revision['section']}"):
            col1, col2 = st.columns(2)
            
            # Show current version in left column
            with col1:
                st.markdown("**🔴 Current Version:**")
                st.markdown(revision['before'])
            
            # Show suggested version in right column
            with col2:
                st.markdown("**🟢 Suggested Version:**")
                st.markdown(revision['after'])
            

def generate_summary_report(results):
    """Generate a text summary report of the resume analysis.
    
    Args:
        results (dict): The resume edits dictionary containing all analysis results.
    
    Returns:
        str: A formatted text report containing the complete analysis summary.
    """
    # Build the report header and overall fit section
    report = f"""RESUME ANALYSIS SUMMARY
======================

OVERALL FIT:
{results.get('fit_summary', 'No summary available')}

KEYWORDS ANALYSIS:
- Found Keywords: {len(results.get('extracted_keywords', []))}
- Missing Keywords: {len(results.get('missing_keywords', []))}

SUGGESTED ADDITIONS ({len(results.get('suggested_additions', []))}):
"""
    
    # Add each suggested addition to the report
    for i, addition in enumerate(results.get('suggested_additions', []), 1):
        report += f"\n{i}. {addition['section']}:\n   {addition['suggestion']}\n"
    
    # Add revisions section header
    report += f"\nSUGGESTED REVISIONS ({len(results.get('suggested_revisions', []))}):\n"
    
    # Add each suggested revision with before/after comparison
    for i, revision in enumerate(results.get('suggested_revisions', []), 1):
        report += f"\n{i}. {revision['section']}:\n   Before: {revision['before']}\n   After: {revision['after']}\n"
    
    return report


if __name__ == "__main__":
    main()