# Code to plot the different parameter distriibutions

import numpy as np
from matplotlib import pyplot as plt

a = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_0.csv", delimiter=",")

for d in range(1, 10):
    b = np.genfromtxt("/hpcwork/cg457676/data/parameters/parameters_{}.csv".format(d), delimiter=",")
    a = np.append(a, b, axis = 0)


print(a.shape)

M = a[:, 0]
md = a[:, 1]
spin = a[:, 2]
e0 = a[:, 3]
p0 = a[:, 4]

fig, ax = plt.subplots()

ax.hist(np.log10(M), bins = 12, color = "royalblue", edgecolor = "black")

# ax.scatter(md, M, s = 5, color = "royalblue")
# ax.set_yscale("log")
plt.savefig("./spectrograms/test_hist.png")