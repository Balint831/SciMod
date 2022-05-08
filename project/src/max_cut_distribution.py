# hwloc-bind --membind node:1 --cpubind node:1 -- python max_cut_distribution.py
import networkx as nx
import numpy as np
import time

import sys
from qubo_divided import yield_qubo_energies
import matplotlib.pyplot as plt
import pandas as pd

import plotly.express as px

updates = 60
shots = 41
d_per_computer = 2
learning_rate = 0.05

#Q = np.loadtxt("/home/balint831/scimod/data/barabasi_adj.txt", delimiter=",")

Q = np.loadtxt("/home/balint831/scimod/data/shallow/erdos_renyi_16/erdos_renyi16_3.txt", delimiter = ",")

def logged_measurement(updates, shots, d_per_computer, learning_rate, fname):
    t1 = time.time()

    it = yield_qubo_energies(Q,
                learning_rate = learning_rate,
                shots = shots,
                updates = updates,
                d_per_computer= d_per_computer)


    #measurements_by_update = []
    measurements = []
    for u in range(updates*2):
        e, bs, p = next(it)
        one_update = { "energies": e, "bitstrings": bs,
                        "parity": p,     "update": u % updates }

        for shot_idx in range(shots):
            one_meas = { "energy": e[shot_idx], "bitstring": bs[shot_idx], 
                        "parity": p,              "update": u % updates }
            measurements.append( one_meas )
        #measurements_by_update.append( one_update )


    measurements = pd.DataFrame(measurements)
    measurements.to_csv(f"/home/balint831/scimod/data/shallow/erdos_renyi_16/{fname}.csv")
    print(time.time() - t1, f"shots: {shots}, updates: {updates}")

logged_measurement( updates, shots, d_per_computer, learning_rate, f"erdos_renyi_lr{learning_rate}_s{shots}_d{d_per_computer}")

learning_rate = 0.1
logged_measurement( updates, shots, d_per_computer, learning_rate, f"erdos_renyi_lr{learning_rate}_s{shots}_d{d_per_computer}")

learning_rate = 0.01
logged_measurement( updates, shots, d_per_computer, learning_rate, f"erdos_renyi_lr{learning_rate}_s{shots}_d{d_per_computer}")

learning_rate = 0.5
logged_measurement( updates, shots, d_per_computer, learning_rate, f"erdos_renyi_lr{learning_rate}_s{shots}_d{d_per_computer}")

learning_rate = 10**(-5)
#logged_measurement( updates, shots, d_per_computer, learning_rate, f"meas_lr{learning_rate}_s{shots}_d{d_per_computer}")

learning_rate = 10**(-6)
#logged_measurement( updates, shots, d_per_computer, learning_rate, f"meas_lr{learning_rate}_s{shots}_d{d_per_computer}")


#fig = px.scatter()