import numpy as np
import matplotlib.pyplot as plt
from math import *

# init const
x0 = 10.0 #10 meter
v0 = 0.0 #0m/s

k = 1.0 #spring constance
m = 1.0 #1kg

omega = sqrt(k/m) #freq.

#solution
t = np.linspace(0,20,500) #0~20을 500번으로 나눔
#t = np.arrange(0,20,0.04) #위의 코드랑 얼추 비슷함

x_t = x0 + np.cos(omega*t) + (v0/omega) * np.sin(omega*t) # x(t)
x_dot_t = -x0*omega * np.sin(omega*t) + v0 * np.cos(omega*t) # x(t)

# KE = 0.5 *m ** x_dot_t
# SP = 0.5 *k * (x_dot_t ** 2)
plt.plot(t,x_t,'b')
plt.show()
