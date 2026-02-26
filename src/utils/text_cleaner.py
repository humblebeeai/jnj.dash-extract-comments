from typing import Any

import pandas as pd


def normalize_text(text: Any, trim: bool = True) -> str:
    """
    Normalizes and cleans text data.

    Args:
        text (any): The input text or value.
        trim (bool): Whether to strip whitespace.

    Returns:
        str: Cleaned text.
    """
    if pd.isna(text):
        return ""

    s = str(text)

    # Replace common anomalies if needed (e.g., non-breaking spaces)
    s = s.replace("\xa0", " ")

    return s.strip() if trim else s


def concatenate_columns(
    row: pd.Series, columns: list[str], separator: str = " | "
) -> str:
    """
    Combines multiple columns into a single string for extraction.
    """
    parts = [normalize_text(row.get(c, "")) for c in columns]
    parts = [p for p in parts if p != ""]
    return separator.join(parts)
