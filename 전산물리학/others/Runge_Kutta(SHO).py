import numpy as np
import matplotlib.pyplot as plt

from numpy.linalg import inv
from math import sqrt

m = 2.0
k = 2.0

omega = sqrt(k/m)

c = 0.0
F0 = 0.0

delta_t = 0.01
time = np.arange(0,40,delta_t)

x0 = 1.0
v0 = 0.0

y = np.array([v0,x0])
A = np.array([[m,0.0],[0.0,1.0]])
B = np.array([[c,k],[-1.0,0.0]])

F = np.array([0.0,0.0])

YY = []
VV = []

A_inv = inv(A)  #note. inv(A)를 밖에 두어서 연산을 줄여서 최적화 가능 

#time steps 
for t in time:

    k1 = A_inv.dot(F-B.dot(y))
    k2 = A_inv.dot(F-B.dot(y+0.5*delta_t*k1))
    k3 = A_inv.dot(F-B.dot(y+0.5*delta_t*k2))
    k4 = A_inv.dot(F-B.dot(y+1.0*delta_t*k3))

    G = (k1+2*k2+2*k3+k4)/6.0
    y = y + delta_t * G

    YY.append(y[1])
    VV.append(y[0])

plt.plot(time,YY)
plt.show()
