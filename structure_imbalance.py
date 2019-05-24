## TOY EXAMPLE

## Packages for setting the problem
import networkx as nx 
import random
import matplotlib.pyplot as plt

## Setting up a sampler 
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))
import dwave_networkx as dnx

from helpers.loader import global_signed_social_network

## This graph has edges with 'sign' lables. +1 and -1 if any type of friends and rivals respectively.
G = global_signed_social_network()

##Let's select a subgroup with Syria gangs and only before 2013:
syria_groups = set()

for group, data in G.nodes(data=True):
	if 'map' not in data:
		continue
	if data['map'] in {'Syria', 'Aleppo'}:
		syria_groups.add(group)
S = G.subgraph(syria_groups)

year = 2013
filtered_edges = ((u, v) for u, v, a in S.edges(data=True) if a['event_year'] <= year)
S = S.edge_subgraph(filtered_edges)

imbalance, bicoloring = dnx.structural_imbalance(S, sampler)

# ## Add labels about violation relationship ('frustration') and attibution to the group('color'):
# for edge in S.edges:
# 	S.edges[edge]['frustraion'] = (edge in imbalance)
# for node in S.nodes:
# 	S.nodes[node]['color'] = bicoloring[node]

