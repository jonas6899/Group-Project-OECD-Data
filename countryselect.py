import customtkinter as ctk

# all countries selected with checkmarks
selected_countries = ["Switzerland"]

class CountrySelect(ctk.CTkToplevel):
    def __init__(self, master=None, countries=[], selected_countries=[]):
        super().__init__(master)
        self.title("Select Country")
        self.countries = countries
        self.selected_countries = selected_countries

        # Create check buttons for each country
        self.check_buttons = []
        self.index_var = 0
        for i, country in enumerate(self.countries):
            var_value = "on" if country in self.selected_countries else "off"
            self.var = ctk.StringVar(value=var_value)
            self.button = ctk.CTkCheckBox(self, text=country, variable=self.var, onvalue="on", offvalue="off")
            row = self.index_var // 3
            column = self.index_var % 3
            self.button.grid(row=row, column=column, padx=15, pady=10, sticky="nw")
            self.check_buttons.append(self.button)
            self.index_var += 1

        print(self.check_buttons)

        # Add a confirm button
        self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self.confirm)
        self.confirm_button.grid(row=row + 1, column=1, padx=10, pady=20, sticky="nsew")

    def confirm(self):
        self.selected_countries.clear()
        for button in self.check_buttons:
            if button.cget("variable").get() == "on":
                country_name = button.cget("text")
                self.selected_countries.append(country_name)
        print(self.selected_countries)
        self.destroy()
