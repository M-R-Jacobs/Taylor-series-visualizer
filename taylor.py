# Library imports
import sympy as sympy
import numpy as numpy 
import matplotlib.pyplot as mpl
from matplotlib.widgets import TextBox, Button, RadioButtons



# Set up variables and function
x, a, b = sympy.symbols('x a b') # variables
b_val = 1

functions = {
    'sin(bx)': sympy.sin(b * x),
    'exp(bx)': sympy.exp(b *x),
    'ln(bx)': sympy.log(b * x),
    '1/(1+x²)': 1 / (1 + x**2)
}
    # functions is a dictionary: maps keys ('' labels) that are searched, onto values (sympy expressions) that you get back

f_label = 'sin(bx)' # start sin(1x) by default
f = functions[f_label].subs(b, b_val) # rebuild f according to user selection




# Build upt Taylor series loop
def taylor_polynomial(f, x, a, n):
    polynomial = 0
    for k in range(n + 1): # every int. from 0 to n inclusive
        term = sympy.diff(f, x, k).subs(x, a) / sympy.factorial(k) * (x - a)**k
        polynomial = polynomial + term
    return polynomial



# Build the figures and plot
x_vals = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 500)
f_vals = numpy.array([float(f.subs(x, val1)) for val1 in x_vals])
    # list comprehension loops through all x_vals, subs into f and puts in array

a_val = 0 # Defaultl Maclaurin
n_val = 0

p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val).subs(x,val)) for val in x_vals])

fig = mpl.figure(figsize=(10, 6)) # window size in inches, w x h. Slightly wider
gs = fig.add_gridspec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1]) # 2 rows and 2 columns, ratios: left 2x as wide
ax = fig.add_subplot(gs[:, 0]) # : makes left column spans both rows
ax_r = fig.add_subplot(gs[1, 1]) # bottom right cell, for R(x) (remainder polynomial)
ax_m = fig.add_subplot(gs[0, 1]) # top right for M (max error in Taylor)
    # index starts i=0, from top; [row, column]

mpl.subplots_adjust(bottom=0.25)
line_f, = ax.plot(x_vals, f_vals, label='f(x)')
line_p, = ax.plot(x_vals, p_vals, label='P_n(x)')
    # comma needed to take from list to line

ax.legend() # accepts labels from line 55 and 56
ax.grid(True) # must be capital
ax.set_ylim(-5, 5) # make adaptable

ax_m.axis('off') # don't want M grid
m_text = ax_m.text(0.5, 0.5, 'M = ', transform = ax_m.transAxes, ha = 'center', va = 'center', fontsize = 12)
    # needs to be a variable that can update

ax_r.set_ylim(0,1)
ax_r.set_title('|R_n(x)|')
ax_r.grid(True)
line_r, = ax_r.plot(x_vals, numpy.zeros_like(x_vals), label = '|R_n(x)|') # array of zeros as default same length as x_vals



# n, a, and b boxes and arrows for user input, plus radio buttons widget for function selection
ax_box_n = mpl.axes([0.22,0.1,0.1,0.04]) # define axes regions before widget creation below
ax_left_n = mpl.axes([0.13,0.1,0.04,0.04])
ax_right_n = mpl.axes([0.34,0.1,0.04,0.04])

ax_box_a = mpl.axes([0.22,0.05,0.1,0.04])
ax_left_a = mpl.axes([0.13,0.05,0.04,0.04])
ax_right_a = mpl.axes([0.34,0.05,0.04,0.04])

ax_box_b = mpl.axes([0.22,0.15,0.1,0.04])
ax_left_b = mpl.axes([0.13,0.15,0.04,0.04])
ax_right_b = mpl.axes([0.34,0.15,0.04,0.04])

ax_radio = mpl.axes([0.55,0.02,0.15,0.15])
    # widget locations in % from: [left, bottom, width, height]

box_n = TextBox(ax_box_n, 'n', initial = str(n_val)) # str converts value to string (for Textbox)
btn_left_n = Button(ax_left_n, '<') # region and label
btn_right_n = Button(ax_right_n, '>')

box_a = TextBox(ax_box_a, 'a', initial = str(a_val)) # str converts value to string
btn_left_a = Button(ax_left_a, '<') # region and label
btn_right_a = Button(ax_right_a, '>')

box_b = TextBox(ax_box_b, 'b', initial = str(b_val))
btn_left_b = Button(ax_left_b, '<')
btn_right_b = Button(ax_right_b, '>')

radio = RadioButtons(ax_radio, list(functions.keys())) # grab labels (function options) as list and make clickable options
    # btn_left and btn_right will be called at the end of the widget interactions section, next
    # box_ will come before that, when defining the user interaction functions



# Handle updates to a and n sumbissions or widget interactions
def update_plot():
    if f_label == 'ln(bx)': # log domain error prevention for "Cannot convert complex to float"
        safe_vals = x_vals[x_vals > 0]
    else:
        safe_vals = x_vals

    f_vals = numpy.array([float(f.subs(x, val1)) for val1 in safe_vals])
    p_vals = numpy.array([float(taylor_polynomial(f, x, a_val, n_val).subs(x, val2)) for val2 in safe_vals])
    line_f.set_ydata(f_vals) # set_y replaces Taylor P y-values with new values, no x array regen
    line_p.set_ydata(p_vals)
    line_f.set_xdata(safe_vals) # Same as 2 lines above, need updated safe domain values
    line_p.set_xdata(safe_vals)

    r_vals = numpy.abs(f_vals - p_vals) # generic formula. Abs value
    line_r.set_ydata(r_vals)
    line_r.set_xdata(safe_vals)
    finite_r = r_vals[numpy.isfinite(r_vals)] # make sure function is visible, but e and ln diverege
    if len(finite_r) > 0:
        ax_r.set_ylim(0, max(finite_r) * 1.2)
    ax_r.set_xlim(safe_vals[0], safe_vals[-1]) # -1 index is just the last element

    # compute M
    f_deriv = sympy.diff(f, x, n_val +1)
    deriv_vals = numpy.array([abs(float(f_deriv.subs(x, val1))) for val1 in safe_vals])
    M = float(numpy.max(deriv_vals)) # these will be computed over only defined x_val. No inf M!
    m_text.set_text(f'M = {M:.4f}') # f string - embeds variables in text. 4 decimal places

    fig.canvas.draw_idle() # draw_idle tells matplotlib to redraw the figure efficiently

def select_function(label):
    global f_label, f
    f_label = label # update global tracker to new function name
    f = functions[f_label].subs(b, b_val)
    update_plot()

# text submissions handled when pressing enter in the wdiget:

def submit_n(text): # text arg passed in by mpl, text for TextBox. In this case, a number
    global n_val # modifies global variable directly, no new variables
    n_val = max(0, int(float(text))) # compares value and returns higher (positive only). Textbox -> integer
    update_plot()

def submit_a(text):
    global a_val 
    a_val = float(text) # any a value is fine
    update_plot()

def submit_b(text):
    global b_val, f # b and f are both globals (and submit_b rebuilds f with the new b_val, unlike n & a)
    b_val = max(1, int(float(text)))
    f = functions[f_label].subs(b, b_val) # look up f_label in functions, use b_val
    update_plot()

# click left and right handled on arrow widget click events, n, a, and b:

def click_left_n(event): # event arg for mpl mouse event object
    global n_val
    n_val = max(0, n_val - 1) # still need to prevent from going <0
    box_n.set_val(str(n_val)) # update box text with new value (n-1). .set_val is in mpl's TextBox object
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

def click_left_b(event):
    global b_val, f
    b_val = max(1, b_val - 1)
    box_b.set_val(str(b_val))
    f = functions[f_label].subs(b, b_val)
    update_plot()

def click_right_b(event):
    global b_val, f
    b_val += 1
    box_b.set_val(str(b_val))
    f = functions[f_label].subs(b, b_val)
    update_plot()

box_n.on_submit(submit_n) # on_submit - when user presses enter in text box
box_a.on_submit(submit_a)
box_b.on_submit(submit_b)
btn_left_n.on_clicked(click_left_n) # on_clicked - button widget click
btn_right_n.on_clicked(click_right_n)
btn_left_a.on_clicked(click_left_a)
btn_right_a.on_clicked(click_right_a)
btn_left_b.on_clicked(click_left_b)
btn_right_b.on_clicked(click_right_b)

radio.on_clicked(select_function)


mpl.show()
