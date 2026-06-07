# Library imports
import sympy as sympy
import numpy as numpy 
import matplotlib.pyplot as matplotlib
from matplotlib.widgets import Slider



# Set up variables and function
x, a = sympy.symbols('x a') # variables
f = sympy.sin(x) # function input (change later!)



# Build upt Taylor series loop
def taylor_polynomial(f, x, a, n):
    polynomial = 0
    for k in range(n + 1): # every int. from 0 to n inclusive
        term = sympy.diff(f, x, k).subs(x, a) / sympy.factorial(k) * (x - a)**k
        polynomial = polynomial + term
    return polynomial



# Build the plot
x_vals = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 500)
f_vals = numpy.array([float(f.subs(x, val1)) for val1 in x_vals])
    # list comprehension loops through all x_vals, subs into f and puts in array

a_val = 0 # Defaultl Maclaurin
n_val = 0

p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val)).sub(x,val) for val in x_vals])

fig, ax = matplotlib.pyplot.subplots()
matplotlib.pyplot.subplots_adjust(botom=0.25)
line_f, = ax.plot(x_vals, f_vals, label='f(x)')
line_p, = ax.plot(x_vals, p_vals, label='P_n(x)')
    # comma needed to take from list to line

ax.legend()
ax.grid(True) # must be capital
ax.set_ylim(-3, 3) # make adaptable



# Slider details for user input
ax_n_slider = matplotlib.pyplot.axes([0.2, 0.1, 0.6, 0.03])
ax_a_slider = matplotlib.pyplot.axes([0.2, 0.05, 0.6, 0.03])
    # each of the 4 numbers are fractions of the figure size, [left, bottom, width, height]

n_slider = Slider(ax_n_slider, 'n', 1, 10, valinit = n_val, valstep = 1)
a_slider = Slider(ax_a_slider, 'a', -2*numpy.pi, 2*numpy.pi, valinit = a_val)
    # axes region, a label, min value, max value, and starting value

def update(val):
    n_val = int(n_slider.val)
    a_val = int(a_slider.val)
    p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val).sub(x,val2) for val2 in x_vals])
    line_p.set_ydata(p_vals)
    fig.canvas.draw_idle()
    # draw_idle tells matplotlib to redraw the figure efficiently

n_slider.on_changed(update)
a_slider.on_changed(update)
    # on_changed will trigger update

matplotlib.pyplot.show()
