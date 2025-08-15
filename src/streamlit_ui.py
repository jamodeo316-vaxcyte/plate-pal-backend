import streamlit as st

from components.plate_data_uploader import plate_data_uploader
from components.bca_assay_protocol import bca_assay_protocol


def streamlit_ui():
    st.set_page_config(page_title="Plate Pal")
    st.title("Plate Pal")
    data = plate_data_uploader()
    if data:
        if data['assay_type'] == 'Bicinchoninic acid (BCA)':
            bca_assay_protocol(data)
