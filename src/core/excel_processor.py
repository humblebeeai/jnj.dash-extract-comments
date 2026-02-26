import io
from typing import Callable, List, Optional

import pandas as pd

from src.utils.logger import get_logger
from src.utils.text_cleaner import concatenate_columns

logger = get_logger(__name__)


class ExcelProcessor:
    def __init__(self):
        pass

    def load_excel(
        self, file_stream: io.BytesIO, sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """Loads an Excel file into a pandas DataFrame."""
        try:
            xls = pd.ExcelFile(file_stream)
            sheet = sheet_name if sheet_name else xls.sheet_names[0]
            df = pd.read_excel(xls, sheet_name=sheet)
            logger.info(f"Successfully loaded {len(df)} rows from sheet '{sheet}'.")
            return df
        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}")
            raise ValueError(f"Failed to read Excel file: {e}")

    def prepare_notes_column(
        self,
        df: pd.DataFrame,
        source_columns: List[str],
        temp_col_name: str = "_temp_notes",
    ) -> pd.DataFrame:
        """
        Concatenates and cleans multiple source columns into a single temporary column for the LLM.
        """
        df_copy = df.copy()
        if not source_columns:
            df_copy[temp_col_name] = ""
            return df_copy

        df_copy[temp_col_name] = df_copy.apply(
            lambda row: concatenate_columns(row, source_columns), axis=1
        )
        return df_copy

    def apply_extraction(
        self,
        df: pd.DataFrame,
        notes_col: str,
        target_columns: List[str],
        extraction_fn: Callable,
    ) -> pd.DataFrame:
        """
        Iterates over the DataFrame, extracts data using the provided function, and populates target columns.

        Args:
            df: The DataFrame to process.
            notes_col: The column name containing the text to process.
            target_columns: The columns to populate.
            extraction_fn: A function that takes a string and returns a dict mapping column names to values.
        """
        df_out = df.copy()

        # Ensure target columns exist
        for col in target_columns:
            if col not in df_out.columns:
                df_out[col] = None

        total_rows = len(df_out)
        for i, (idx, row) in enumerate(df_out.iterrows()):
            logger.debug(f"Processing row {i + 1}/{total_rows}")
            row_text = str(row.get(notes_col, "") or "").strip()

            if not row_text:
                continue

            try:
                extracted_data = extraction_fn(row_text)
                for col in target_columns:
                    if col in extracted_data and extracted_data[col] is not None:
                        df_out.at[idx, col] = extracted_data[col]
            except Exception as e:
                logger.error(f"Failed to extract row {idx}: {e}")

        return df_out

    def export_to_excel(self, df: pd.DataFrame) -> io.BytesIO:
        """Exports the DataFrame to an in-memory Excel file."""
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Processed_Data")
            output.seek(0)
            return output
        except Exception as e:
            logger.error(f"Failed to export Excel file: {e}")
            raise ValueError(f"Failed to export Excel file: {e}")
