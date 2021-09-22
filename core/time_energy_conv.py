import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from tools.data_flow import header_to_dict
from numba import njit

MASS = 9.1093837015 * 10**-31  # electon mass
CHARGE = 1.602176634 * 10**-19  # electron charge

#expensive function (apply numba)
@njit
def t2E(time:np.ndarray, count:np.ndarray, L=0.53, t0=1.92e-8, E_max=400): # t2E was mainly written by Kent
    """
    converting time to energy
    time (arr) is taken from the original data (not modified)
    L is the TOF length in meters
    t0:extra time (s) that the signel spent on the electronics. TOF = Tot_t - t0.
    """
    # get actual time of flight (remove t0 delays)
    T = time - t0

    # remove negative and 0 time
    ind = T > 0
    T = T[ind]
    I = count[ind]  # keep only bins with positive times

    # time to energy conversion
    V = L / T  # velocity in m/s
    E = MASS * V**2 / 2  # energy bins in Joules
    E = E / CHARGE  # energy bins in eV

    # multiply by jacobian for conversion (I(E) = I(t)*E^(-3/2))
    #constants were thrown away since we only care about relative yields
    Ie = I / E**(3 / 2)

    # throw away high energy data just to reduce file size, also flip arrays to make low energy at index 0
    ind = np.argmax(E < E_max)
    E = np.flip(E[ind:])
    Ie = np.flip(Ie[ind:])
    Ie = Ie / Ie.max()
    return E, Ie


class TEC:

    def __init__(self):
        # Init Time fig
        self.fig_t, self.ax_t, self.line_t = self.add_fig(
            title='Time of Flight', xlabel='TOF (sec)', ylabel='Yeild (a.u.)', xlim=(0, 100e-9), ylim=(10e-16,1))
        # Init E Fig
        self.fig_e, self.ax_e, self.line_e = self.add_fig(
            title='ATI Spectra', xlabel='Electron Energy (ev)', ylabel='Yeild (a.u.)', xlim=(0, 100), ylim=(10e-8, 1))
        # Init Vlines
        self.vls = self.ax_e.vlines([0],0,0)
        
        self.has_data = False
        self.file_str = None
        self.prev_wl = None

    def update_vlines(self, wl):
        if wl != self.prev_wl:
            self.set_wl(wl)
            self.vls.remove()
            self.set_fixed_vlines(self.ax_e)
            self.prev_wl = wl

    def set_wl(self, wl=650):
        self.wl = wl
        self.cal_ph_e()

    def cal_ph_e(self):
        self.ph_e = 1239.8 / self.wl  # photon energy in ev

    def load_data(self, file, kind='st'):
        """ file is either a streamlit 'load' object (kid='st'), txt file (kind='txt') or numpy file
        (kind='npy'). The file should have two columns: time and count arr. 
        """
        if kind == 'st':
            self.file_str = file.read().decode("utf-8")
            self.time, self.count = np.loadtxt(StringIO(self.file_str), delimiter=',').T
            self.time = self.time*1e-9
            self.count = self.count / self.count.max()    # Normalization
        elif kind == 'txt':
            pass
        elif kind == 'npy':
            data = np.load(file)  # load raw time of flight data
            self.time = data[0]  # time bins
            self.count = data[1]  # electron counts per time bin
        else:
            pass
        self.has_data = True

    def get_file_header(self):
        if self.file_str:
            return header_to_dict(self.file_str)
        return {'info':['None']}

    def add_fig(self, title, xlabel, ylabel, xlim, ylim,figsize=None, dpi=90):
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(*ylim)
        ax.set_xlim(*xlim)
        ax.set_yscale('log')
        # add empty line
        line, = ax.plot([])
        return fig, ax, line

    def set_fixed_vlines(self, ax, max_ev=80):
        n_of_vlines = int(max_ev / self.ph_e) + 1
        vl_xp = [i * self.ph_e for i in range(n_of_vlines)]
        self.vls = ax.vlines(vl_xp, 0, 1, alpha=0.4)
    
    def update_energy_line(self, t0, L, shift):
        """Update Energy axis. The y data is not modified, but will be limited
        to positive and low Energies
        """
        E, Ie = t2E(time=self.time.copy(), count=self.count.copy(), t0=t0, L=L)
        self.line_e.set_data(E + shift, Ie)





    # def add_vlines(self):
    #     self.vls = self.ax.vlines([0,0,0,0], 0, 1)

    # def update_vlines(self, x_list, spacing, offset, ymin=0, ymax=1):
    #     seg_new = [np.array([[x*spacing + offset, ymin],
    #                         [x*spacing + offset, ymax]]) for x in x_list]
    #     self.vls.set_segments(seg_new)
