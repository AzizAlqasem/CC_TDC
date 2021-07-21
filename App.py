import streamlit as st
from gui import dataAQ_page

st.title("Time OF Flight Experiment")


select_pages = st.sidebar.selectbox(
    "Pages", ("DataAQ", "T-E Conversion", "Settings", "Test TDC","Help")
)


if select_pages == "DataAQ":
    dataAQ_page.main()