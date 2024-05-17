# main code starts on line XXX
# make sure to pip install all necessary libraries from the requirements.txt by using pip install -r requirements.txt

# import necessary libraries
import customtkinter as ctk
from PIL import Image
import pandas as pd
from oecd_countries import oecd_countries, oecd_images, oecd_iso_access
import os
import importlib


# define styles and colors
ctk.set_appearance_mode("system")  # sets mode to either light, dark or system settings
ctk.set_default_color_theme("green")  # sets default color theme to green, from green, blue and dark blue
main_color = "#137C4C"
secondary_color = "#1ABE73"
widget_bg_dark = "#5D5D5D"
widget_bg_light = "#C2C2C2"

white = "#FFFFFF"
black = "#000000"
light_grey = "#ABB0B5"
dark_grey = "#4B4D50"

# check whether necessary data needs to be imported

# list of necessary files
file_paths = ["Data/Doctors_Region.csv", "Data/HC_Market.csv", "Data/HC_Market_meaning.csv"]

# check if all files exist
if not all(os.path.exists(file_path) for file_path in file_paths):

    class Root(ctk.CTk):  # create window for progress bar
        def __init__(self):
            super().__init__()

            # set title and geometry of root
            self.title("App Name")
            self.geometry("400x200")

            # create descriptive label
            self.csv_download_label = ctk.CTkLabel(self, text="Downloading data...", font=("Helvetica Bold", 18))
            self.csv_download_label.pack(pady=30)

            # create progress bar
            self.csv_pb = ctk.CTkProgressBar(self, width=250, progress_color=main_color)
            self.csv_pb.pack(pady=10)
            self.csv_pb.set(0)

            # create progress label
            self.csv_progress_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12))
            self.csv_progress_label.pack(pady=30)

            # start the download process
            self.after(100, self.start_download)  # add some time for gui to initialize

        def start_download(self):  # set up labels and progress bar to start importing
            self.csv_progress_label.configure(text="Importing module...")
            self.csv_pb.set(0)
            self.after(100, self.import_module)  # continue with next function

        def import_module(self):  # import the necessary functions to load data
            global load_basic_oecd_data, load_oecd_med_data
            module = importlib.import_module('total_data')
            load_basic_oecd_data = module.load_basic_oecd_data
            load_oecd_med_data = module.load_oecd_med_data
            self.csv_progress_label.configure(text="Loading basic OECD data...")
            self.csv_pb.set(0.33)
            self.after(500, self.load_basic_data)  # Wait 0.5 second before next step

        def load_basic_data(self):  # load in basic oecd data
            self.csv_progress_label.configure(text="Loading med OECD data...")
            load_basic_oecd_data()
            self.csv_pb.set(0.66)
            self.after(1000, self.load_med_data)  # Wait 1 second before next step

        def load_med_data(self):  # load in med data
            load_oecd_med_data()
            self.csv_pb.set(1.0)  # set progress to 100% when finished
            self.csv_download_label.configure(text="Download finished. Main app initializing...",
                                              font=("Helvetica Bold", 16))
            self.csv_progress_label.configure(text="Loading data finished.")
            self.after(3000,
                       self.close_window)  # Wait 5 second before closing to give time to read further instructions

        def close_window(self):
            self.destroy()
            print("All necessary files created.")


    root = Root()
    root.mainloop()

else:
    print("All necessary files in directory.")

# create dataframe from .csv files
master_df = pd.read_csv("Data/HC_Market.csv").set_index("REF_AREA")

# initialize SubFrame class for general information display
class SubFrame(ctk.CTkFrame):
    def __init__(self, master, text="", text2="-", **kwargs):
        # set default values for geometry and layout
        super().__init__(master, width=170, height=80, corner_radius=15, fg_color=secondary_color, **kwargs)
        # create label to label data displayed
        self.gi_datalabel = ctk.CTkLabel(self, text=text, font=("Helvetica Bold", 16), fg_color="transparent", text_color=white)
        self.gi_datalabel.place(x=85, y=10, anchor="n")
        self.pack_propagate(False)  # stop the frame from resizing to fit the label

        # create label to display the data
        self.gi_data = ctk.CTkLabel(self, text=text2, font=("Helvetica", 14), fg_color="transparent", text_color=white)
        self.gi_data.place(x=85, y=40, anchor="n")

    # define function to change displayed data in gi_data
    def change_gi_data(self, new_data):
        self.text2 = new_data
        self.gi_data.configure(text=self.text2)

# initialize frame class for cool sliders with labels
class Sliders(ctk.CTkFrame):
    def __init__(self, master, steps, width, start, end, text, color_right, color_left):
        super().__init__(master, fg_color="transparent")
        # Create a slider
        self.slider = ctk.CTkSlider(self, width=width, number_of_steps=steps, from_=start, to=end, button_color=secondary_color,
                         button_hover_color=main_color, fg_color=color_right, progress_color=color_left,
                                    command=self.update_label)
        self.slider.pack()  #
        # Create a label to display the slider value
        self.slider_value_label = ctk.CTkLabel(self, text=text, font=("Helvetica", 12))
        self.slider_value_label.pack()

    # define function to update label text according to slider position
    def update_label(self, value):
        self.slider_value_label.configure(text=int(value))



# define main window

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # make master_df a class attribute
        self.master_df = master_df

        # window title and size
        self.title("App Name")
        self.geometry("1250x800")

        # header bar
        self.title_background = ctk.CTkCanvas(self, height=70, bg=main_color, highlightthickness=0)  # sets the background for a title font
        self.title_background.pack(
            fill="x")  # packs the background onto the main window, with variable width depending on window size
        self.title_text = ctk.CTkLabel(self, text="App Title", text_color=white, font=("Helvetica Bold", 24),
                                  fg_color=main_color)  # title text
        self.title_text.place(x=30, y=35, anchor="w")  # placement of title text

        # country dropdown menu
        self.country_dropdown = ctk.CTkComboBox(self, values=oecd_countries, hover=True, border_color=(widget_bg_light, widget_bg_dark),
                                           button_color=(widget_bg_light, widget_bg_dark), button_hover_color=main_color,
                                            command=self.display_country_data)
        self.country_dropdown.bind("<Return>", self.display_country_data)
        self.country_dropdown.place(x=20, y=90)

        # create filtering options

        # create frame for filter options
        self.filter_frame = ctk.CTkFrame(self, fg_color=(widget_bg_light, widget_bg_dark), height=500, width=140)
        self.filter_frame.place(x=20, y=130)

        # create title
        self.filter_title = ctk.CTkLabel(self.filter_frame, text="Filter Options", font=("Helvetica Bold", 18))
        self.filter_title.place(x=10, y=5)

        # create subtitle "from:"
        self.year_from = ctk.CTkLabel(self.filter_frame, text="from:", font=("Helvetica Bold", 12))
        self.year_from.place(x=10, y=38)

        # create slider to input from
        self.year_lower_limit = Sliders(self.filter_frame, steps=6, width=120, start=2015, end=2021, text="2018",
                                        color_right=light_grey, color_left="#4B4D50")
        self.year_lower_limit.place(x=10, y=70)

        # create subtitle "to:"
        self.year_from = ctk.CTkLabel(self.filter_frame, text="to:", font=("Helvetica Bold", 12))
        self.year_from.place(x=10, y=110)

        # create slider to input to
        self.year_upper_limit = Sliders(self.filter_frame, steps=6, width=120, start=2015, end=2021, text="2018",
                                        color_right=dark_grey, color_left=light_grey)
        self.year_upper_limit.place(x=10, y=142)

        # design the general information frame
        self.country_title = ctk.CTkLabel(self, text="", font=("Helvetica Bold", 24))  # create label for country name
        self.country_title.place(x=185, y=90)

        self.gi_frame = ctk.CTkFrame(self, fg_color=(widget_bg_light, widget_bg_dark), height=120, width=1050)  # create window to display information
        self.gi_frame.place(x=180, y=130)

        self.dc_label = ctk.CTkLabel(self.gi_frame, text="")  # create label for country image
        self.dc_label.place(x=30, y=20, anchor="nw")

        # indicate when the data is from in gi_frame
        self.dd_label = ctk.CTkLabel(self.gi_frame, text="", font=("Helvetica", 10), text_color=(white, widget_bg_light))
        self.dd_label.place(x=950, y=-4)

        # instanciate subframes to display data
        self.subframepopulation = SubFrame(self.gi_frame, text="Population")  # display population data
        self.subframepopulation.place(x=140, y=20)

        self.subframegdp = SubFrame(self.gi_frame, text="GDP (bn $)")  # display GDP
        self.subframegdp.place(x=320, y=20)

        self.subframegdppc = SubFrame(self.gi_frame, text="GDP per Capita ($)") # display GDP per capita
        self.subframegdppc.place(x=500, y=20)

        self.subframecurrency = SubFrame(self.gi_frame, text="Currency")  # display currency
        self.subframecurrency.place(x=680, y=20)

        self.subframelanguages = SubFrame(self.gi_frame, text="Language")  # display languages
        self.subframelanguages.place(x=860, y=20)

    # define functions to display information

    def display_country_data(self, event=None):  # main function that runs all other functions
        self.display_general_information()

    def display_general_information(self):

        # read input from dropdown menu
        country_ddmenu_choice = self.country_dropdown.get().lower()

        # display country title
        cc2 = country_ddmenu_choice.title()  # ensure that all words from the input are capitalized (choice capitalized)
        if cc2 in oecd_countries:
            self.country_title.configure(text=cc2)
        else:
            pass

        # modify dd_label to show which year the data is from
        self.dd_label.configure(text="Data from 2021")

        # display country image
        cip = oecd_images.get(country_ddmenu_choice)  # find image path (cip = chosen image path)
        if cip is None:  # handle inputs in the dropdown that have no equivalent in the dictionary
            return
        try:  # create and display image label
            country_image = ctk.CTkImage(light_image=Image.open(cip), dark_image=Image.open(cip), size=(80, 80))
            # configure CTkLabel with image
            self.dc_label.configure(image=country_image, text='')
            # display image
            self.dc_label.place()
        # handle file not found error --> it does not really work just yet; it does not properly reset the function
        except FileNotFoundError:
            self.dc_label.configure(image=None, text="No image", font=("Helvetica", 18))  # Handle file not found error
            self.dc_label.place()
            return

        # display population
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        population_data = self.master_df.loc[gic]["Population"][0]  # get population data from dataframe
        new_data = '{:,.0f}'.format(population_data * 1e6)  # multiply to get to actual population; format
        self.subframepopulation.change_gi_data(new_data)  # update gi_data label

        # display gdp
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        gdp_data = self.master_df.loc[gic]["GDP (bn USD)"][0]  # get gdp data from dataframe
        new_data = '{:,.2f}'.format(gdp_data)  # round and format
        self.subframegdp.change_gi_data(new_data)  # update gi_data label

        # display gdp per capita
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        gdppc_data = self.master_df.loc[gic]["GDP per Capita (USD)"][0]  # get gdp per capita data from dataframe
        new_data = '{:,.2f}'.format(gdppc_data)  # round and format
        self.subframegdppc.change_gi_data(new_data)  # update gi_data label

        # display currency
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        new_data = self.master_df.loc[gic]["Currency"][0]  # get gdp data from dataframe
        self.subframecurrency.change_gi_data(new_data)  # update gi_data label

        # display Language
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        new_data = self.master_df.loc[gic]["Language"][0]  # get language data from dataframe
        self.subframelanguages.change_gi_data(new_data)  # update gi_data label


# execute customtkinter
app = App()
app.mainloop()
