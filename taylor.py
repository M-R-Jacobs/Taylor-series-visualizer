# Library imports
import sympy as sympy
import numpy as numpy 
import matplotlib.pyplot as mpl
from matplotlib.widgets import TextBox, Button



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

p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val).subs(x,val)) for val in x_vals])

fig, ax = mpl.subplots()
mpl.subplots_adjust(bottom=0.25)
line_f, = ax.plot(x_vals, f_vals, label='f(x)')
line_p, = ax.plot(x_vals, p_vals, label='P_n(x)')
    # comma needed to take from list to line

ax.legend()
ax.grid(True) # must be capital
ax.set_ylim(-3, 3) # make adaptable



# n and a boxes and arrows for user input
ax_box_n = mpl.axes([0.22,0.1,0.1,0.04]) # define axes regions before widget creation
ax_left_n = mpl.axes([0.13,0.1,0.04,0.04])
ax_right_n = mpl.axes([0.34,0.1,0.04,0.04])

ax_box_a = mpl.axes([0.22,0.05,0.1,0.04])
ax_left_a = mpl.axes([0.13,0.05,0.04,0.04])
ax_right_a = mpl.axes([0.34,0.05,0.04,0.04])
    # widget locations in format: [left, bottom, width, height]

box_n = TextBox(ax_box_n, 'n', initial = str(n_val)) # str converts value to string (for Textbox)
btn_left_n = Button(ax_left_n, '<') # region and label
btn_right_n = Button(ax_right_n, '>')

box_a = TextBox(ax_box_a, 'a', initial = str(a_val)) # str converts value to string
btn_left_a = Button(ax_left_a, '<') # region and label
btn_right_a = Button(ax_right_a, '>')



# Handle updates to a and n sumbissions or widget interactions
def update_plot():
    p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val).subs(x, val2)) for val2 in x_vals])
    line_p.set_ydata(p_vals) # set_y replaces Taylor P y-values with new values, no x array regen
    fig.canvas.draw_idle() # draw_idle tells matplotlib to redraw the figure efficiently

def submit_n(text):
    global n_val # modifies global variable directly, no new variables
    n_val = max(0, int(float(text))) # compares value and returns higher (positive only). Textbox -> integer
    update_plot()

def submit_a(text):
    global a_val 
    a_val = float(text) # any a value is fine
    update_plot()

def click_left_n(event): # need the event argument
    global n_val
    n_val = max(0, n_val - 1) # still need to prevent from going <0
    box_n.set_val(str(n_val)) # update box text with new value (n-1)
    update_plot()

def click_right_n(event):
    global n_val
    n_val += 1
    box_n.set_val(str(n_val))
    update_plot()

def click_left_a(event):
    global a_val
    a_val -= 0.1 # tenths place adjustments
    box_a.set_val(str(round(a_val, 2))) # round to 2 decimal places
    update_plot()

def click_right_a(event):
    global a_val
    a_val += 0.1
    box_a.set_val(str(round(a_val, 2)))
    update_plot()

box_n.on_submit(submit_n) # on_submit - when user presses enter in text box
box_a.on_submit(submit_a)
btn_left_n.on_clicked(click_left_n) # on_clicked - button widget click
btn_right_n.on_clicked(click_right_n)
btn_left_a.on_clicked(click_left_a)
btn_right_a.on_clicked(click_right_a)


mpl.show()
