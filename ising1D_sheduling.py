import networkx as nx 
import dwave_networkx as dnx
import matplotlib.pyplot as plt
import minorminer
import dimod
import numpy as np 

from dwave.embedding import embed_ising, unembed_sampleset

## Sampler setting
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler(solver={'qpu': True, 'max_anneal_schedule_points__gte': 4})
# List of nodes, edges and structure of out QPU
target_nodelist, target_edgelist, target_adjacency = sampler.structure



## Set the task:
#number of spins 
n = 4
#Quadratic coefficients (ring topology)
J = {(i,i+1):1 for i in range(n-1)} 
#Linear coefficients
h = {0: 1}
# Embed logical qubits on QPU's qubits
embedding = minorminer.find_embedding(J, target_edgelist)


# Check, whether an embedding was succesfull
if not embedding:
    raise ValueError("no embedding found")


#Create a complete Ising model on a QPU 
target_h, target_J = embed_ising(h, J, embedding, target_adjacency)

# print('__________________')
# print('Linear coeff on QPU:', target_h)
# print('Quadratic coeff on QPU:', target_J)
# print('__________________')

# Set parameters for calculations. num_reas is a number of experiments
runs = 30
schedule = [[0.0,0.0], [10.1, 0.1], [10.3, 0.3], [100.0, 1.0]]
response = sampler.sample_ising(target_h,
							target_J, 
							num_reads=runs, 
							answer_mode='histogram',
							anneal_schedule=schedule)
#Get a SampleSet with spins and energies (WARNING: results are for the task, embedded on QPU)
# print('Resulting spins on QPU:')
# print(response)
# print('__________________')

#Return to the original spins:
unembedding = unembed_sampleset(response, embedding, dimod.BinaryQuadraticModel.from_ising({}, J))
# print('Resulting spins in terms of original task:')
# print(unembedding)
# print('__________________')
# plt.hist(unembedding.record.energy,rwidth=1,align='left')
# plt.show()
print(unembedding)
print("QPU time used:", unembedding.info['timing']['qpu_access_time'], "microseconds.")


