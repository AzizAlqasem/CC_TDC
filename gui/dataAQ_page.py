import streamlit as st
from gui.dataAq import Main

main = Main()





def main_page():
    st.title("DataAQ Page")

    fc0, fc1, fc2 = st.beta_columns([1,4,3])

    with fc1:
        tof_hand = st.pyplot(main.tof.fig)
    with fc2:
        s_hand = st.pyplot(main.mtof_stream)
        h_hand = st.pyplot(main.mtof_hit)

    main.add_handler(tof_hand, s_hand, h_hand)

    if st.button("Run"):
        main.run()

    if st.button("Stop"):
        main.stop()

    if st.button("Save"):
        main.save()

    if st.button("Clear"):
        main.clear()
    
    if st.button("TDC_Connect"):
        main.TDC_connect()
    
    if st.button("TDC_Close"):
        main.TDC_close()

    if st.button("Reload"):
        main.reload()



    