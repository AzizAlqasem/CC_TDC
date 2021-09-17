import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class Data():

    def __init__(self, pth: str):
        self.file = pth
        data = np.load(self.file)  # load raw time of flight data
        self.T = data[0]  # time bins
        self.elec = data[1]  # electron counts per time bin

    def t2E(self, L=0.53, t0=1.92e-8):
        """
        converting time to energy
        L is the TOF length in meters
        t0 is the time zero.
        """
        m = 9.1093837015 * 10**-31  # electon mass
        e = 1.602176634 * 10**-19  # electron charge

        # get actual time of flight (remove t0 delays)
        T0 = self.T.copy()
        T = T0 - t0

        # remove negative and 0 time
        ind = T > 0
        T = T[ind]

        # time to energy conversion
        V = L / T  # velocity in m/s
        E = m * V**2 / 2  # energy bins in Joules
        self.V = V
        self.E = E / e  # energy bins in eV

        self.I = self.elec[ind]  # keep only bins with positive times


        # multiply by jacobian for conversion (I(e) = I(t)*E^(-3/2))
        #constants were thrown away since we only care about relative yields
        self.Ie = self.I / self.E**(3 / 2)

        # throw away high energy data just to reduce file size, also flip arrays to make low energy at index 0
        ind = np.argmax(self.E < 400)
        self.E = np.flip(self.E[ind:])
        self.Ie = np.flip(self.Ie[ind:])
        self.Ie = self.Ie / self.Ie.max()

    def manipulatePlot(self, wavelength=650, t0=1.92, L=0.53):
        """
        Takes an electron spectrum and an energy axis that is at least close
        and creates a plot with sliders to fine tune calibration scale
        """
        eg = 1239.8 / wavelength  # photon energy
        self.t2E(L, t0 * 1e-8)

        axis_color = 'lightgoldenrodyellow'

        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111)

        # Adjust the subplots region to leave some space for the sliders and buttons
        fig.subplots_adjust(left=0.1, bottom=0.25)

        # Draw the initial plot
        # The 'line' variable is used for modifying the line later
        gridline = []
        for i in range(int(80 / eg) + 1):
            gridline.append(ax.axvline(i * eg, alpha=0.4))
        [line] = ax.plot(self.E, self.Ie,
                         linewidth=2, color='red')

        ax.set_yscale('log')
        ax.set_xlim([0, 55])
        ax.set_ylim(1e-6)

        # Add three sliders for tweaking the parameters

        # Define an axes area and draw a slider in it
        L_slider_ax = fig.add_axes(
            [0.1, 0.1, 0.65, 0.03], facecolor=axis_color)
        L_slider = Slider(L_slider_ax, 'L', 0.4, 0.6, valinit=L)

        t0_dButton_ax = fig.add_axes(
            [0.8, 0.15, 0.03, 0.03], facecolor=axis_color)
        t0_dButton = Button(t0_dButton_ax, '-')
        t0_dButton.label.set_fontsize(16)

        t0_uButton_ax = fig.add_axes(
            [0.83, 0.15, 0.03, 0.03], facecolor=axis_color)
        t0_uButton = Button(t0_uButton_ax, '+')
        t0_uButton.label.set_fontsize(11)

        # Draw another slider
        t0_slider_ax = fig.add_axes(
            [0.1, 0.15, 0.65, 0.03], facecolor=axis_color)
        t0_slider = Slider(t0_slider_ax, 'T0', -5, 5, valinit=t0)

        # Draw another slider
        shift_slider_ax = fig.add_axes(
            [0.1, 0.05, 0.65, 0.03], facecolor=axis_color)
        shift_slider = Slider(
            shift_slider_ax, 'Shift', -2.0, 2.0, valinit=0)

        # Define an action for modifying the line when any slider's value changes

        def sliders_on_changed(val):
            t0 = t0_slider.val * 1e-8
            self.t2E(L_slider.val, t0)
            line.set_data(self.E + shift_slider.val, self.Ie)
            fig.canvas.draw_idle()

        def dButton_clicked(val):
            t0 = t0_slider.val * 1e-8 - 0.01e-8
            t0_slider.set_val(t0 / 1e-8)
            self.t2E(L_slider.val, t0)
            line.set_data(self.E + shift_slider.val, self.Ie)
            fig.canvas.draw_idle()

        def uButton_clicked(val):
            t0 = t0_slider.val * 1e-8 + 0.01e-8
            t0_slider.set_val(t0 / 1e-8)
            self.t2E(L_slider.val, t0)
            line.set_data(self.E + shift_slider.val, self.Ie)
            fig.canvas.draw_idle()

        L_slider.on_changed(sliders_on_changed)
        t0_slider.on_changed(sliders_on_changed)
        shift_slider.on_changed(sliders_on_changed)
        t0_dButton.on_clicked(dButton_clicked)
        t0_uButton.on_clicked(uButton_clicked)
        plt.show()
        print(
            f'L = {L_slider.val}, T0 = {t0_slider.val}, offset = {shift_slider.val}')

data = Data(pth='Ar_650nm.npy')
data.manipulatePlot()
#plt.show()
