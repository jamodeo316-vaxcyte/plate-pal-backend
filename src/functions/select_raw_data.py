import streamlit as st


def select_raw_data(excel_data):
    if len(excel_data.sheet_names) > 1:
        with st.expander("Click to select your raw data"):
            selections = []
            for sheet_name in excel_data.sheet_names:
                selected = st.checkbox(sheet_name)
                selections.append(int(selected))
                sheet_data = excel_data.parse(sheet_name)
                st.dataframe(sheet_data)
            if 1 in selections:
                idx = selections.index(1)
                sheet_name = excel_data.sheet_names[idx]
                raw_data = excel_data.parse(sheet_name)
            else:
                raw_data = None
    else:
        raw_data = excel_data.parse(excel_data.sheet_names[0])

    return raw_data
