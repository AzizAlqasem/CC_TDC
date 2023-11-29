import streamlit as st
from gui.dataAQ import Main
from time import sleep
import os
import numpy as np

st.columns = st.beta_columns
st.sidebar.columns = st.sidebar.beta_columns

main = Main()



def main_page():
    # First Row: Figures
    fc1, fc2 = st.columns([4,1])
    with fc1:
        tof_hand = st.pyplot(main.tof.fig)
    with fc2:
       # s_hand = st.pyplot(main.mtof_stream.fig)
        # st.text("."+"\n"*+".")
        st.subheader("Average hit/shot")
        h_hand = st.pyplot(main.mtof_hit.fig)
    # Tot avg hit
    avg_hits1 = fc2.empty()
    # avg_hits2 = fc2.empty()
    avh_list = main.dcounter.get_tot_avg_hit(last=10)
    avh1 = avh_list[0][1] # TDC1
    # avh2 = avh_list[1][1] # TDC2
    avg_hits1.write(f"TDC1: {round(avh1,3)}")
    # avg_hits2.write(f"TDC2: {round(avh2,3)}")

    # Tot Laser shot
    laser_shots = fc2.empty()
    laser_shots.write(f"Total Laser shots:  {main.dcounter.tot_laser_shot}")


    # Second Row: Fig settings
    sc0, sc1, _,  sc2 = st.columns([2, 6, 1, 6])
    sc3, sc4, sc5, sc6, sc7 = st.columns([1, 2, 2, 2, 2])
    # y-scale
    yscale = sc0.radio("Y-scale",("log","linear"))
    main.adj_y_scale(yscale)

    # x and y lim
    x_lim = sc1.slider("X-lim", min_value=0, max_value=50000, value=(0,40000), step=1000)
    y_lim = sc2.slider("Y-lim", min_value=0, max_value=-9, value=(-4,0), step=1)
    main.adj_xlim(x_lim)
    y_lim=list(y_lim)
    y_lim[0] = 10**(y_lim[0])
    y_lim[1] = 10**(y_lim[1])
    main.adj_ylim(y_lim)

    # Max laser shot
    max_laser_shot = int(sc4.text_input("Max. Laser Shots (K)", "10000"))

    # Update rate (delay) (max = 1 sec)
    update_delay = sc5.number_input("Update delay (sec)", value=1)

    # Show Prev data
    if sc3.checkbox("P.D."):
        main.tof.show_prev_arr(True)
    else:
        main.tof.show_prev_arr(False)

    if sc3.checkbox("Live"):
        main.live_plot = True
    else:
        main.live_plot = False

    # Power:
    # power_ang = sc6.slider("Motor Controller (Angle)", min_value=0, max_value=360, value=0, step=1)

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
        main.is_scanning = False # Also stop scanning

    if sb3.button("Clear"):
        main.clear()

    if sb_0.button("Connect"):
        main.TDC_connect()

    if sb_1.button("Close"):
        main.TDC_close()

    if sb_2.button("Reload"):
        main.reload()

    st.sidebar.write("### Scan")
    sbc_0, sbc_1, sbc_2 = st.sidebar.columns([1,1,1])
    _,sbc_3, sbc_4, sbc_5, _ = st.sidebar.columns([1,2,2,2,1])
    # Motor position:
    motor_pos = sc6.number_input("Motor Position (deg)", value=0.0, step=0.5)
    motor_pos_offset = sc7.number_input("Offset (deg)", value=0.0, step=0.1)
    if sbc_3.button("Move"):
        main.current_motor_pos = motor_pos
        main.motor.move_to((main.current_motor_pos+motor_pos_offset) * main.STEP_SIZE_PER_DEGREE) # Convert to step size known by motor
    scan_start = int(sbc_0.text_input("Start", "0"))
    scan_end = int(sbc_1.text_input("End", "900"))
    scan_step = int(sbc_2.text_input("Step", "50"))
    if sbc_4.button("Scan"):
        main.is_scanning = True
        main.scan_angles = list(range(scan_start, scan_end+1, scan_step))
        # Randomize angles
        np.random.shuffle(main.scan_angles)
        main.current_motor_pos = main.scan_angles.pop(0)/10
        main.motor.move_to((main.current_motor_pos+motor_pos_offset) * main.STEP_SIZE_PER_DEGREE)
        main.run()
        sleep(4) # Wait for motor to move
        main.clear() # Clear buffer from previous scan (angle)
        # For LIED round scan (Temp)
        main.round_counter = 1

    if sbc_5.button("Resume"):
        main.is_scanning = True
        main.run()


    # Theird Row: Experiment info
    inpcol1, inpcol2, inpcol3 = st.columns(3)
    inpcol4, inpcol5, inpcol6 = st.columns(3)
    proj = inpcol1.text_input('Project Name', 'He ATI')
    expr = inpcol2.text_input('Experiment Name', 'High int. 800nm')
    target_n = inpcol3.text_input('Target Name', 'He')
    pulse_energy = inpcol4.text_input('Power (mW)', '50')
    wl = inpcol5.text_input('Wavelength (nm)', '800')
    pressure = inpcol6.text_input("Pressure (torr)", "1E-7")
    note = st.text_input('Note', 'Things are working great!')
    info = {
            "Project": proj,
            "Experiment": expr,
            "Target Name": target_n,
            "Power (mW)": pulse_energy,
            "Wavelength (nm)": wl,
            "Pressure (torr)": pressure,
            "Angle (deg)": main.current_motor_pos,
            "Note": note,
            "Columns": "Time (ns), TDC Count"}
    if sb2.button("Save"):
        try:
            os.makedirs(rf"../Projects/{proj}")
        except FileExistsError:
            pass
        save_file_path = rf"../Projects/{proj}/{expr}.csv"
        main.dcounter.save(save_file_path, info)


    # Update outputs:
    while main.is_running:
        tot_laser_shot = main.dcounter.tot_laser_shot
        if tot_laser_shot >= max_laser_shot*1000:
            # print(tot_laser_shot, max_laser_shot*1000)
            print("Max laser shot reached: ", tot_laser_shot, max_laser_shot*1000)
            main.stop()
            if main.is_scanning:
                # Save data
                try:
                    os.makedirs(rf"../Projects/{proj}")
                except FileExistsError:
                    pass
                # ---- specific to HWP and LIED
                # ang_zero = 44.2 # This is the HWP angle that make the polarization angle horizontal
                # ang = main.current_motor_pos # This is the HWP angle
                # angle_from_horizontal = ang - ang_zero
                # pol_ang = 2 * angle_from_horizontal # convert from HWP to Polarization angle
                # pol_ang_txt = str(int(pol_ang)).zfill(2)
                # ---- END
                pol_ang_txt = main.current_motor_pos
                save_file_path = rf"../Projects/{proj}/{expr}{main.round_counter}_ang{pol_ang_txt}.csv"
                # update angle in info dict
                info["Angle (deg)"] = pol_ang_txt
                info["Experiment"] = f"{expr}{main.round_counter}_ang{pol_ang_txt}"
                main.dcounter.save(save_file_path, info)
                print("Data saved to: ", save_file_path)
                # Change motor angle, if not at the end
                if main.scan_angles:
                    main.current_motor_pos = main.scan_angles.pop(0)/10
                    print("Moving to next angle: ", main.current_motor_pos)
                    print("Remaining angles: ", main.scan_angles)
                    main.motor.move_to(main.current_motor_pos * main.STEP_SIZE_PER_DEGREE) # Convert to step size known by motor
                else: # Scan finished
                    ### original
                    # main.is_scanning = False
                    # print("Scan finished!")
                    # break
                    ### end original

                    ### for LIED round scan (temp)
                    print("Scan finished for round: ", main.round_counter)
                    main.round_counter += 1
                    main.scan_angles = list(range(scan_start, scan_end+1, scan_step))
                    # Randomize angles
                    np.random.shuffle(main.scan_angles)
                    main.current_motor_pos = main.scan_angles.pop(0)/10
                    main.motor.move_to((main.current_motor_pos+motor_pos_offset) * main.STEP_SIZE_PER_DEGREE)
                # Run again
                main.run()
                sleep(4) # Wait for motor to move
                main.clear() # Clear buffer from previous scan (angle)

        if main.live_plot:
            tof_hand.pyplot(main.tof.fig)
            #s_hand.pyplot(main.mtof_stream.fig)
            h_hand.pyplot(main.mtof_hit.fig)
        avh_list = main.dcounter.get_tot_avg_hit(last=10)
        avh1 = avh_list[0][1] # TDC1
        # avh2 = avh_list[1][1] # TDC2
        avg_hits1.write(f"TDC1: {round(avh1,3)}")
        # avg_hits2.write(f"TDC2: {round(avh2,3)}")
        laser_shots.write(f"Total Laser shots  =  {tot_laser_shot}\n")

        sleep(update_delay)

    tof_hand.pyplot(main.tof.fig)
    #s_hand.pyplot(main.mtof_stream.fig)
    h_hand.pyplot(main.mtof_hit.fig)






# main.tof.fig.clf()
# Streamlit, version 0.84.1