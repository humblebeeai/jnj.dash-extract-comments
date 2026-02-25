import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Excel Concatenator", layout="wide")

st.title("Excel Column Concatenator")
st.write("Upload an Excel file, then choose the columns you want to concatenate. The app will create a new column and return an Excel file.")

uploaded = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

def safe_str(x, trim: bool = True) -> str:
    if pd.isna(x):
        return ""
    s = str(x)
    return s.strip() if trim else s

if uploaded:
    # Read workbook
    xls = pd.ExcelFile(uploaded)

    # Automatically select the first sheet
    sheet_name = xls.sheet_names[0]

    # Read the selected sheet
    df = pd.read_excel(xls, sheet_name=sheet_name)

    cols = list(df.columns)

    st.divider()
    st.subheader("Choose columns to concatenate")

    st.write("✅ **Choose the columns you want to concatenate (in order).**")

    selected_cols = st.multiselect(
        "Choose columns to concatenate:",
        options=cols,
        help="Select 1+ columns. The output will be joined using the separator you choose."
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        separator = st.text_input("Separator", value="/")

    with col2:
        new_col_name = st.text_input("New column name", value="combined")

    with col3:
        trim = st.checkbox("Trim whitespace", value=True)

    missing_policy = st.radio(
        "Missing values handling",
        ["skip empty values", "keep empty values"],
        horizontal=True
    )

    # ---------------------------
    # NEW: COLUMN MAPPING SECTION
    # ---------------------------

    st.divider()
    st.subheader("Choose columns to map")

    map_columns = st.multiselect(
        "Choose columns to map:",
        options=cols,
        help="Selected columns will be replaced with the mapping value."
    )

    map_value = "Mapped"

    # ---------------------------
    # GENERATE BUTTON
    # ---------------------------

    can_generate = len(selected_cols) >= 1

    if st.button("Generate output Excel", type="primary", disabled=not can_generate):

        out_df = df.copy()

        # Apply mapping first
        if map_columns:
            for col in map_columns:
                out_df[col] = map_value

        # Combine columns
        def combine_row(row):
            parts = [safe_str(row[c], trim=trim) for c in selected_cols]
            if missing_policy == "skip empty values":
                parts = [p for p in parts if p != ""]
            return separator.join(parts)

        out_df[new_col_name] = out_df.apply(combine_row, axis=1)

        st.success(f"Done! Created a new column: {new_col_name}")
        st.subheader("Preview (with concatenated column)")
        st.dataframe(out_df.head(20), use_container_width=True)

        # Write output Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            out_df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)

        st.download_button(
            label="Download Excel file",
            data=output,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Upload an Excel file to get started.")