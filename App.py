import streamlit as st
from gui import dataAQ_page
from gui import settings_page
from gui import TEC_page

st.set_page_config(
     page_title="Time Of Flight",
     page_icon="⏱",
     layout="wide",
     initial_sidebar_state= "auto"#"collapsed",
)


# st.write("## Time of Flight Experiment")


# select_pages = st.sidebar.selectbox(
#     "Pages", ("DataAQ", "Settings", "T-E Conversion", "Help")
# )

select_pages = st.sidebar.selectbox(
    "Pages", ("DataAQ", "Help")
)

if select_pages == "DataAQ":
    dataAQ_page.main_page()

elif select_pages == "Settings":
    settings_page.main()

elif select_pages == "T-E Conversion":
    TEC_page.main()

else:
    pass