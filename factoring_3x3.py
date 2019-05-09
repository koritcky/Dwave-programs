### Use this file only to make 3x3->6 bit mutliplication. For other multiplications use another file

# Constrain satisfaction problem 
import dwavebinarycsp as dbc

# Set an integer to factor
P = 19

# A binary representation of P ("{:06b}" formats for 6-bit binary)
bP = "{:06b}".format(P)

## Obtains a multiplication circuit of 3 bits
csp = dbc.factories.multiplication_circuit(3)

## Convert the problem from CSP to BQM (min_classical_gap - gap between energies of wrong results)
bqm = dbc.stitch(csp, min_classical_gap=.1)

## This is the result of multiplication
p_vars = ['p0','p1','p2','p3','p4','p5']

## Make a dictionary of p_vars and P in binary
fixed_variables = dict(zip(reversed(p_vars),"{:06b}".format(P)))
fixed_variables = {var: int(x) for (var,x) in fixed_variables.items()}

## Fix the result of the product (kind of making a constrain). 
## As a result, all 'p0',...,'p5' will be removed from the bqm.
for var, value in fixed_variables.items():
	bqm.fix_variable(var, value)

## SETTING UP A SOLVER

from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler(solver={'qpu': True}, token='DEV-7201bbe105379663905954b7ed302eed2bd97866')
_, target_edgelist, target_adjacency = sampler.structure
## embedding
from dwave.embedding import embed_bqm, unembed_sampleset
from helpers.embedding import embeddings

## Embedding logical qubits to physical ones
embedding = embeddings[sampler.solver.id]
## Set connections betweeen physical qubits
bqm_embedded = embed_bqm(bqm, embedding, target_adjacency, 3.0)

# Return num_reads solutions (responses are in the D-Wave's graph of indexed qubits)

kwargs = {}
n = 50
if 'num_reads' in sampler.parameters:
    kwargs['num_reads'] = n
if 'answer_mode' in sampler.parameters:
    kwargs['answer_mode'] = 'histogram'
response = sampler.sample(bqm_embedded, **kwargs)
response = response.lowest()
print(response)
max_occur = 1
num_exp = 0
for i in range(len(response)):
	if response.record[i][2] > max_occur:
		max_occur = response.record[i][2]
		num_exp = i
#print(response)
#print("A solution indexed by qubits: \n", next(response.data(fields=['sample'])))

## Map back to the BQM's graph (nodes labeled "a0", "b0" etc,)
print(next(response.samples(n=num_exp)))
response = unembed_sampleset(response, embedding, source_bqm=bqm)
#print("\nThe solution in problem variables: \n",next(response.data(fields=['sample'])))

from helpers.convert import to_base_ten
# Select just the first sample. 
sample = next(response.samples(n=1))
dict(sample)

a, b = to_base_ten(sample)

print("Given integer P={}, found factors a={} and b={}".format(P, a, b))

