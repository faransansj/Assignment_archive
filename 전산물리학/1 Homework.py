# 1. Taylor Series 
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

# 2. Simple Harmonic Oscillator 

# 3. Three cases for the damping harmonic oscillator 

# 4. 1st order Runge-Kutta and 4th order Runge-Kutta method 
