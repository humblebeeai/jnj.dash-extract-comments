# AGENTS.md - Agent Coding Guidelines

This document provides guidelines for agents working on this codebase.

## Project Overview

This is a Streamlit-based Excel column concatenator application. The app allows users to upload Excel files, select columns to concatenate, optionally map column values, and download the processed file.

- **Language**: Python 3.10+
- **Framework**: Streamlit 1.54.0
- **Dependencies**: pandas, openpyxl, streamlit

---

## Build & Run Commands

### Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run Streamlit app
streamlit run app.py

# Or with specific port
streamlit run app.py --server.port 8501
```

### Development Tools

```bash
# Install development dependencies
pip install pytest ruff black isort mypy

# Run linter (ruff)
ruff check .

# Format code (black + isort)
black .
isort .

# Type checking
mypy .

# Run tests (if tests exist)
pytest
pytest tests/                    # Run all tests
pytest tests/test_file.py        # Run specific test file
pytest tests/test_file.py::test_function  # Run specific test function
pytest -k "test_name"            # Run tests matching pattern
pytest --tb=short                # Shorter traceback format
```

---

## Code Style Guidelines

### General Principles

- Write clean, readable, and maintainable code
- Follow PEP 8 style guide for Python
- Keep functions focused and single-purpose (SRP)
- Use meaningful variable and function names

### Imports

Order imports in the following groups (separated by blank lines):

1. Standard library imports (`io`, `os`, `re`, etc.)
2. Third-party imports (`pandas`, `streamlit`, `numpy`, etc.)
3. Local application imports

Within each group, sort alphabetically:

```python
import io
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from main import utils
```

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines sparingly to separate logical sections
- One blank line at end of file

### Type Hints

Always use type hints for function parameters and return values:

```python
def safe_str(x, trim: bool = True) -> str:
    """Convert value to string with optional trimming."""
    if pd.isna(x):
        return ""
    s = str(x)
    return s.strip() if trim else s
```

Use `Optional` for potentially None values:

```python
from typing import Optional

def process_file(path: Optional[str] = None) -> pd.DataFrame:
    ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `uploaded_file`, `selected_cols` |
| Functions | snake_case | `safe_str()`, `combine_row()` |
| Classes | PascalCase | `ExcelProcessor`, `DataValidator` |
| Constants | UPPER_SNAKE_CASE | `MAX_ROWS`, `DEFAULT_SEPARATOR` |
| Private functions | _snake_case | `_internal_helper()` |

### Docstrings

Use Google-style docstrings for all public functions:

```python
def concatenate_columns(
    df: pd.DataFrame,
    columns: list[str],
    separator: str = "/"
) -> pd.DataFrame:
    """Concatenate specified columns into a new column.

    Args:
        df: Input DataFrame.
        columns: List of column names to concatenate.
        separator: String separator between concatenated values.

    Returns:
        DataFrame with new concatenated column.

    Raises:
        ValueError: If any column is not found in DataFrame.
    """
    ...
```

### Error Handling

- Use specific exception types rather than catching `Exception`
- Include meaningful error messages
- Handle errors gracefully with user-friendly messages in Streamlit

```python
try:
    df = pd.read_excel(uploaded, sheet_name=sheet_name)
except ValueError as e:
    st.error(f"Failed to read Excel file: {e}")
    return
```

### Streamlit-Specific Guidelines

- Use `st.set_page_config()` at the top of the app
- Use `st.divider()` for visual separation
- Use `st.columns()` for layout
- Use `st.session_state` for persisting state across reruns
- Provide helpful `help` text in widgets
- Use appropriate widget keys when needed

### File Organization

```
project/
├── app.py              # Main Streamlit entry point
├── src/                # Application source code
├── tests/              # Test files (when added)
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── AGENTS.md          # This file
```

---

## Testing Guidelines

When adding tests:

```bash
# Test file naming: test_<module_name>.py
tests/
├── test_app.py
└── utils/
    └── test_helpers.py
```

Example test structure:

```python
import pytest
import pandas as pd

def test_safe_str_trim():
    """Test string trimming functionality."""
    assert safe_str("  hello  ") == "hello"
    assert safe_str("  hello  ", trim=False) == "  hello  "

def test_safe_str_na():
    """Test handling of NA values."""
    assert safe_str(None) == ""
    assert safe_str(pd.NA) == ""
```

---

## Common Development Tasks

### Adding a new feature
1. Create a new branch: `git checkout -b feature/feature-name`
2. Make changes following code style guidelines
3. Run linter: `ruff check .`
4. Test locally: `streamlit run app.py`
5. Commit and push changes

### Debugging Streamlit issues
- Use `st.write()` or `st.dataframe()` to inspect variables
- Check browser console for JavaScript errors
- Use `st.cache_data` decorator for expensive operations (with TTL)

---

## Lint/Type Check Before Committing

Always run before committing:

```bash
ruff check .          # Lint
mypy .                # Type check (if configured)
```

Fix any issues reported before committing.
