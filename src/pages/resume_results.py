import streamlit as st
import json
from pathlib import Path
from homepage import render_header


def main():
    render_header()

    if "resume_edits" in st.session_state:
        results_section()
    else:
        st.info("Tailor your resume for results!")


def results_section():
    """Display the resume tailoring results in an organized format"""
    st.markdown("## 📄 Resume Tailoring Results")
    
    try:
        # Parse the JSON response
        results = json.loads(st.session_state.resume_edits)
        
        # Display fit summary at the top
        if "fit_summary" in results:
            st.markdown("### 🎯 Overall Fit Assessment")
            st.info(results["fit_summary"])
        
        # Create tabs for different result sections
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 Keywords", "➕ Additions", "✏️ Revisions", "📊 Analysis"])
        
        with tab1:
            display_keywords_section(results)
        
        with tab2:
            display_additions_section(results)
        
        with tab3:
            display_revisions_section(results)
        
        with tab4:
            display_analysis_section(results)
            
    except json.JSONDecodeError:
        # If the response is not valid JSON, display as plain text
        st.markdown("### Raw Results")
        st.text_area("Response", value=st.session_state.resume_edits, height=400, disabled=True)
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")


def display_keywords_section(results):
    """Display extracted and missing keywords"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Extracted Keywords")
        if "extracted_keywords" in results and results["extracted_keywords"]:
            for keyword in results["extracted_keywords"]:
                st.markdown(f"- {keyword}")
        else:
            st.info("No keywords extracted")
    
    with col2:
        st.markdown("#### ❌ Missing Keywords")
        if "missing_keywords" in results and results["missing_keywords"]:
            for keyword in results["missing_keywords"]:
                st.markdown(f"- {keyword}")
        else:
            st.success("No missing keywords identified")


def display_additions_section(results):
    """Display suggested additions"""
    st.markdown("#### 💡 Suggested Additions")
    
    if "suggested_additions" in results and results["suggested_additions"]:
        for addition in results["suggested_additions"]:
            with st.expander(f"📝 {addition.get('section', 'Section')}", expanded=False):
                st.markdown(f"**Suggestion:** {addition.get('suggestion', 'No suggestion provided')}")
    else:
        st.info("No additions suggested")


def display_revisions_section(results):
    """Display suggested revisions"""
    st.markdown("#### ✏️ Suggested Revisions")
    
    if "suggested_revisions" in results and results["suggested_revisions"]:
        for revision in results["suggested_revisions"]:
            with st.expander(f"📝 {revision.get('section', 'Section')}", expanded=False):
                st.markdown("**Before:**")
                st.text(revision.get('before', 'No before text provided'))
                st.markdown("**After:**")
                st.text(revision.get('after', 'No after text provided'))
    else:
        st.info("No revisions suggested")


def display_analysis_section(results):
    """Display additional analysis information"""
    st.markdown("#### 📊 Detailed Analysis")
    
    # Show all available keys for debugging/development
    st.markdown("**Available Data Fields:**")
    for key in results.keys():
        if key not in ["fit_summary", "extracted_keywords", "missing_keywords", "suggested_additions", "suggested_revisions"]:
            st.markdown(f"- **{key}:** {str(results[key])}")
    
    # Display raw JSON for developers
    with st.expander("🔧 Raw JSON Data", expanded=False):
        st.json(results)


if __name__ == "__main__":
    main()