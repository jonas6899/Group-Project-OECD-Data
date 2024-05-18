from matplotlib.figure import Figure
import pandas as pd
import numpy as np

# create dataframe from .csv files and set index to REF_AREA
master_df = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")
print("df created")

def display_data():

    # define columns
    columns_list = ["TIME_PERIOD", "HC0"]
    print(columns_list)

    # define country
    graph_index_store = "AUS"  # define g1_index_store as AUS, as we do not have a dropdown here
    print("graph_index set as AUS")

    # create data frame
    health_care_data = master_df.loc[graph_index_store][columns_list] # get health care data from dataframe
    print("health care data accessed!")

    # create plot
    fig = Figure(figsize = (4.5,4), facecolor="#FFFFFF")
    ax = fig.add_subplot()
    ax.set_facecolor("#C2C2C2")
    ax.fill_between(x=health_care_data["TIME_PERIOD"], y1=health_care_data["HC0"], y2=0, color="#137C4C")
    ax.tick_params(labelsize=10, labelcolor="black")
    ax.set_title("Health Care Cost Over Time", color="black")
    ax.set_xlabel("Year", color="black")
    ax.set_ylabel("Health Care Cost", color="black")

    return fig


# display_data()