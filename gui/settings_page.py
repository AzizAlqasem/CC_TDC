import streamlit as st



def main():
    st.write("## Settings")

    st.write("### TDC Settings")
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    tdc_n = col1.radio('TDC Model', ['TDC 2228A','TDC 4208','Dual'])
    slot_n = col4.text_input('Module Slot Number', '20')
    reso = col2.radio('TDC Resolution (PICSEC)', [50, 100, 250], help="A manual switch on the TDC must be turend first")
    bit_dy_range = col3.radio('Bit Daynamic Range', [11, 8], help="A manual switch on the TDC must be turend first")
    cc_time_out = col5.text_input('CC-USB Time Out (ms)', '100')

    st.write("\n-----------\n")
    st.write("### Calculations")
    st.write('\n')
    st.write("#### Bins to Time Conversion (calibration)")       
    st.latex(r''' Time [ns] = Slope * ChannelNumber + OffSet''')
    cc1, cc2, cc3 = st.beta_columns(3)
    ch_n = cc1.text_input('Channel Number', '0')
    slop = cc2.text_input('Slope (ns/ch)', '0.047')
    off_set = cc3.text_input('Off Set (ns)', '5.12')

