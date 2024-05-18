from matplotlib.figure import Figure
import pandas as pd
import numpy as np

def display_data(data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023):
    # filter data 
    data = data[data.index.values == selectedcountry] # filter country
    data = data[data.TIME_PERIOD <= selectedtimeend] # filter end year
    data = data[data.TIME_PERIOD >= selectedtimestart] # filter end year
    
    # Create plot
    fig = Figure(figsize=(10, 6), facecolor="#FFFFFF")
    ax = fig.add_subplot()
    
    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]
    
    categories = ["HC0", "HC1HC2", "HC511_x", "HC3", "HC4", "HC512_x", "HC513", "HC52"]
    for i, category in enumerate(categories):
        if plottype == "line":
            ax.plot(data["TIME_PERIOD"], data[category], label=category, color=colors[i])
        elif plottype == "scatter":
            ax.scatter(data["TIME_PERIOD"], data[category], label=category, color=colors[i])
        elif plottype == "bar":
            ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=category, width=0.1, color=colors[i])
    
    ax.tick_params(labelsize=10, labelcolor="black")
    ax.set_title("Health Care Cost Over Time", color="black")
    ax.set_xlabel("Year", color="black")
    ax.set_ylabel("Health Care Cost", color="black")
    ax.legend(title="Categories")
    
    return fig



# %% display this data here


# create dataframe from .csv files and set index to REF_AREA
master_df = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")
print("df created")

# define parameters
plottype = "scatter"
selectedcountry = "CHE"
selectedtimestart = 2015
selectedtimeend = 2020


import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Call the function
fig = display_data(master_df, plottype, selectedcountry, selectedtimestart, selectedtimeend)

# Display the figure
canvas = FigureCanvas(fig)
canvas.draw()

plt.figure(figsize=(10, 6))
plt.imshow(canvas.buffer_rgba())
plt.axis('off')
plt.show()


print(fig)
plt.fig