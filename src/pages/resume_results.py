import streamlit as st
from pathlib import Path
from homepage import render_header

results = Path( Path(__file__).parent.parent.parent, "results", "tailored_resume.json")

def main():
    render_header()

    if results:
        results_section()
    else:
        st.info("Tailor your resume for results!")


def results_section(): #ai_response: json
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