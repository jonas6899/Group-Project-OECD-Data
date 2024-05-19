from matplotlib.figure import Figure
import pandas as pd



def display_data(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[data.TIME_PERIOD <= selectedtimeend]  # filter end year
    data = data[data.TIME_PERIOD >= selectedtimestart]  # filter end year
    
    if len(data) == 0:
        return "NO DATA"
    
    # remove the doubled columns
    del data["HC511_y"]
    del data["HC512_y"]
    data.rename(columns={"HC511_x": "HC511"}, inplace=True)
    data.rename(columns={"HC512_x": "HC512"}, inplace=True)

    
    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    
    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))


    # Create plot
    fig = Figure(figsize=(4.8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["HC0", "HC1HC2", "HC511", "HC3", "HC4", "HC512", "HC513", "HC52"]
    for i, category in enumerate(categories):
        if plottype == "line":
            ax.plot(data["TIME_PERIOD"], data[category], label=legend_mapping[category], color=colors[i])
        elif plottype == "scatter":
            ax.scatter(data["TIME_PERIOD"], data[category], label=legend_mapping[category], color=colors[i])
        elif plottype == "bar":
            ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=legend_mapping[category], width=0.1, color=colors[i])
        else:
            raise ValueError
            
    # Set x-axis to only show integers
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(labelsize=10, labelcolor=labelcolor)
    ax.set_title("Health Care Cost Over Time", color=labelcolor)
    ax.set_xlabel("Year", color=labelcolor)
    ax.set_ylabel("Health Care Cost", color=labelcolor)
    
    # Position the legend underneath the plot
    ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5))

    return fig



if __name__ == "__main__":
    
    # import data
    data = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")
    
    # define face and label colour
    facecolor = "#FFFFFF"
    labelcolor = "#000000"
    plottype="scatter"
    selectedcountry = "CHE"
    
    
    
    
    
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    fig = display_data(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023)
    
    # Display the figure
    canvas = FigureCanvas(fig)
    canvas.draw()
    
    plt.figure(figsize=(10, 6))
    plt.imshow(canvas.buffer_rgba())
    plt.axis('off')
    plt.show()
    
    
    print(fig)
    
    
    
    
    
    
    
    
