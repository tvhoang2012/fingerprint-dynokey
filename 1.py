from os.path import dirname, join as pjoin
import numpy as np
import scipy.io as sio
import file
from scipy.io import savemat
Nperm = 600
Nkernel = 2
Kwindow = 128
G_vecs=[]
"""for i in range(Nperm):
  G_vecs.append(np.zeros((2,298)))
for i in range(Nperm):
  G_vecs[i] = file.getGvec(299,Nkernel)"""
G_vecs=file.randompern(Nperm,G_vecs,Nkernel)
data = sio.loadmat('1_8.mat')
a = data['Ftemplate']
a=np.array(a).flatten()
binary_codes=np.zeros(Nperm,dtype=np.int16)
binary_codes,G_vecs=file.WTA_hashing(a,G_vecs,Nkernel, Kwindow, Nperm)
#print(binary_codes)
#mdic = {"binary_code": binary_codes}
#print(mdic)
data = sio.loadmat('1_5.mat')
b = data['Ftemplate']
b=np.array(b).flatten()
binary_codes1=np.zeros(Nperm,dtype=np.int16)
binary_codes1,G_vecs=file.WTA_hashing(b,G_vecs,Nkernel, Kwindow, Nperm)
count=file.match(binary_codes,binary_codes1)
print(count/600)
        