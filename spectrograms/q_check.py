# Test code to plot the simulated data
import sys
import os

from gwpy.timeseries import TimeSeries

import matplotlib.pyplot as plt
import numpy as np

# from few.trajectory.inspiral import EMRIInspiral
# from few.amplitude.romannet import RomanAmplitude
# from few.amplitude.interp2dcubicspline import Interp2DAmplitude
# from few.waveform import FastSchwarzschildEccentricFlux, SlowSchwarzschildEccentricFlux, GenerateEMRIWaveform
# from few.utils.utility import (get_overlap,
#                                get_mismatch,
#                                get_fundamental_frequencies,
#                                get_separatrix,
#                                get_mu_at_t,
#                                get_p_at_t,
#                                get_kerr_geo_constants_of_motion,
#                                xI_to_Y,
#                                Y_to_xI)

# from few.utils.ylm import GetYlms
# from few.utils.modeselector import ModeSelector
# from few.summation.interpolatedmodesum import CubicSplineInterpolant
# from few.waveform import SchwarzschildEccentricWaveformBase
# from few.summation.interpolatedmodesum import InterpolatedModeSum
# from few.summation.directmodesum import DirectModeSum
# from few.utils.constants import *
# from few.summation.aakwave import AAKSummation
# from few.waveform import Pn5AAKWaveform, AAKWaveformBase

plt.rcParams['pgf.rcfonts'] = False
plt.rcParams['font.serif'] = []
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['errorbar.capsize'] = 2
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.title_fontsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.1

#plt.rcParams['savefig.transparent'] = True
plt.rcParams['figure.figsize'] = (10, 5)


# use_gpu = False

# # keyword arguments for inspiral generator (RunSchwarzEccFluxInspiral)
# inspiral_kwargs={
#         "DENSE_STEPPING": 0,  # we want a sparsely sampled trajectory
#         "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
#     }

# # keyword arguments for inspiral generator (RomanAmplitude)
# amplitude_kwargs = {
#     "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
#     "use_gpu": use_gpu  # GPU is available in this class
# }

# # keyword arguments for Ylm generator (GetYlms)
# Ylm_kwargs = {
#     "assume_positive_m": False  # if we assume positive m, it will generate negative m for all m>0
# }

# # keyword arguments for summation generator (InterpolatedModeSum)
# sum_kwargs = {
#     "use_gpu": use_gpu,  # GPU is availabel for this type of summation
#     "pad_output": False,
# }

# # THE FOLLOWING THREAD COMMANDS DO NOT WORK ON THE M1 CHIP, BUT CAN BE USED WITH OLDER MODELS
# # EVENTUALLY WE WILL PROBABLY REMOVE OMP WHICH NOW PARALLELIZES WITHIN ONE WAVEFORM AND LEAVE IT TO
# # THE USER TO PARALLELIZE FOR MANY WAVEFORMS ON THEIR OWN.

# # set omp threads one of two ways
# # num_threads = 4

# # this is the general way to set it for all computations
# # from few.utils.utility import omp_set_num_threads
# # omp_set_num_threads(num_threads)

# few = FastSchwarzschildEccentricFlux(
#     inspiral_kwargs=inspiral_kwargs,
#     amplitude_kwargs=amplitude_kwargs,
#     Ylm_kwargs=Ylm_kwargs,
#     sum_kwargs=sum_kwargs,
#     use_gpu=use_gpu,
#     # num_threads=num_threads,  # 2nd way for specific classes
# )




# gen_wave = GenerateEMRIWaveform("Pn5AAKWaveform")

# # parameters
# T = 0.05 # years
# dt = 5  # seconds

# M = 1e4  # solar mass
# mu = 1  # solar mass

# dist = 1.0  # distance in Gpc

# p0 = 12.0
# e0 = 0.2
# x0 = 0.99  # will be ignored in Schwarzschild waveform

# qS = 1E-6  # polar sky angle
# phiS = 0.0  # azimuthal viewing angle


# # spin related variables
# a = 0.6  # will be ignored in Schwarzschild waveform
# qK = 1E-6  # polar spin angle
# phiK = 0.0  # azimuthal viewing angle


# # Phases in r, theta and phi
# Phi_phi0 = 0
# Phi_theta0 = 0
# Phi_r0 = 0

# # Generate the random parameters for the EMRIs
# # The parameters include M, mu / d, a, e0 and p0

# # SEED = 3183

# par = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_3.csv", delimiter=",", skip_header = 813, skip_footer = 186)

# print("Masse M = {:.2E} M_sun, mu / d = {:.2E} M_sun / Gpc, spin a = {:.2f}\nEccentricity e_0 = {:.2f}, Seperation p_0 = {:.1f}".format(par[0], 1 / par[1], par[2], par[3], par[4]))

# # Vergleich mit den erzeugten daten
# # h = gen_wave(par[0], 1.00, par[2], par[4], par[3], x0, par[1], qS, phiS, qK, phiK, Phi_phi0, Phi_theta0, Phi_r0, T=T, dt=dt).real

# h = np.genfromtxt("/hpcwork/cg457676/data/strains/h_03813.csv", delimiter = ",", dtype = np.complex_).real

# t = np.arange(len(h)) * 5

# fig, ax = plt.subplots()

# ax.plot(t[:300], h[:300], color = "#e60049", zorder = 10)

# ax.set_xlabel("Time $t$ [s]")
# ax.set_ylabel("Strain $h_+$")
# ax.set_title("Plot of a strain (file number 3.813)", y = 1.02)

# plt.savefig("./spectrograms/Quality_check/test_h.png")



spectrogram = np.swapaxes(np.genfromtxt("/hpcwork/cg457676/data/Processed_Data_0/pspec0_03817.csv", delimiter = ","), 0, 1)

# Time in days

x = (np.arange(0, 79) + 0.5) * 2E4 / (3600 * 24)
y = (np.arange(2E3 + 1) + 0.5) * 5E-5

z = spectrogram

print(z.shape)
print(len(x))
print(len(y))

fig, ax = plt.subplots()

ax.pcolormesh(x, y, z)
ax.set_yscale("log")

ax.set_ylim(1E-4, 1E-1)


ax.set_ylabel("Frequency $f$")
ax.set_xlabel("Time $t$ in days")
ax.set_title("Spectrogram of a gravitational wave (file number 3.814)", y = 1.02)
ax.colorbar(label=r'Gravitational wave amplitude [1/$\sqrt{\mathrm{Hz}}$]')

ax.grid(False)

plt.savefig("./blabla.png")


# hp = np.pad(h, (0, 315582 - len(h)))

# ts = TimeSeries(hp, dt = dt)

# data = ts.spectrogram(2E4) ** (1/2)

# plot = data.imshow(norm='log', vmin = 2E-5 * np.max(np.array(data)))
# ax = plot.gca()
# ax.set_yscale('log')
# ax.set_ylim(1E-4, 1E-1)
# ax.grid(False)
# # ax.set_xlabel("Time $t$ [day]")
# ax.set_ylabel("Frequency $f$ [Hz]")
# ax.colorbar(label=r'Gravitational-wave amplitude [strain/$\sqrt{\mathrm{Hz}}$]')
    
# ax.set_title("Spectrogram of the wave", y = 1.02)

# print(data.shape)

# plot.savefig("./spectrograms/vgl_spec.png")


