from matplotlib.figure import Figure
import pandas as pd
from matplotlib.ticker import MaxNLocator, FuncFormatter, PercentFormatter
import textwrap

def wrap_text(text, width):  # wrap text of long legends
    wrapped_lines = textwrap.wrap(text, width=width, break_long_words=False, replace_whitespace=False)
    return '\n'.join(wrapped_lines)

def currency_formatter(x, pos):  # format y-axis to display bn $
    return f'${x*1e-9:.1f}bn'

def add_new_column_if_not_exists(data):  # add new data columns
    new_column_name = 'PT_SL_VAL_TOTAL'
    if new_column_name not in data.columns:
        if 'PT_SL_VAL_M' in data.columns and 'TOTAL_PHARM' in data.columns:
            data[new_column_name] = data['PT_SL_VAL_M'] * data['TOTAL_PHARM']
        else:
            raise ValueError("Required columns 'PT_SL_VAL_M' and 'TOTAL_PHARM' are missing in the data")
    return data

def add_meaning_to_csv(csv_path, column_name, meaning):
    # Read the existing CSV file
    df = pd.read_csv(csv_path)

    # Check if the column name already exists in the DataFrame
    if column_name not in df.columns:
        # Append a new row with the column name and its meaning
        new_row = pd.DataFrame([[column_name, meaning]], columns=["Column name", "Meaning"])
        df = pd.concat([df, new_row], ignore_index=True)
        # Write the updated DataFrame back to the CSV file
        df.to_csv(csv_path, index=False)


# display data for graph 1
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

# display data for graph 2

# display data for graph 3
def display_data_3(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[(data.TIME_PERIOD <= selectedtimeend) & (data.TIME_PERIOD >= selectedtimestart)]  # filter years

    if len(data) == 0:
        print("no data")
        return "NO DATA"

    # remove the doubled columns
    data.rename(columns={"HC511_x": "HC511", "HC512_x": "HC512"}, inplace=True)

    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

    # Create plot
    fig = Figure(figsize=(8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["HC511", "HC512"]
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
    ax.set_title("Expenditure Prescription vs OTC Over Time", color=labelcolor, fontname="Helvetica")
    ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
    ax.set_ylabel("Expenditure", color=labelcolor, fontname="Helvetica")

    # Apply custom formatter to y-axis to display bn
    ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

    # Adjust the layout to make room for the legend
    fig.subplots_adjust(right=0.75)

    # Position the legend outside the plot area with Helvetica font
    legend = ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})
    legend.get_title().set_fontsize('12')  # set the title font size
    legend.get_title().set_fontname('Helvetica')  # set the title font family

    return fig

# display data for graph 4 (inactive)
def display_data_4(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015, selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[(data.TIME_PERIOD <= selectedtimeend) & (data.TIME_PERIOD >= selectedtimestart)]  # filter years

    if len(data) == 0:
        print("no data")
        return "NO DATA"

    # remove the doubled columns
    data.rename(columns={"HC511_x": "HC511", "HC512_x": "HC512"}, inplace=True)

    # divide by population to get per capita value
    data["HC511"] = data["HC511"] / data["Population"]
    data["HC512"] = data["HC512"] / data["Population"]

    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

    # Create plot
    fig = Figure(figsize=(8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["HC511", "HC512"]
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
    ax.set_title("Expenditure Prescription vs OTC Over Time", color=labelcolor, fontname="Helvetica")
    ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
    ax.set_ylabel("Expenditure", color=labelcolor, fontname="Helvetica")

    # Apply custom formatter to y-axis to display bn
    ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

    # Adjust the layout to make room for the legend
    fig.subplots_adjust(right=0.75)

    # Position the legend outside the plot area with Helvetica font
    legend = ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})
    legend.get_title().set_fontsize('12')  # set the title font size
    legend.get_title().set_fontname('Helvetica')  # set the title font family

    return fig

# display data for graph 5
def display_data_5(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015,
                   selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[data.TIME_PERIOD <= selectedtimeend]  # filter end year
    data = data[data.TIME_PERIOD >= selectedtimestart]  # filter end year

    if len(data) == 0:
        print("no data")
        fig = "NO DATA"
        return fig

    else:
        # import legend
        legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

        # Create a dictionary mapping categories to their explanations
        legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

        # Create plot
        fig = Figure(figsize=(8, 4), facecolor=facecolor)
        ax = fig.add_subplot()

        colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

        categories = ["PT_SL_VOL_M"]
        for i, category in enumerate(categories):
            data[category] = data[category] * 100  # Convert to percentage
            if plottype == "line":
                ax.plot(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15), color=colors[i])
            elif plottype == "scatter":
                ax.scatter(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15),
                           color=colors[i])
            elif plottype == "bar":
                ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=wrap_text(legend_mapping[category], 15),
                       width=0.5,
                       color=colors[i])
            else:
                raise ValueError("Unsupported plot type")

        # Set x-axis to only show integers
        from matplotlib.ticker import MaxNLocator
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Set y-axis labels to percentages
        ax.yaxis.set_major_formatter(PercentFormatter())

        ax.tick_params(labelsize=10, labelcolor=labelcolor, labelfontfamily="Helvetica")
        ax.set_title("Generic penetration in volume (in %)", color=labelcolor, fontname="Helvetica")
        ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
        ax.set_ylabel("Volume of pharmaceutical sales", color=labelcolor, fontname="Helvetica")

        # adjust layout to make room for legend
        fig.subplots_adjust(right=0.75)
        # Position the legend underneath the plot
        ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})

        return fig

# display data for graph 6
def display_data_6(facecolor, labelcolor, data, plottype, selectedcountry, selectedtimestart=2015,
                   selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[data.TIME_PERIOD <= selectedtimeend]  # filter end year
    data = data[data.TIME_PERIOD >= selectedtimestart]  # filter end year

    if len(data) == 0:
        return "NO DATA"

    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

    # Create plot
    fig = Figure(figsize=(8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["PT_SL_VAL_M"]
    for i, category in enumerate(categories):
        data[category] = data[category] * 100  # Convert to percentage
        if plottype == "line":
            ax.plot(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15), color=colors[i])
        elif plottype == "scatter":
            ax.scatter(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15),
                       color=colors[i])
        elif plottype == "bar":
            ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=wrap_text(legend_mapping[category], 15),
                   width=0.5,
                   color=colors[i])
        else:
            raise ValueError("Unsupported plot type")

    # Set x-axis to only show integers
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Set y-axis labels to percentages
    ax.yaxis.set_major_formatter(PercentFormatter())

    ax.tick_params(labelsize=10, labelcolor=labelcolor, labelfontfamily="Helvetica")
    ax.set_title("Generic penetration in value (in %)", color=labelcolor, fontname="Helvetica")
    ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
    ax.set_ylabel("Value of pharmaceutical sales", color=labelcolor, fontname="Helvetica")

    # adjust layout to make room for legend
    fig.subplots_adjust(right=0.75)
    # Position the legend underneath the plot
    ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})

    return fig

# display data for graph 7
def display_data_7(facecolor, labelcolor, data, plottype, selectedcountry="GER", selectedtimestart=2015,
                   selectedtimeend=2023):
    # filter data
    data = data[data.index.values == selectedcountry]  # filter country
    data = data[data.TIME_PERIOD <= selectedtimeend]  # filter end year
    data = data[data.TIME_PERIOD >= selectedtimestart]  # filter end year

    if len(data) == 0:
        return "NO DATA"

    # Add new column if not exists
    data = add_new_column_if_not_exists(data)

    # Call the function to add meaning to the CSV file
    add_meaning_to_csv("Data/HC_Market_meaning.csv", "PT_SL_VAL_TOTAL", "Generic pharmaceuticals spend per capita")

    # import legend
    legendnames = pd.read_csv("Data/HC_Market_meaning.csv")

    # Read population data
    population_data = pd.read_csv("Data/population_filtered.csv")

    # Merge population data with your existing DataFrame
    data = pd.merge(data, population_data, on=["REF_AREA", "TIME_PERIOD"], how="left")

    # Calculate spend per capita
    data["PT_SL_VAL_TOTAL"] = data["PT_SL_VAL_TOTAL"] / data["Total_Population"]

    # Create a dictionary mapping categories to their explanations
    legend_mapping = dict(zip(legendnames["Column name"], legendnames["Meaning"]))

    # Create plot
    fig = Figure(figsize=(8, 4), facecolor=facecolor)
    ax = fig.add_subplot()

    colors = ["#137C4C", "#1E88E5", "#D32F2F", "#8E24AA", "#FDD835", "#43A047", "#FB8C00", "#3949AB"]

    categories = ["PT_SL_VAL_TOTAL"]
    for i, category in enumerate(categories):
        data[category] = data[category]
        if plottype == "line":
            ax.plot(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15), color=colors[i])
        elif plottype == "scatter":
            ax.scatter(data["TIME_PERIOD"], data[category], label=wrap_text(legend_mapping[category], 15),
                       color=colors[i])
        elif plottype == "bar":
            ax.bar(data["TIME_PERIOD"] + i * 0.1, data[category], label=wrap_text(legend_mapping[category], 15),
                   width=0.5,
                   color=colors[i])
        else:
            raise ValueError("Unsupported plot type")

    # Set x-axis to only show integers
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.tick_params(labelsize=10, labelcolor=labelcolor, labelfontfamily="Helvetica")
    ax.set_title("Generic spend per capita (in dollars)", color=labelcolor, fontname="Helvetica")
    ax.set_xlabel("Year", color=labelcolor, fontname="Helvetica")
    ax.set_ylabel("Value of pharmaceutical sales", color=labelcolor, fontname="Helvetica")

    # adjust layout to make room for legend
    fig.subplots_adjust(right=0.75)
    # Position the legend underneath the plot
    ax.legend(title="Categories", loc='center left', bbox_to_anchor=(1, 0.5), prop={'family': 'Helvetica'})

    return fig
