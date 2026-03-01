import streamlit as st

from src.config.settings import APP_TITLE, OPENAI_API_KEY
from src.core.document_parser import extract_text_from_pdf
from src.core.excel_processor import ExcelProcessor
from src.core.llm_service import LLMService
from src.ui.column_selector import render_column_selection
from src.ui.file_upload import render_dataset_upload, render_description_upload
from src.ui.results_display import render_download_button, render_preview


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.write(
        "Extract structured data from clinical notes using AI and an uploaded definition document."
    )

    if not OPENAI_API_KEY:
        st.error("⚠️ OPENAI_API_KEY is missing. Please set it in your .env file.")
        st.stop()

    excel_processor = ExcelProcessor()

    # 1. Upload Dataset
    uploaded_dataset = render_dataset_upload()

    if not uploaded_dataset:
        st.info("Please upload an Excel dataset to begin.")
        st.stop()

    try:
        df = excel_processor.load_excel(uploaded_dataset)
        st.success(f"Loaded dataset with {len(df)} rows.")
        with st.expander("Preview Raw Data"):
            render_preview(df, "Raw Data Preview")
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        st.stop()

    st.divider()

    # 2. Column Selection
    notes_cols, target_cols = render_column_selection(df)

    st.divider()

    # 3. Upload Description
    uploaded_pdf = render_description_upload()

    st.divider()

    # Extraction Execution
    can_run = bool(uploaded_dataset and notes_cols and target_cols and uploaded_pdf)

    st.subheader("4. Execute Extraction")
    if not can_run:
        st.warning("Please complete all steps above to enable extraction.")

    if st.button("Extract Data", type="primary", disabled=not can_run):
        with st.spinner("Initializing AI Service..."):
            llm_service = LLMService()

            # Step A: Parse PDF
            st.write("📄 Parsing description document...")
            try:
                pdf_text = extract_text_from_pdf(uploaded_pdf)
            except Exception as e:
                st.error(f"Failed to read PDF: {e}")
                st.stop()

            # Step B: Extract Schema
            st.write("🧠 Extracting target column schemas...")
            try:
                schema = llm_service.extract_column_schema(pdf_text, target_cols)
                with st.expander("View Extracted Schema (JSON)"):
                    st.json(schema)
            except Exception as e:
                st.error(f"Failed to extract schema: {e}")
                st.stop()

            # Step C: Prepare Data
            st.write("⚙️ Preparing notes column...")
            df_prepared = excel_processor.prepare_notes_column(df, notes_cols)

            # Step D: Extract Row Data
            st.write("🚀 Extracting row data (This may take a while)...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            def extraction_callback(row_text: str):
                return llm_service.extract_row_data(row_text, schema, target_cols)

            # Using a custom loop for progress bar updates instead of the generic apply_extraction
            # to give better user feedback in Streamlit.

            df_out = df_prepared.copy()
            for col in target_cols:
                if col not in df_out.columns:
                    df_out[col] = None

            total_rows = len(df_out)
            notes_col_name = "_temp_notes"

            for i, (idx, row) in enumerate(df_out.iterrows()):
                status_text.text(f"Processing row {i + 1} of {total_rows}...")
                progress_bar.progress((i + 1) / total_rows)

                row_text = str(row.get(notes_col_name, "") or "").strip()
                if row_text:
                    try:
                        extracted = extraction_callback(row_text)
                        for col in target_cols:
                            if col in extracted and extracted[col] is not None:
                                df_out.at[idx, col] = extracted[col]
                    except Exception as e:
                        st.error(f"Error on row {i+1}: {e}")

            # Clean up temp column
            if notes_col_name in df_out.columns:
                df_out = df_out.drop(columns=[notes_col_name])

            status_text.text("Extraction complete!")

            st.success("✅ Data extraction finished successfully!")

            st.divider()
            st.subheader("5. Results")
            render_preview(df_out, "Processed Data Preview")

            try:
                excel_bytes = excel_processor.export_to_excel(df_out)
                render_download_button(excel_bytes)
            except Exception as e:
                st.error(f"Failed to create download file: {e}")
