import streamlit as st
from settings.settings import settings

st.columns = st.beta_columns

# Settings will change the temp variables
# Default variables are change by the .txt file.

def main():
    st.write("## Settings")

    st.write("### TDC Settings")
    col1, col4, col5, col6, col7 = st.columns(5)
    tdc_n = col1.radio('TDC Model', ['TDC 2228A','TDC 4208','Dual'], index=0)
    if tdc_n == 'Dual':
        value = ['TDC2228A','TDC4208']
    else:
        value = [tdc_n.replace(' ', '')]  # one item and remove space
    settings.set_setting('target_modules', value)

    for tdc in value:
        slot_n = col4.text_input(f'{tdc} Slot Number', '19',  max_chars=2)
        settings.set_setting('slot_number', slot_n, target=tdc)

    cc_time_out = col5.text_input('CC-USB Time Out (ms)', '100')
    settings.set_setting('cc_time_out_ms', cc_time_out)

    cc_trig_delay_us = col6.text_input('CC-USB Trigger Delay (us)', '100')
    settings.set_setting('trig_delay_us', cc_trig_delay_us)

    auto_save_delay = col7.text_input('DAQ Auto Save Delay (# of loops)', '10')
    settings.set_setting('auto_save_delay', auto_save_delay)

    st.write("All settings:")
    st.json(settings.settings_dict)


"""#The two lines below add complexity, so they will be left for future update 
reso = col2.radio('TDC Resolution (PICSEC)', [50, 100, 250], help="A manual switch on the TDC must be turend first")
bit_dy_range = col3.radio('Bit Daynamic Range', [11, 8], help="A manual switch on the TDC must be turend first")

st.write("\n-----------\n")
st.write("### Calculations")
st.write('\n')
st.write("#### Bins to Time Conversion (calibration)")       
st.latex(r''' Time [ns] = Slope * ChannelNumber + OffSet''')
cc1, cc2, cc3 = st.columns(3)
ch_n = cc1.text_input('Channel Number', '0')
slop = cc2.text_input('Slope (ns/ch)', '0.047')
off_set = cc3.text_input('Off Set (ns)', '5.12')
"""

