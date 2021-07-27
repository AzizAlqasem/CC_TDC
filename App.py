import streamlit as st
from gui import dataAQ_page
from gui import settings_page

st.set_page_config(
     page_title="Time Of Flight",
     page_icon="⏱",
     layout="wide",
     initial_sidebar_state= "auto"#"collapsed",
)


st.write("## Time of Flight Experiment")


select_pages = st.sidebar.selectbox(
    "Pages", ("DataAQ", "T-E Conversion", "Settings", "Test TDC","Help")
)


if select_pages == "DataAQ":
    dataAQ_page.main_page()

elif select_pages == "Settings":
    settings_page.main()

else:
    pass