import streamlit as st
from homepage import render_header


def main():
    render_header()

    if "resume_edits" in st.session_state:
        results_section()
    else:
        st.info("Tailor your resume for results!")


def results_section():
    """Display the resume tailoring results in an organized format"""
    
    # Overall fit assessment with better styling
    st.markdown("### Overall Fit Assessment")
    st.info(st.session_state.resume_edits["fit_summary"])

    # Enhanced tabs with better organization
    tab1, tab2, tab3 = st.tabs([
        "Keywords", 
        "Additions", 
        "Revisions"
        ])
    
    with tab1:
        display_keywords_section(st.session_state.resume_edits)
    
    with tab2:
        display_additions_section(st.session_state.resume_edits)
    
    with tab3:
        display_revisions_section(st.session_state.resume_edits)
    
    st.divider()
    st.download_button(
        label="⬇ Download Summary Report",
        data=generate_summary_report(st.session_state.resume_edits),
        file_name="resume_analysis_summary.txt",
        mime="text/plain",
        type="primary"
    )


def display_keywords_section(results):
    """Display found and missing keywords with better formatting"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        found_keywords = results.get("found_keywords", [])
        st.markdown(f"#### Keywords Found")
        st.markdown(f"*Found {len(found_keywords)} Keyword(s) already in your resume*")
        
        if found_keywords:
            keywords_html = ""
            for keyword in found_keywords:
                keywords_html += f'<span style="background-color: #d4edda; color: #155724; padding: 4px 8px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 0.9em;">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)
    
    with col2:
        missing_keywords = results.get("missing_keywords", [])
        st.markdown(f"#### Keywords Missing")
        st.markdown(f"*Found {len(missing_keywords)} Keyword(s) to strengthen your resume*")
        
        if missing_keywords:
            keywords_html = ""
            for keyword in missing_keywords:
                keywords_html += f'<span style="background-color: #f8d7da; color: #721c24; padding: 4px 8px; margin: 2px; border-radius: 12px; display: inline-block; font-size: 0.9em;">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)


def display_additions_section(results):
    """Display suggested additions with priority and action buttons"""
    additions = results.get("suggested_additions", [])
    
    if not additions:
        st.info("No additions suggested - your resume looks complete!")
        return
    
    st.markdown(f"#### Suggested Additions")
    st.markdown(f"*Found {len(additions)} suggestion(s) to strengthen your resume*")
        
    for addition in additions:
        with st.expander(f"{addition['section']}"):
            st.markdown(addition["suggestion"])

def display_revisions_section(results):
    """Display suggested revisions with side-by-side comparison"""
    revisions = results.get("suggested_revisions", [])
    
    if not revisions:
        st.info("No revisions suggested - your content looks great!")
        return
    
    st.markdown("#### Suggested Revisions")
    st.markdown(f"*Found {len(revisions)} revision(s) to improve your resume*")
    
    for revision in revisions:
        with st.expander(f"{revision['section']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔴 Current Version:**")
                st.markdown(revision['before'])
            
            with col2:
                st.markdown("**🟢 Suggested Version:**")
                st.markdown(revision['after'])
            

def generate_summary_report(results):
    """Generate a text summary report"""
    report = f"""RESUME ANALYSIS SUMMARY
======================

OVERALL FIT:
{results.get('fit_summary', 'No summary available')}

KEYWORDS ANALYSIS:
- Found Keywords: {len(results.get('found_keywords', []))}
- Missing Keywords: {len(results.get('missing_keywords', []))}

SUGGESTED ADDITIONS ({len(results.get('suggested_additions', []))}):
"""
    
    for i, addition in enumerate(results.get('suggested_additions', []), 1):
        report += f"\n{i}. {addition['section']}:\n   {addition['suggestion']}\n"
    
    report += f"\nSUGGESTED REVISIONS ({len(results.get('suggested_revisions', []))}):\n"
    
    for i, revision in enumerate(results.get('suggested_revisions', []), 1):
        report += f"\n{i}. {revision['section']}:\n   Before: {revision['before']}\n   After: {revision['after']}\n"
    
    return report


if __name__ == "__main__":
    main()