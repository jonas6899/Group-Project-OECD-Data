# import things

import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import scipy.stats as ss
import ssl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# set main window
app = ctk.CTk()
app.geometry("1000x750")
app.title("Graph Display")

# import function that creates the plot
from oscars_data import display_data

# define function that creates the canvas in which to display the plot
def canvas_creator():
    # Call the function that returns the Matplotlib plot
    plot = display_data()
    # Create a canvas widget
    canvas = FigureCanvasTkAgg(plot, master=app)
    canvas.draw()
    canvas.get_tk_widget().place(x=40, rely=0.15)


button1 = ctk.CTkButton(app, text="Graph it!", command=canvas_creator)
button1.pack(pady=20)

# execute
app.mainloop()



