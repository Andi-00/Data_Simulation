# The datasets 700 - 999 are missing so they have to be gerated again

import sys
import os

from gwpy.timeseries import TimeSeries

import matplotlib.pyplot as plt
import numpy as np

from few.trajectory.inspiral import EMRIInspiral
from few.amplitude.romannet import RomanAmplitude
from few.amplitude.interp2dcubicspline import Interp2DAmplitude
from few.waveform import FastSchwarzschildEccentricFlux, SlowSchwarzschildEccentricFlux, GenerateEMRIWaveform
from few.utils.utility import (get_overlap,
                               get_mismatch,
                               get_fundamental_frequencies,
                               get_separatrix,
                               get_mu_at_t,
                               get_p_at_t,
                               get_kerr_geo_constants_of_motion,
                               xI_to_Y,
                               Y_to_xI)

from few.utils.ylm import GetYlms
from few.utils.modeselector import ModeSelector
from few.summation.interpolatedmodesum import CubicSplineInterpolant
from few.waveform import SchwarzschildEccentricWaveformBase
from few.summation.interpolatedmodesum import InterpolatedModeSum
from few.summation.directmodesum import DirectModeSum
from few.utils.constants import *
from few.summation.aakwave import AAKSummation
from few.waveform import Pn5AAKWaveform, AAKWaveformBase



use_gpu = False

# keyword arguments for inspiral generator (RunSchwarzEccFluxInspiral)
inspiral_kwargs={
        "DENSE_STEPPING": 0,  # we want a sparsely sampled trajectory
        "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
    }

# keyword arguments for inspiral generator (RomanAmplitude)
amplitude_kwargs = {
    "max_init_len": int(1e3),  # all of the trajectories will be well under len = 1000
    "use_gpu": use_gpu  # GPU is available in this class
}

# keyword arguments for Ylm generator (GetYlms)
Ylm_kwargs = {
    "assume_positive_m": False  # if we assume positive m, it will generate negative m for all m>0
}

# keyword arguments for summation generator (InterpolatedModeSum)
sum_kwargs = {
    "use_gpu": use_gpu,  # GPU is availabel for this type of summation
    "pad_output": False,
}

# THE FOLLOWING THREAD COMMANDS DO NOT WORK ON THE M1 CHIP, BUT CAN BE USED WITH OLDER MODELS
# EVENTUALLY WE WILL PROBABLY REMOVE OMP WHICH NOW PARALLELIZES WITHIN ONE WAVEFORM AND LEAVE IT TO
# THE USER TO PARALLELIZE FOR MANY WAVEFORMS ON THEIR OWN.

# set omp threads one of two ways
# num_threads = 4

# this is the general way to set it for all computations
# from few.utils.utility import omp_set_num_threads
# omp_set_num_threads(num_threads)

few = FastSchwarzschildEccentricFlux(
    inspiral_kwargs=inspiral_kwargs,
    amplitude_kwargs=amplitude_kwargs,
    Ylm_kwargs=Ylm_kwargs,
    sum_kwargs=sum_kwargs,
    use_gpu=use_gpu,
    # num_threads=num_threads,  # 2nd way for specific classes
)



gen_wave = GenerateEMRIWaveform("Pn5AAKWaveform")

# parameters
T = 0.05 # years
dt = 5  # seconds

M = 1e4  # solar mass
mu = 1  # solar mass

dist = 1.0  # distance in Gpc

p0 = 12.0
e0 = 0.2
x0 = 0.99  # will be ignored in Schwarzschild waveform

qS = 1E-6  # polar sky angle
phiS = 0.0  # azimuthal viewing angle


# spin related variables
a = 0.6  # will be ignored in Schwarzschild waveform
qK = 1E-6  # polar spin angle
phiK = 0.0  # azimuthal viewing angle


# Phases in r, theta and phi
Phi_phi0 = 0
Phi_theta0 = 0
Phi_r0 = 0

# Generate the random parameters for the EMRIs
# The parameters include M, mu / d, a, e0 and p0

def gen_parameters(N):
    n = np.random.uniform(4, 7, N)
    M = 10 ** n
    dm = np.random.uniform(1, 1E2, N)
    a = np.random.uniform(0, 1, N)
    e0 = np.random.uniform(0.1, 0.7, N)
    p0 = np.random.uniform(10, 16, N)

    parameters = np.array([np.array([M[i], dm[i], a[i], e0[i], p0[i]]) for i in range(N)])

    return parameters

# Generate the strain h from the parameters par and returns it
def gen_strain(par):
    M = par[:, 0]
    mu = np.ones_like(M)
    d = par[:, 1]
    a = par[:, 2]
    e0 = par[:, 3]
    p0 = par[:, 4]

    h = [gen_wave(M[i], mu[i], a[i], p0[i], e0[i], x0, d[i], qS, phiS, qK, phiK, Phi_phi0, Phi_theta0, Phi_r0, T=T, dt=dt) for i in range(len(d))]

    return h

# Generate the spectrograms of the given strains
def gen_specs(hs):

    specs = []

    for h in hs:
        
        # Fill the strain array with zeros, so that all have the same length
        # independant of the signal duration
        hp = np.pad(h.real, (0, 315582 - len(h)))

        ts = TimeSeries(hp, dt = dt)

        data = ts.spectrogram(2E4) ** (1/2)


        specs.append(data)

    return specs

# Save the spectrogram files as csv data
def save_files(files, loc, n = 0):
    for i in range(len(files)):
        np.savetxt("/hpcwork/cg457676/data/" + loc + "_{:05}.csv".format(700 + i), np.array(files[i]), delimiter = ",")


# Generate the data
# data = [np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_{:1}.csv".format(i), delimiter = ",") for i in range(10)]

# The geration yields, that the spin values of number 749 and 836 are above 0.9999
# this  results in an error, when generating the strain. Therefore the values are replaced with 0.9999
# The difference of the values of a is 0.000064 and 0.000049 and therefore negligable compared to the real values

# print(data[0][749])
# print(data[0][836])

# for j in range(len(data)):
#     for i in range(len(data[j])):
#         if data[j][i][2] > 0.9999: 
#             print(i, data[j][i][2])
#             data[j][i][2] = 0.9999

# fixing the values to 0.9999 -- has been done


data = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter = ",")[700:]


h = gen_strain(data)
spec = gen_specs(h)

# Save the strain
save_files(h, "strains/h")

# Save the spectrograms
save_files(spec, "spectrograms/spec")
