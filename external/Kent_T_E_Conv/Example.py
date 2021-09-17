import numpy as np
import matplotlib.pyplot as plt
import tools

data = tools.Data('Ar_650nm.npy')  # create data object
data.t2E()

# Plot Raw time of flight spectrum
plt.figure(figsize=(11, 5))
p = plt.subplot(121)
plt.plot(data.T * 1e9, data.elec, lw=2)

plt.xlabel('Time (ns)', fontsize=16)
plt.ylabel('Electron Count (arbitrary units)', fontsize=16)
plt.yscale('log')
plt.xlim(100, 1000)
plt.ylim(1e-6)
plt.arrow(0.3, 0.15, 0.4, 0, transform=p.transAxes,
          length_includes_head=True, width=0.01, shape='right', color='r')
plt.text(0.36, 0.18, 'To Lower Energy', transform=p.transAxes, fontsize=12)
plt.title('Argon, 650 nm, Raw time of flight data')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Plot converted time of flight spectrum
p = plt.subplot(122)
plt.plot(data.E, data.Ie, lw=2)

plt.xlabel('Energy (eV)', fontsize=16)
plt.ylabel('Electron Count (arbitrary units)', fontsize=16)
plt.yscale('log')
plt.xlim(0, 60)
plt.ylim(1e-7)

plt.title('Argon, 650 nm, converted time of flight data')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()


plt.show()
