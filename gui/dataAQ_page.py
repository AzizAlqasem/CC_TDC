import streamlit as st
from gui.dataAQ import Main
from time import sleep
import os

st.columns = st.beta_columns
st.sidebar.columns = st.sidebar.beta_columns

main = Main()



def main_page():
    # First Row: Figures
    fc1, fc2 = st.columns([5,3])
    with fc1:
        tof_hand = st.pyplot(main.tof.fig)
    with fc2:
        s_hand = st.pyplot(main.mtof_stream.fig)
        h_hand = st.pyplot(main.mtof_hit.fig)
    # Tot avg hit
    avg_hits = fc2.empty()
    txt = ""
    for name, avh in main.dcounter.get_tot_avg_hit(last=2):
        txt += f"{name}: Average hit/shot  =  {round(avh,3)}\n"
    avg_hits.write(txt)
    # Tot Laser shot
    laser_shots = fc2.empty()
    laser_shots.write(f"Total Laser shots  =  {main.dcounter.tot_laser_shot}\n")


    # Second Row: Fig settings
    sc0, sc1, _,  sc2 = st.columns([2, 6, 1, 6])
    sc3, sc4, sc5, sc6 = st.columns([1, 3, 2, 4])
    # y-scale
    yscale = sc0.radio("Y-scale",("linear", "log"))
    main.adj_y_scale(yscale)

    # x and y lim
    x_lim = sc1.slider("X-lim", min_value=0.0, max_value=400.0, value=(0.0,100.0), step=0.5)
    y_lim = sc2.slider("Y-lim", min_value=1e-6, max_value=1.0, value=(1e-6,1.0), step=5e-4)
    main.adj_xlim(x_lim)
    main.adj_ylim(y_lim)

    # Max laser shot
    max_laser_shot = sc4.number_input("Max. Laser Shots (K)", value = 1000)

    # Update rate (delay) (max = 1 sec)
    update_delay = sc5.number_input("Update delay (sec)", value=1)
    # Show Prev data
    if sc3.checkbox("P.D."):
        main.tof.show_prev_arr(True)
    else:
        main.tof.show_prev_arr(False)

    # Power:
    power_ang = sc6.slider("Motor Controller (Angle)", min_value=0, max_value=360, value=0, step=1)

    # Side bar: Controls and status
    st.sidebar.write("### CC-TDC")
    sb_0, sb_1, sb_2 = st.sidebar.columns([1,1,1])

    st.sidebar.write("### Controol")
    _,sb0, sb1, _ = st.sidebar.columns([1,2,2,1])
    _,sb2, sb3, _ = st.sidebar.columns([1,2,2,1])

    if sb0.button("Run"):
        main.run()
    
    if sb1.button("Stop"):
        main.stop()

    if sb3.button("Clear"):
        main.clear()
    
    if sb_0.button("Connect"):
        main.TDC_connect()
    
    if sb_1.button("Close"):
        main.TDC_close()

    if sb_2.button("Reload"):
        main.reload()

    # Theird Row: Experiment info
    inpcol1, inpcol2, inpcol3 = st.columns(3)
    inpcol4, inpcol5, inpcol6 = st.columns(3)
    proj = inpcol1.text_input('Project Name', 'He ATI')
    expr = inpcol2.text_input('Experiment Name', 'High int. 800nm')
    target_n = inpcol3.text_input('Target Name', 'He')
    pulse_energy = inpcol4.text_input('Pulse Energy', '1mJ')
    wl = inpcol5.text_input('Wavelength', '800 nm')
    pressure = inpcol6.text_input("Pressure (torr)", "10^-5")
    note = st.text_input('Note', 'Things are working great!')
    if sb2.button("Save"):
        try:
            os.makedirs(rf"../Projects/{proj}")
        except FileExistsError:
            pass
        save_file_path = rf"../Projects/{proj}/{expr}.csv"
        info = {
            "Project": proj,
            "Experiment": expr,
            "Target Name": target_n,
            "Pulse Energy": pulse_energy,
            "Wavelength": wl,
            "Pressure": pressure,
            "Note": note,
            "Columns": "Time (ns), TDC Count"
        }
        main.dcounter.save(save_file_path, info)


    # Update outputs:
    while main.is_running:
        tof_hand.pyplot(main.tof.fig)
        s_hand.pyplot(main.mtof_stream.fig)
        h_hand.pyplot(main.mtof_hit.fig)

        txt = ""
        for name, avh in main.dcounter.get_tot_avg_hit():
            txt += f"{name}: Average hit/shot  =  {round(avh,3)}\n"
        avg_hits.write(txt)
        laser_shots.write(f"Total Laser shots  =  {main.dcounter.tot_laser_shot}\n")
        sleep(update_delay)
    
    tof_hand.pyplot(main.tof.fig)
    s_hand.pyplot(main.mtof_stream.fig)
    h_hand.pyplot(main.mtof_hit.fig)