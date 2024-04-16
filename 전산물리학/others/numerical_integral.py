#--------------------------------------------------
# 
#--------------------------------------------------

import numpy as np 
import matplotlib.pyplot as plt

# variables 
m = 2.0
k = 2.0

# x-axis 
delta_t = 0.001 # time step 1ms 
time = np.arange(0.0,20.0,delta_t)

# initial condition
x0,v0 = 1.0,0.0

# states
x,v = x0,v0

# result list 
Y = [] # list position 
W = [] # list velocuty 

# time steps
for t in time:
    v = v + delta_t * (-k/m)*x
    x = x + delta_t * v
    Y.append(x)
    W.append(v)

# plot result 
plt.grid(True)
plt.plot(time,Y,'r')
plt.plot(time,W,'b')
plt.show()

#--------------------------------------------------
# 
#--------------------------------------------------
import numpy as np 
import matplotlib.pyplot as plt

from numpy.linalg import inv
from math import * 

# variables 
m = 2.0
k = 2.0

c = 1.0
F0 = 0.0

# x-axis 
delta_t = 0.0001 # time step 1ms 
time = np.arange(0.0,20.0,delta_t)

# initial condition
x0,v0 = 1.0,0.0

# initial state
y = np.array([v0,x0]) #vector [vel, pos]

#metrics
A = np.array([[m , 0.0],
             [0.0,1.0]])

B = np.array([[c ,k],
             [-1.0,0.0]])

F = np.array([0.0,0.0])

# result list 
Y = [] # list position 

# time steps
for t in time:
    v = v + delta_t * (-k/m)*x
    x = x + delta_t * v

    y = y + delta_t * inv(A).dot(F - B.dot(y))

    Y.append(y[1])

# plot result 
plt.grid(True)
plt.plot(time,Y,'r')
plt.show()

