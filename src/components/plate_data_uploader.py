import streamlit as st
import pandas as pd

from functions.select_raw_data import select_raw_data
from functions.get_file_information import get_file_information
from functions.get_plate_values import get_plate_values


def plate_data_uploader():
    if 'data' not in st.session_state:
        st.session_state.data = {}

    excel_file = st.file_uploader("Choose an Excel file:", type=['xlsx', 'xls'])
    if excel_file is None:
        st.info("Please upload an Excel file to get started.")
        st.session_state.data = {}
    
    else:
        excel_data = pd.ExcelFile(excel_file)
        raw_data = select_raw_data(excel_data)

        if raw_data is not None:
            file_info = get_file_information(raw_data)
            file_name = f'"{str(excel_file.name)}" ({file_info})'
            plate_values = get_plate_values(raw_data)

            st.subheader('Plate Map')
            st.write("Click on cells to edit:")  
            template = plate_values.astype(str)
            plate_map = st.data_editor(template, use_container_width=True, key='plate_map')

            st.subheader('Assay Type')
            assay_types = ['Bicinchoninic acid (BCA)']
            assay_type = st.selectbox('Select from drop-down:', assay_types)

            if st.button('Perform Protocol'):
                data = {
                    'file_name': file_name,
                    'plate_values': plate_values,
                    'plate_map': plate_map,
                    'assay_type': assay_type
                }
                st.session_state.data = data

    data = st.session_state.data

    return data