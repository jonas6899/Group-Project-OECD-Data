from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator, FuncFormatter
import textwrap

def wrap_text(text, width):
    wrapped_lines = textwrap.wrap(text, width=width, break_long_words=False, replace_whitespace=False)
    return '\n'.join(wrapped_lines)

def currency_formatter(x, pos):
    return f'${x*1e-9:.1f}bn'

def display_data(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[(data.TIME_PERIOD <= selectedtimeend) & (data.TIME_PERIOD >= selectedtimestart)]  # filter years

    if len(data) == 0:
        return "NO DATA"

    # remove the doubled columns
    del data["HC511_y"]
    del data["HC512_y"]
    data.rename(columns={"HC511_x": "HC511", "HC512_x": "HC512"}, inplace=True)

    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

    # Create plot
    fig = Figure(figsize=(8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["HC0", "HC1HC2", "HC511", "HC3", "HC4", "HC512", "HC513", "HC52"]
    for i, category in enumerate(categories):
        if plottype == "line":
            ax.plot(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 20), color=colors[i])
        elif plottype == "scatter":
            ax.scatter(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 20), color=colors[i])
        elif plottype == "bar":
            ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=wrap_text(legend_mapping[category], 20), width=0.1, color=colors[i])
        else:
            raise ValueError("Unsupported plot type")

    # Set x-axis to only show integers
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(labelsize=10, labelcolor=labelcolor, labelfontfamily="Helvetica")
    ax.set_title("Health Care Cost Over Time", color=labelcolor, fontname="Helvetica")
    ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
    ax.set_ylabel("Health Care Cost", color=labelcolor, fontname="Helvetica")

    # Apply custom formatter to y-axis to display bn
    ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

    # Adjust the layout to make room for the legend
    fig.subplots_adjust(right=0.75)

    # Position the legend outside the plot area with Helvetica font
    legend = ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})
    legend.get_title().set_fontsize('12')  # Optional: set the title font size
    legend.get_title().set_fontname('Helvetica')  # Optional: set the title font family

    return fig

if __name__ == "__main__":
    # import data
    data = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")

    # define face and label colour
    facecolor = "#FFFFFF"
    labelcolor = "#000000"
    plottype = "scatter"
    selectedcountry = "CHE"

    fig = display_data(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023)

    if fig == "NO DATA":
        print("No data available for the selected filters.")
    else:
        # Display the figure
        canvas = FigureCanvas(fig)
        canvas.draw()

        plt.figure(figsize=(10, 6))
        plt.imshow(canvas.buffer_rgba())
        plt.axis('off')
        plt.show()