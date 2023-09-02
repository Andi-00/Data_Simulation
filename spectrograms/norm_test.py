# Code to plot the different parameter distriibutions

import numpy as np
from matplotlib import pyplot as plt

plt.rcParams['pgf.rcfonts'] = False
plt.rcParams['font.serif'] = []
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = True
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['errorbar.capsize'] = 2
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.title_fontsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.1

#plt.rcParams['savefig.transparent'] = True
plt.rcParams['figure.figsize'] = (6, 4)


a = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter=",")

for d in range(1, 10):
    b = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_{}.csv".format(d), delimiter=",")
    a = np.append(a, b, axis = 0)


print(a.shape)

M = np.log10(np.array(a[:, 0]))
dm = np.array(a[:, 1])
spin = a[:, 2]
e0 = a[:, 3]
p0 = a[:, 4]

parameters = [M, dm, spin, e0, p0]
names = [r"$\log M / M_{\odot}$", r"$d_L/ \mu$", r"Spin $a$", r"Eccentricity $e_0$", r"Seperation $p_0/M$"]
file_names = ["mass", "dist", "spin", "e", "p"]
n_bins = [12, 10, 10, 12, 12]
title = ["central mass", "distance and small mass", "spin", "eccentricity", "seperation"]


for i in range(len(names)):

    fig, ax = plt.subplots()

    print(len(parameters[i]))

    ax.hist(parameters[i], bins = n_bins[i], color = "#e60049", edgecolor = "black")
    ax.set_ylabel("Number")
    ax.set_xlabel(names[i])
    ax.set_title("Distribution of the generated " + title[i], y = 1.02)

    plt.savefig("./spectrograms/Parameter_Distributions/hist_" + file_names[i] + ".png")