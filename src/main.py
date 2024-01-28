## application layer

import customtkinter as ctk
import tkinter as tk
import ApiHandler as api
import Plots as my_plt



 
# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System") 
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
appWidth, appHeight = 600, 500
 
# App Class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.title("Stonkpaper Engine")
        self.geometry(f"{appWidth}x{appHeight}")
 
        # Ticker Label
        self.tickerLabel = ctk.CTkLabel(self,
                                      text="Ticker")
        self.tickerLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 
        # Ticker Entry Field
        self.tickerEntry = ctk.CTkEntry(self,
                         placeholder_text="Teja")
        self.tickerEntry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")
 
        # Years Label
        self.timeLabel = ctk.CTkLabel(self,
                                     text="years")
        self.timeLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")
 
        # Years Entry Field
        self.timeEntry = ctk.CTkEntry(self,
                            placeholder_text="18")
        self.timeEntry.grid(row=1, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")

 
        # Choice Label
        self.choiceLabel = ctk.CTkLabel(self,
                                        text="Options")
        self.choiceLabel.grid(row=2, column=0,
                              padx=20, pady=20,
                              sticky="ew")
        self.choice1 = ctk.CTkCheckBox(self, text="Show Volume")
        self.choice1.grid(row=2, column=1, padx=20,
                          pady=20, sticky="ew")
 
        self.choice2 = ctk.CTkCheckBox(self, text="Log y-axis")                               
        self.choice2.grid(row=2, column=2, padx=20, pady=20,
                          sticky="ew")
 
        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
                                         text="Generate Plot",
                                         command=self.button_clicked)
        self.generateResultsButton.grid(row=3, column=1,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        
    def button_clicked(self):
        ticker = self.tickerEntry.get()
        time = int(self.timeEntry.get())
        volume = self.choice1._check_state
        log = self.choice1._check_state
        data = api.data_request(ticker, time, "1wk")
        plot = my_plt.simple_plot(data, volume, log)
        return None


        


    #def scedule_plot
 
if __name__ == "__main__":
    app = App()
    app.mainloop()