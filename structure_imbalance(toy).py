## TOY EXAMPLE

## Packages for setting the problem
import networkx as nx 
import random
import matplotlib.pyplot as plt

## Setting up a sampler 
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

## Creating a graph of social structure
G = nx.complete_graph(4)
G.add_edges_from([(u,v,{'sign': 2*random.randint(0,1)-1}) for u,v in G.edges])
nx.relabel_nodes(G, {0: 'Alice', 1: 'Bob', 2: 'Eve', 3: 'Wally'}, copy=False)

## Just printing out
print('Friends:',[(x,y) for (x,y, sign) in G.edges(data='sign') if (sign == 1)])
print('Enemies:',[(x,y) for (x,y, sign) in G.edges(data='sign') if (sign == -1)])

## SOLVING
## dnx can solve our problem by itself

import dwave_networkx as dnx
imbalance, bicoloring = dnx.structural_imbalance(G, sampler)

print('Imbalance:',imbalance)
print('Groups:', bicoloring)

