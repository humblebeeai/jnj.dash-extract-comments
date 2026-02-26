import streamlit as st


def render_dataset_upload():
    """Renders the UI for uploading the main Excel dataset."""
    st.subheader("1. Upload Dataset")
    uploaded_file = st.file_uploader(
        "Upload your Excel dataset (.xlsx)", type=["xlsx"], key="dataset_uploader"
    )
    return uploaded_file


def render_description_upload():
    """Renders the UI for uploading the PDF description file."""
    st.subheader("3. Upload Description Document")
    st.write("Upload a PDF that defines the rules and fields to be extracted.")
    pdf_file = st.file_uploader(
        "Upload Description (.pdf)",
        type=["pdf"],
        key="pdf_uploader",
        help="This document is used by the LLM to understand what each column means.",
    )
    return pdf_file
