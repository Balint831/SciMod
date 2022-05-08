import networkx as nx
import numpy as np

import sys
from qubo_divided import solve_qubo_by_dividing
import matplotlib.pyplot as plt



def max_cut_qubo(A):
    for i in range( A.shape[0] ):
        degree = sum(A[i,:])
        A[i, i] = - degree
    return A

def generate_adjacency(n):
    G = nx.barabasi_albert_graph(n, 5)
    return nx.to_numpy_array(G)

import itertools

def calculate_QUBO_explicitely(Q):
    d = len(Q)

    bitstrings = list(map(np.array, list(itertools.product([0, 1], repeat=d))))

    values = []

    for bitstring in bitstrings:
        values.append(bitstring @ Q @ bitstring)

    return min(values), bitstrings[np.argmin(values)]


#A = generate_adjacency(20)
#Q = max_cut_qubo(A)
#np.savetxt("barabasi_adj.txt", Q, delimiter =",")
#Q = np.loadtxt("/home/balint831/scimod/data/barabasi_adj.txt", delimiter=",")
#b = np.random.normal(size = (10,10))
#Q = b + b.T
#np.savetxt("/home/balint831/scimod/random.txt",Q,delimiter =",")
Q = np.loadtxt("/home/balint831/scimod/data/shallow/erdos_renyi_16/erdos_renyi16_3.txt", delimiter = ",")
updates = 30
shots = 20
d_per_computer = 4
lr  = 100
#min_energy, min_bitstring = calculate_QUBO_explicitely(Q)
min_energy, min_bitstring = solve_qubo_by_dividing( Q,
            learning_rate = lr,
            shots = shots,
            updates = updates,
            d_per_computer= d_per_computer)
 
print(min_energy, "\n", min_bitstring)
with open("/home/balint831/scimod/log_erdos.txt",mode="a") as f:
    pass
    s = f"{updates} \t {shots} \t {d_per_computer} \t {min_energy} \t {min_bitstring}\n"
    f.write(s)
plt.savefig(f"/home/balint831/scimod/media/energy-update_lr{lr}_s{shots}_u{updates}_d{d_per_computer}.png", dpi = 600)