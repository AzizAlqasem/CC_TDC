import streamlit as st
import pandas as pd

from core.time_energy_conv import TEC


tec = TEC()

def main():
    st.write("### TOF to Energy conversion")
    hand_t = st.pyplot(tec.fig_t)
    hand_e = st.pyplot(tec.fig_e)

    # choose parametes
    t0 = st.slider("T0 (x10^-8)", min_value=-2.0, max_value=5.0, value=1.92, step=0.01)
    t0 = t0*1e-8
    L = st.slider("L (cm)", min_value=45.0, max_value=60.0, value=53.0, step=0.05)
    L = L/100
    shift = st.slider("Shift (ev)", min_value=-2.0, max_value=2.0, value=0.0, step=0.01)
    wavelength = st.number_input("Wavelength (nm)", value=700.0)
    
    # Load Data
    uploaded_file = st.sidebar.file_uploader("Choose a TOF csv file")
    if st.sidebar.button("Load Data"):
        if uploaded_file is not None:
            print("Uploading File ...")
            tec.load_data(uploaded_file)
            # Plot I(t)
            tec.line_t.set_data(tec.time, tec.count)
            tec.ax_t.set_xlim(tec.time.min(), tec.time.max())
            tec.ax_t.set_ylim(tec.count.min(), tec.count.max())
            hand_t.pyplot(tec.fig_t)
            st.write(pd.DataFrame(tec.get_file_header(), index=["Info"]).T)
        else:
            print('Error in upploading the file')
            print(uploaded_file)

    if tec.has_data:
        tec.update_vlines(wl=wavelength)

        # Plot I(E)
        tec.update_energy_line(t0=t0, L=L, shift=shift)

        hand_e.pyplot(tec.fig_e)

