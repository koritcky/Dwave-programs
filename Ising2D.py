import networkx as nx 
import dwave_networkx as dnx
import matplotlib.pyplot as plt
import minorminer
import dimod
import numpy as np 

from dwave.embedding import embed_ising, unembed_sampleset

## Sampler setting
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler()

# List of nodes, edges and structure of out QPU
target_nodelist, target_edgelist, target_adjacency = sampler.structure

## Set the task:

## Building connections. Simple topology, edges are connected only to inner spins.
def QuadraticRandomCoefBuilder(num_rows, num_columns):
	J = {}
	for row in range(num_rows):
		for column in range(num_columns-1):
			J[(num_columns*row + column, num_columns*row + (column + 1))] = np.random.choice([1, -1])
	for row in range(num_rows-1):
		for column in range(num_columns):
			J[(num_columns*row + column, num_columns*(row + 1) + column)] = np.random.choice([1, -1])
	## Check for numbers of connections
	#print(len(J)==num_rows*(num_columns-1)+num_columns*(num_rows-1))
	return J

def QuadraticEqualCoefBuilder(num_rows, num_columns):
	J = {}
	sign = -1
	for row in range(num_rows):
		for column in range(num_columns-1):
			J[(num_columns*row + column, num_columns*row + (column + 1))] = sign
	for row in range(num_rows-1):
		for column in range(num_columns):
			J[(num_columns*row + column, num_columns*(row + 1) + column)] = sign
	## Check for numbers of connections
	#print(len(J)==num_rows*(num_columns-1)+num_columns*(num_rows-1))
	return J

## Number of spins in row/colums 
spins_in_row = 15
spins_in_column = 15




## Quadratic coefficients (square n x m with torus topology)np.random.choice([1, -1])
J = QuadraticRandomCoefBuilder(spins_in_row, spins_in_column)

## Linear coefficients
h = {i: (np.random.ranf()-0.5)*20 for i in range(spins_in_row*spins_in_column)}

## Embed logical qubits on QPU's qubits
embedding = minorminer.find_embedding(J, target_edgelist)




## Check, whether an embedding was succesfull
if not J:
    raise ValueError("no embedding found")


## Create a complete Ising model on a QPU 
target_h, target_J = embed_ising(h, J, embedding, target_adjacency)
# print('__________________')
# print('Linear coeff on QPU:', target_h)
# print('Quadratic coeff on QPU:', target_J)
# print('__________________')

## Set parameters for calculations. num_reas is a number of experiments
kwargs = {}
if 'num_reads' in sampler.parameters:
    kwargs['num_reads'] = 30
if 'answer_mode' in sampler.parameters:
    kwargs['answer_mode'] = 'histogram'

## Get a SampleSet with spins and energies (WARNING: results are for the task, embedded on QPU)
response = sampler.sample_ising(target_h,target_J, **kwargs)
# print('Resulting spins on QPU:')
# print(response)
# print('__________________')

## Return to the original spins:
unembedding = unembed_sampleset(response, embedding, dimod.BinaryQuadraticModel.from_ising({}, J))
# print('Resulting spins in terms of original task:')
# print(unembedding)
# print('__________________')
print('Results:')
for sample in unembedding.data():
	print(sample)
	break

