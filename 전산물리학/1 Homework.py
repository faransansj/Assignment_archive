# ------------------------------------------------------------------------
# 1. Taylor Series 
# ------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

from math import *

def taylor_series_approximation(x, count):
    # Initialize result
    result = np.zeros_like(x)
    
    # Calculate Taylor series approximation
    for n in range(count):
        term = x**n / factorial(n)
        result += term
    return result

# Test the function
x = np.linspace(0, 2, 100)  # Range of x values
count = 5  # Degree of the Taylor series

# Calculate the approximation
approximation = taylor_series_approximation(x, count)

# Plotting
plt.plot(x, approximation, 'b', label=f'Taylor Series (n={count})')
plt.plot(x, np.exp(x), 'r--', label='e^x')
plt.legend()
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Taylor Series Approximation of e^x')
plt.show()

# ------------------------------------------------------------------------
# 2. Simple Harmonic Oscillator 
# ------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

from math import *

# const & initial condition 
omega = 2.0
x0 = 1.0
v0 = 1.0

#parameter 
t = np.linspace(0,20,100)

#function 
x_t = x0 * np.cos(omega*t) + v0/omega * np.sin(omega*t)

#plotting
plt.grid(True)
plt.plot(t,x_t,'r')
plt.show()

# ------------------------------------------------------------------------
# 3. Three cases for the damping harmonic oscillator 
# ------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

from math import *

# Constants and initial conditions
k = 0.01  # spring constant
m = 1.0   # mass
x0 = 1.0  # initial position
v0 = 0.0  # initial velocity

# Critical damping coefficient
c_critical = 2 * sqrt(k * m)

# Damping coefficients for each case
c_over = 2 * c_critical  # Overdamping
c_crit = c_critical      # Critical Damping
c_under = 0.5 * c_critical  # Underdamping

# Time array
t = np.linspace(0, 200, 1000)

# Function to calculate displacement x(t) for different damping cases
def damped_oscillation(c):
    omega = sqrt(k / m)
    gamma = 0.5 * c / m

    if c == c_crit:  # Critical damping
        A = x0
        B = v0 + gamma * x0
        x_t = (A + B * t) * np.exp(-gamma * t)
    elif c > c_crit:  # Overdamping
        q = sqrt(gamma**2 - omega**2)
        A1 = 0.5 * ((1 + gamma/q) * x0 + v0/q)
        A2 = 0.5 * ((1 - gamma/q) * x0 - v0/q)
        x_t = A1 * np.exp(-(gamma - q) * t) + A2 * np.exp(-(gamma + q) * t)
    else:  # Underdamping
        omega_d = sqrt(omega**2 - gamma**2)
        A = x0
        B = (v0 + gamma * x0) / omega_d
        x_t = np.exp(-gamma * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))

    return x_t

# Plotting
plt.figure(figsize=(12, 8))

# Overdamping
x_over = damped_oscillation(c_over)
plt.plot(t, x_over, label="Overdamping")

# Critical Damping
x_crit = damped_oscillation(c_crit)
plt.plot(t, x_crit, label="Critical Damping")

# Underdamping
x_under = damped_oscillation(c_under)
plt.plot(t, x_under, label="Underdamping")

# Additional plot settings
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.title('Damped Harmonic Oscillators: Overdamping, Critical Damping, Underdamping')
plt.legend()

plt.show()

# ------------------------------------------------------------------------
# 4. 1st order Runge-Kutta and 4th order Runge-Kutta method 
# ------------------------------------------------------------------------

# 4-1. 1st order Runge-Kutta
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

# 4-2. 4th order Runge-Kutta method
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
