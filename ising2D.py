import networkx as nx 
import dwave_networkx as dnx
import matplotlib.pyplot as plt
import minorminer
import dimod
import numpy as np 

from dwave.embedding import embed_ising, unembed_sampleset
num_raws = 10
num_columns = 10
from helpers import ising2Dbuilder
from helpers import coef
J,h = coef.QuadraticRandomCoefBuilder(num_columns, num_raws)
print('Standard')
print(ising2Dbuilder.Ising2DBuilder(num_columns,num_raws,False,J,h))
print('Lower noise')
print(ising2Dbuilder.Ising2DBuilder(num_columns,num_raws,True,J,h))
