import io

import pandas as pd
import streamlit as st

from src.config.settings import MAX_ROWS_PREVIEW


def render_preview(df: pd.DataFrame, title: str = "Data Preview"):
    """Renders a preview of the DataFrame."""
    st.write(f"**{title}**")
    st.dataframe(df.head(MAX_ROWS_PREVIEW), use_container_width=True)
    if len(df) > MAX_ROWS_PREVIEW:
        st.caption(f"Showing first {MAX_ROWS_PREVIEW} of {len(df)} rows.")


def render_download_button(
    excel_data: io.BytesIO, file_name: str = "extracted_data.xlsx"
):
    """Renders the download button for the processed Excel file."""
    st.download_button(
        label="Download Processed Excel",
        data=excel_data,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )
