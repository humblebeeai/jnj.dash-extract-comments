from typing import List, Tuple

import pandas as pd
import streamlit as st


def render_column_selection(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Renders UI for selecting the source (notes) columns and defining target columns.
    """
    st.subheader("2. Define Extraction Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Source Columns**")
        all_columns = df.columns.tolist()
        notes_cols = st.multiselect(
            "Select columns containing notes to process:",
            options=all_columns,
            help="If multiple columns are selected, they will be combined.",
        )

    with col2:
        st.write("**Target Columns**")
        all_columns = df.columns.tolist()

        target_cols = st.multiselect(
            "Select target columns to populate with extracted data:",
            options=all_columns,
            help="Select the existing columns in your dataset that you want the LLM to populate. These names MUST match the fields defined in your PDF.",
        )

    return notes_cols, target_cols
