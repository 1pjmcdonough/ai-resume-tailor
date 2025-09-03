import streamlit as st
import json
import io
import base64
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from pathlib import Path
from homepage import render_header


def main():
    render_header()

    with open(Path(Path(__file__).parent.parent.parent, "response_history", "McDonough_Phil_J.pdf_for_job_desc.pdf", "cover_letter.txt")) as f:
        st.session_state.cover_letter = json.loads(f.read())

    if st.session_state.cover_letter:
        tab1, tab2 = st.tabs(["Preview", "Edit"])
        
        with tab1:
            display_preview(st.session_state.cover_letter)
            download_cl()
        
        with tab2:
            edited_data = create_editable_form(st.session_state.cover_letter)
            
            # Update preview button
            if st.button("🔄 Update Preview", type="primary"):
                st.session_state.cover_letter = edited_data
                st.success("✅ Cover letter updated! Check the Preview tab.")    
    else:
        st.info("Please generate a cover letter first.")


def display_preview(data):
    st.subheader("Preview Cover Letter")

    st.write(data["intro_paragraph"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Your Requirements")
    with col2:
        st.markdown("##### My Qualifications")
    st.divider()
    
    for pair in data["t_table"]:
        col1, col2 = st.columns(2)
        with col1:
            st.write(pair["job_requirement"])
        with col2:
            st.write(pair["my_qualification"])
        st.divider()

    st.write(data["closing_paragraph"])


def download_cl():    
    doc_bytes = create_ttable_cover_letter_bytes(st.session_state.cover_letter)
        
    st.download_button(
        label="⬇ Click here to download",
        data=doc_bytes,
        file_name="cover_letter.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary"
    )

def create_ttable_cover_letter_bytes(json_data):
    """
    Create a T-table formatted cover letter from JSON data and return as bytes
    
    Args:
        json_data (dict or str): Either a dictionary or JSON string containing the cover letter data
    
    Returns:
        bytes: The document as bytes for download
    """
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    intro_para = doc.add_paragraph()
    intro_para.add_run(json_data["intro_paragraph"])
    
    doc.add_paragraph()
    
    if json_data["t_table"]:
        table = doc.add_table(rows=len(json_data['t_table'])+1, cols=2) # +1 for the header
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        table.columns[0].width = Inches(3.5) # 3.2
        table.columns[1].width = Inches(3.5) # 3.2
        
        header_cells = table.rows[0].cells
        header_cells[0].text = "Your Requirements"
        header_cells[1].text = "My Qualifications"
        
        for cell in header_cells:
            cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
        for i, item in enumerate(json_data['t_table'], 1):
            row_cells = table.rows[i].cells
            row_cells[0].text = item['job_requirement']
            row_cells[1].text = item['my_qualification']
            
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    doc.add_paragraph() # add some space after the table
    
    closing_para = doc.add_paragraph()
    closing_para.add_run(json_data['closing_paragraph'])
    
    doc_buffer = io.BytesIO()
    doc.save(doc_buffer)
    doc_buffer.seek(0)
    
    return doc_buffer.getvalue()


def create_editable_form(initial_data):
    """Create an editable form for the cover letter data"""
    st.subheader("✏️ Edit Your Cover Letter")
    
    # Initialize session state if not exists
    if 'st.session_state.cover_letter' not in st.session_state:
        st.session_state.cover_letter = initial_data.copy()
    
    data = st.session_state.cover_letter
    
    # Edit introduction
    st.markdown("**Introduction Paragraph:**")
    data['intro_paragraph'] = st.text_area(
        "Introduction", 
        value=data['intro_paragraph'],
        height=100,
        key="intro_edit"
    )
    
    # Edit T-table entries
    st.markdown("**Requirements vs Qualifications Table:**")
    
    # Button to add new row
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Add Row"):
            data['t_table'].append({
                'job_requirement': '',
                'my_qualification': ''
            })
            st.rerun()
    
    # Edit existing rows
    rows_to_delete = []
    for i, item in enumerate(data['t_table']):
        st.markdown(f"**Row {i+1}:**")
        col1, col2, col3 = st.columns([2, 2, 0.3])
        
        with col1:
            item['job_requirement'] = st.text_area(
                f"Job Requirement {i+1}",
                value=item['job_requirement'],
                height=80,
                key=f"req_{i}"
            )
        
        with col2:
            item['my_qualification'] = st.text_area(
                f"My Qualification {i+1}",
                value=item['my_qualification'],
                height=80,
                key=f"qual_{i}"
            )
        
        with col3:
            st.write("")  # Space for alignment
            if st.button("🗑️", key=f"delete_{i}", help="Delete this row"):
                rows_to_delete.append(i)
    
    # Delete marked rows
    for i in reversed(rows_to_delete):
        del data['t_table'][i]
        st.rerun()
    
    st.divider()
    
    # Edit closing
    st.markdown("**Closing Paragraph:**")
    data['closing_paragraph'] = st.text_area(
        "Closing", 
        value=data['closing_paragraph'],
        height=100,
        key="closing_edit"
    )
    
    return data


if __name__ == "__main__":
    main()