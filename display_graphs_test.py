import customtkinter as ctk
from display_graphs_backend_template import display_data
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# create dataframe from .csv files
master_df = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")

app = ctk.CTk()
app.geometry("900x800")

frame = ctk.CTkFrame(app, width=850, height=600)
frame.pack(pady=5)

def display_graph(plottype="scatter", selectedtimestart=2015,
                    selectedtimeend=2022):  # display Expenditure in health care across all areas of care
    print("started creating canvas!")  # test print

    # create variables
    selectedcountry = "AUS"
    facecolor = "#FFFFFF"
    labelcolor = "#000000"

    # Call the function that returns the Matplotlib plot
    plot = display_data(facecolor, labelcolor, master_df, plottype, selectedcountry, selectedtimestart, selectedtimeend)

    # Create a canvas widget
    canvas = FigureCanvasTkAgg(plot, master=frame)
    print("create graph")
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5)
    print("place graph")

def clear_it():
    # Clear the graph_frame
    for widget in frame.winfo_children():
        widget.destroy()

Button = ctk.CTkButton(app, text="Graph it!", command=display_graph)
Button.pack(pady=30)
Button = ctk.CTkButton(app, text="Clear it!", command=clear_it)
Button.pack(pady=5)


app.mainloop()