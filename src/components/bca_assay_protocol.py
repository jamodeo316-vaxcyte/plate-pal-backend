import streamlit as st

from functions.get_assay_summary import get_assay_summary
from functions.get_group_results import get_group_results
from functions.fit_standard_curve import fit_standard_curve
from functions.plot_standard_curve import plot_standard_curve
from functions.get_concentrations import get_concentrations
from functions.get_results_table import get_results_table
from functions.get_results_summary import get_results_summary
from functions.get_assay_report import get_assay_report


def bca_assay_protocol(data):
    with st.spinner('Analyzing samples...'):
        data = get_assay_summary(data)
        data = get_group_results(data)
        data = fit_standard_curve(data)
        data = plot_standard_curve(data)
        data = get_concentrations(data)
        data = get_results_table(data)
        data = get_results_summary(data)
        data = get_assay_report(data)

    st.subheader('Standard Curve')
    r_squared = data['curve_fit']['r_squared']
    if r_squared < 0.98:
        st.warning(f'Poor standard curve fit. R-squared = {r_squared}')
    st.pyplot(data['curve_plot'])

    st.subheader('Results Table')
    st.dataframe(data['results_table'])

    st.download_button(
        label='Download Report',
        data=data['assay_report'],
        file_name="assay_report.pdf",
        mime="application/pdf"
    )