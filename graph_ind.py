import networkx as nx 
import dwave_networkx as dnx
import matplotlib.pyplot as plt 


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

## Set the sampler we  are going to use
sampler = EmbeddingComposite(DWaveSampler())

## Creates an epmty graph
G = nx.Graph()

## Add edges to graph - this also adds the nodes
G.add_edges_from([(1,2),(2,5),(3,4),(4,5),(5,6),(6,7),(6,8)])

## Find the maximum independent set, S
S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=10)

##Pring the solution for user
print('Maximum independent set size found is', len(S))
print(S)

## Some visualisation
k = G.subgraph(S)
notS = list(set(G.nodes())-set(S))
othersubgraph = G.subgraph(notS)
pos = nx.spring_layout(G)
plt.figure()
nx.draw(G,pos=pos)
nx.draw(k,pos=pos)
nx.draw(othersubgraph, pos=pos, node_color='r')
plt.show()




