import streamlit as st
import docx
from pathlib import Path
from homepage import render_header


def main():
    render_header()

    st.info("Tailor your resume for results!")


if __name__ == "__main__":
    main()