# main code starts on line XXX
# make sure to pip install all necessary libraries from the requirements.txt by using pip install -r requirements.txt

# import necessary libraries
import customtkinter as ctk
from PIL import Image
import pandas as pd
import os
import importlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from oecd_countries import oecd_countries, oecd_images, oecd_iso_access, cross_country_graphs
from display_graphs_backend_template import display_data
from graph_3 import display_data_3
from countryselect import CountrySelect, preselected_countries, selected_countries


# define styles and colors
ctk.set_appearance_mode("dark")  # sets mode to either light, dark or system settings
ctk.set_default_color_theme("green")  # sets default color theme to green, from green, blue and dark blue
main_color = "#137C4C"
secondary_color = "#1ABE73"
widget_bg_dark = "#5D5D5D"
window_bg_dark = "#242524"
widget_bg_light = "#C2C2C2"

white = "#FFFFFF"
black = "#000000"
light_grey = "#ABB0B5"
dark_grey = "#343638"

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

# create SubFrame class for general information display
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

# create frame class for cool sliders with labels
class Sliders(ctk.CTkFrame):
    def __init__(self, master, steps, width, start, end, color_right, color_left, default_value=None, command=None):
        super().__init__(master, fg_color="transparent")
        # Internal function to handle slider value changes
        def slider_command(value):
            # Call the external command if it exists
            if command:
                command(value)
            # Update the label with the new value
            else:
                self.update_label(value)
        # Create a slider
        self.slider = ctk.CTkSlider(self, width=width, number_of_steps=steps, from_=start, to=end, button_color=secondary_color,
                         button_hover_color=main_color, fg_color=(color_left, color_right),
                                    progress_color=(color_right, color_left), command=slider_command)
        self.slider.pack()  # display slider

        # Create a label to display the slider value
        self.slider_value_label = ctk.CTkLabel(self, text=default_value, font=("Helvetica", 12))
        self.slider_value_label.pack()

        # set slider to default value if provided, else set to center value
        if default_value is not None:
            self.slider.set(default_value)
            self.update_label(default_value)
        else:
            self.slider.set((start + end) / 2)
            self.update_label((start + end) / 2)

    # define function to update label text according to slider position
    def update_label(self, value):
        self.slider_value_label.configure(text=int(value))


# create top level window class to display messages if needed

class MessageWindow(ctk.CTkToplevel):
    def __init__(self, title, message, label):
        super().__init__()
        self.geometry("400x340")
        self.title(title)

        self.grid_rowconfigure(2, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.message_window_label = ctk.CTkLabel(master=self, text=label, font=("Helvetica Bold", 18))
        self.message_window_label.grid(row=0, column=0, padx=30, pady=30, sticky="nw")

        self.textbox = ctk.CTkTextbox(master=self, width=400, height=160, corner_radius=5, fg_color=window_bg_dark)  # add message in text box
        self.textbox.grid(row=1, column=0, padx=25, sticky="")
        self.textbox.insert("1.0", message)

        self.button = ctk.CTkButton(master=self, text="Close", command=self.destroy)  # add button to close window
        self.button.grid(row=2, column=0, pady=10, sticky="")


# define main window

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # make master_df a class attribute
        self.master_df = master_df

        # window title and size
        self.title("App Name")
        self.geometry("1250x1000")

        # header bar
        self.title_background = ctk.CTkCanvas(self, height=70, bg=main_color, highlightthickness=0)  # sets the background for a title font
        self.title_background.pack(
            fill="x")  # packs the background onto the main window, with variable width depending on window size

        self.title_image = ctk.CTkImage(light_image=Image.open("Images/Logos/Health_Explorer_Label.png"),
                                        dark_image=Image.open("Images/Logos/Health_Explorer_Label.png"),
                                        size=(320, 62.5))  # title image
        self.title_image_container = ctk.CTkLabel(self, image=self.title_image, text="", fg_color=main_color)  # container for title image
        self.title_image_container.place(x=12, y=35, anchor="w")  # placement of title image

        # change from dark to light mode
        self.darklight = ctk.CTkButton(self, width=80, text="Change Mode", text_color=white, font=("Helvetica", 12),
                                       border_color=white, border_width=1, bg_color=main_color, fg_color=main_color,
                                       command=self.change_mode)
        self.darklight.place(x=1185, y=35, anchor="center")

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

        # create title for frame
        self.filter_title = ctk.CTkLabel(self.filter_frame, text="Filter Options", font=("Helvetica Bold", 18))
        self.filter_title.place(x=10, y=5)

        # create subtitle "Choose graph to update:"
        self.graph_update_label = ctk.CTkLabel(self.filter_frame, text="Choose graph to update:", font=("Helvetica Bold", 10))
        self.graph_update_label.place(x=10, y=38)

        # create option menu to choose which graph to update
        self.graph_update_menu = ctk.CTkOptionMenu(self.filter_frame, values=["Graph 1", "Graph 2", "Graph 3", "Graph 4"],
                                            width=120, hover=True, fg_color=(white, light_grey), button_color=(secondary_color),
                                            button_hover_color=main_color, text_color=black)
        self.graph_update_menu.place(x=10, y=70)

        # create subtitle "from:"
        self.year_from = ctk.CTkLabel(self.filter_frame, text="from:", font=("Helvetica Bold", 12))
        self.year_from.place(x=10, y=110)

        # create slider to input from
        self.year_lower_limit = Sliders(self.filter_frame, steps=7, width=120, start=2015, end=2022, default_value=2015,
                                        color_right=light_grey, color_left=dark_grey, command=self.update_upper_limit)
        self.year_lower_limit.place(x=10, y=142)

        # create subtitle "to:"
        self.year_to = ctk.CTkLabel(self.filter_frame, text="to:", font=("Helvetica Bold", 12))
        self.year_to.place(x=10, y=182)

        # create slider to input to
        self.year_upper_limit = Sliders(self.filter_frame, steps=7, width=120, start=2015, end=2022, default_value=2022,
                                        color_right=dark_grey, color_left=light_grey, command=self.update_upper_limit)
        self.year_upper_limit.place(x=10, y=214)
        self.year_upper_limit.slider.set(2022)

        # create label for "Graph Type:"
        self.graph_type_label = ctk.CTkLabel(self.filter_frame, text="Graph Type:", font=("Helvetica Bold", 12))
        self.graph_type_label.place(x=10, y=264)

        # create option menu for graph type
        self.graph_type_menu = ctk.CTkOptionMenu(self.filter_frame, values=["Line", "Bar", "Scatter", "Pie"],
                                        width=120, hover=True, fg_color=(white, light_grey), button_color=(secondary_color),
                                            button_hover_color=main_color, text_color=black)
        self.graph_type_menu.place(x=10, y=296)

        # create option to select countries
        self.select_country_button = ctk.CTkButton(self.filter_frame, text="Select Country", width=120, hover=True, fg_color=secondary_color, font=("Helvetica Bold", 12), command=self.open_country_selection)
        self.select_country_button.place(x=10, y=343)

        # create button to update graphs
        self.apply_button = ctk.CTkButton(self.filter_frame, width = 120, fg_color=main_color, hover=True, hover_color=secondary_color,
                                     text="Apply", text_color=white, font=("Helvetica Bold", 14), command=self.apply_filter)
        self.apply_button.place(x=70, y=388, anchor="n")

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

        # design the graph frame
        self.graph_frame = ctk.CTkScrollableFrame(self, height=615, width=1025, fg_color=(widget_bg_light, widget_bg_dark))
        self.graph_frame.place(x=180, y=270)

        # configure grid for graph frame (16x1)
        self.graph_frame.grid_rowconfigure(15, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # initialize message windows
        self.window_lge = None  # initializes line graph error message
        self.window_gte = None  # initializes graph type error message

    # define functions to display information

    def display_country_data(self, event=None):  # main function that runs all other functions
        self.display_general_information()
        self.display_graph_1()
        self.display_graph_3()

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

        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe

        # display population
        population_data = self.master_df.loc[gic]["Population"][0]  # get population data from dataframe
        new_data = '{:,.0f}'.format(population_data * 1e6)  # multiply to get to actual population; format
        self.subframepopulation.change_gi_data(new_data)  # update gi_data label

        # display gdp
        gdp_data = self.master_df.loc[gic]["GDP (bn USD)"][0]  # get gdp data from dataframe
        new_data = '{:,.2f}'.format(gdp_data)  # round and format
        self.subframegdp.change_gi_data(new_data)  # update gi_data label

        # display gdp per capita
        gdppc_data = self.master_df.loc[gic]["GDP per Capita (USD)"][0]  # get gdp per capita data from dataframe
        new_data = '{:,.2f}'.format(gdppc_data)  # round and format
        self.subframegdppc.change_gi_data(new_data)  # update gi_data label

        # display currency
        new_data = self.master_df.loc[gic]["Currency"][0]  # get gdp data from dataframe
        self.subframecurrency.change_gi_data(new_data)  # update gi_data label

        # display Language
        gic = oecd_iso_access.get(country_ddmenu_choice.title())  # get iso country code (gic) to access dataframe
        new_data = self.master_df.loc[gic]["Language"][0]  # get language data from dataframe
        self.subframelanguages.change_gi_data(new_data)  # update gi_data label

    def display_graph_1(self, plottype="scatter", selectedtimestart=2015, selectedtimeend=2022):  # display Expenditure in health care across all areas of care
        print("started creating canvas 1!")  # test print

        # check for line graph error
        if plottype == "line" and selectedtimestart == selectedtimeend:
            self.open_line_graph_error()
            return

        try:
            # create variables
            selectedcountry = oecd_iso_access.get(self.country_dropdown.get().title())

            # pass different colors depending on mode
            if ctk.get_appearance_mode() == "Light":
                facecolor = widget_bg_light
            elif ctk.get_appearance_mode() == "Dark":
                facecolor = widget_bg_dark
            else:
                facecolor = widget_bg_light

            if ctk.get_appearance_mode() == "Light":
                labelcolor = black
            elif ctk.get_appearance_mode() == "Dark":
                labelcolor = white
            else:
                labelcolor = black

            # Call the function that returns the Matplotlib plot
            plot = display_data(facecolor, labelcolor, master_df, plottype, selectedcountry, selectedtimestart, selectedtimeend)

            if not hasattr(self, "graph_1_name"):
                self.graph_1_name = ctk.CTkLabel(self.graph_frame,
                                                 text="Health Care Cost Over Time (Graph 1)",
                                                 font=("Helvetica Bold", 24))
                self.graph_1_name.grid(row=0, column=0, sticky="w", padx=20, pady=20)

            # destroy old graph if it exists
            if hasattr(self, "canvas1"):
                self.canvas1.get_tk_widget().destroy

            # Create a canvas widget
            canvas1 = FigureCanvasTkAgg(plot, master=self.graph_frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        except ValueError:
            self.open_graph_type_error()
            return

    # display expenditure of prescription vs otc
    def display_graph_3(self, plottype="line", selectedtimestart=2015, selectedtimeend=2022):  # display expenditure of prescription vs otc
        print("started creating canvas 3!")  # test print

        # check for line graph error
        if plottype == "line" and selectedtimestart == selectedtimeend:
            self.open_line_graph_error()
            return

        try:
            # create variables
            selectedcountry = oecd_iso_access.get(self.country_dropdown.get().title())

            # pass different colors depending on mode
            if ctk.get_appearance_mode() == "Light":
                facecolor = widget_bg_light
            elif ctk.get_appearance_mode() == "Dark":
                facecolor = widget_bg_dark
            else:
                facecolor = widget_bg_light

            if ctk.get_appearance_mode() == "Light":
                labelcolor = black
            elif ctk.get_appearance_mode() == "Dark":
                labelcolor = white
            else:
                labelcolor = black

            # Call the function that returns the Matplotlib plot
            plot = display_data_3(facecolor, labelcolor, master_df, plottype, selectedcountry, selectedtimestart, selectedtimeend)

            # create a UI title for the graph if it does not exist
            if not hasattr(self, "graph_3_name"):
                self.graph_3_name = ctk.CTkLabel(self.graph_frame, text="Expenditure in Prescription (Rx) vs Over-The-Counter (OTC) Over Time (Graph 3)",
                                             font=("Helvetica Bold", 24))
                self.graph_3_name.grid(row=2, column=0, sticky="w", padx=20, pady=20)

            # destroy old graph if it exists
            if hasattr(self, "canvas3"):
                self.canvas3.get_tk_widget().destroy

            # Create a canvas widget
            canvas3 = FigureCanvasTkAgg(plot, master=self.graph_frame)
            canvas3.draw()
            canvas3.get_tk_widget().grid(row=3, column=0, sticky="nsew")

        except ValueError:
            self.open_graph_type_error()
            return

    # create function to choose countries
    def open_country_selection(self):
        country_selection_window = CountrySelect(self, countries=oecd_countries, preselected=preselected_countries)
    # create function for the apply button
    def apply_filter(self):
        self.check_graph_update = self.graph_update_menu.get()  # get value from graph update menu

        if self.check_graph_update in cross_country_graphs:  # check whether we need selected countries
            if not selected_countries: # trigger error if no countries are selected
                self.open_no_countries_selected_error()
                return

        plottype = self.graph_type_menu.get().lower()
        selectedtimestart = self.year_lower_limit.slider.get()
        selectedtimeend = self.year_upper_limit.slider.get()

        # create dictionary to store function references
        graph2function = {
            "Graph 1": self.display_graph_1,
            "Graph 3": self.display_graph_3,
        }

        # Get the correct function reference from the dictionary
        self.run_function = graph2function.get(self.check_graph_update)

        # Call the function with the provided arguments
        self.run_function(plottype, selectedtimestart, selectedtimeend)

    # create function for lower limit slider stay the lower limit
    def update_upper_limit(self, value):
    # Get the current values of the sliders
        lower_limit_value = self.year_lower_limit.slider.get()
        upper_limit_value = self.year_upper_limit.slider.get()

        # Check if the upper limit value is less than the lower limit value
        if upper_limit_value < lower_limit_value:
            # Set the upper limit slider to the same value as the lower limit slider
            self.year_upper_limit.slider.set(lower_limit_value)
            self.year_upper_limit.update_label(lower_limit_value)
            # ensure that lower label also gets updated, as the update_label function is skipped in the class
            self.year_lower_limit.update_label(lower_limit_value)
        else:
            # update labels in other cases
            self.year_lower_limit.update_label(lower_limit_value)
            self.year_upper_limit.update_label(upper_limit_value)

    def change_mode(self):
        global mode
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            ctk.set_appearance_mode("light")
            mode = "Light"
        elif mode == "Light":
            ctk.set_appearance_mode("dark")
            mode = "Dark"
        self.display_country_data()

    # define error messages
    def open_line_graph_error(self):  # is raised when minimum and maximum year are the same and no line can be drawn
        if self.window_lge is None or not self.window_lge.winfo_exists():
            self.window_lge = MessageWindow(title="Line Graph Error", message="Line graphs cannot be displayed for one year.\n"
                                                                               "Please choose longer time period.",
                                            label="Line Graph Error")
            self.window_lge.grab_set()  # make window modal
            self.window_lge.focus_set()  # set focus to window
            self.window_lge.transient(self)  # make window not disappear
            self.window_lge.wait_window()  # wait until window is closed
        else:
            self.window_lge.focus_set()

    def open_graph_type_error(self):  # is raised when a plot type unavailable in the backend function is chosen
        if self.window_gte is None or not self.window_gte.winfo_exists():
            self.wrong_graphtype = self.graph_type_menu.get().title()
            # create new instance of Message class
            self.window_gte = MessageWindow(title="Graph Type Error", message=f"The graph type '{self.wrong_graphtype}' is not available for this graph.\n"
                                                                             f"Please choose a different one.",
                                            label="Graph Type Error")
            self.window_gte.grab_set()  # make window modal
            self.window_gte.focus_set()  # set focus to window
            self.window_gte.transient(self)  # make window not disappear
            self.window_gte.wait_window()  # wait until window is closed
        else:
            self.window_gte.focus_set()

    def open_no_countries_selected_error(self):  # is raised when a graph requires selected countries, but none are selected
        if self.window_ncs is None or not self.window_ncs.winfo_exists():
            # create new instance of Message class
            self.window_ncs = MessageWindow(title="No Countries Selected Error", message=f"This graph requires selection of countries. Please select countries.",
                                            label="No Countries Selected Error")
            self.window_ncs.grab_set()  # make window modal
            self.window_ncs.focus_set()  # set focus to window
            self.window_ncs.transient(self)  # make window not disappear
            self.window_ncs.wait_window()  # wait until window is closed


# execute customtkinter
app = App()
app.mainloop()