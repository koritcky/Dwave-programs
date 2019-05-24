import numpy as np

sigma_x = np.array([[0,1],[1,0]])
sigma_z = np.array([[1,0],[0,-1]])
Id_2	= np.array([[1,0],[0,1]])
Id_4 	= np.kron(Id_2, Id_2)
H_I = Id_4 - (1.0/2)*(np.kron(sigma_x,Id_2) + np.kron(Id_2,sigma_x))
H_F = (1.0/2)*(Id_4 + np.kron(sigma_z,sigma_z))
H = H_I + H_F
print('H_I:')
print(H_I)
print('H_F:')
print(H_F)
print(H)
