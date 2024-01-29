## application layer

import customtkinter as ctk
import tkinter as tk
import ApiHandler as api
import Plots as my_plt
import os 
import time
import multiprocessing
from datetime import datetime

 
# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System") 
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
appWidth, appHeight = 600, 500


# File to store the last execution time
state_file = 'last_execution.txt'

def read_last_execution_time():
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            return float(file.read().strip())
    else:
        return 0.0
    

def write_last_execution_time(current_time):
    with open(state_file, 'w') as file:
        file.write(str(current_time))



def schedule_plots(ticker, volume, log, data):
    interval_minutes = 30  # Change this to your desired interval in minutes
    interval_seconds = interval_minutes * 60
    first = True
    while True:
        last_execution_time = read_last_execution_time()
        current_time = time.time()

        if current_time - last_execution_time >= interval_seconds or first :
            # update plot
            print("attempt at data retrival")
            my_plt.simple_plot(data, volume, log)
            # Update last execution time
            write_last_execution_time(current_time)

        time.sleep(60)  # Sleep for 1 minute 


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
                         placeholder_text="BTC-USD")
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
                            placeholder_text="30")
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
                                         text="Set as Background",
                                         command=self.button_clicked)
        self.generateResultsButton.grid(row=3, column=1,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        
    def button_clicked(self):
        self.terminate_other_processes()

        ticker = self.tickerEntry.get()
        periods = int(self.timeEntry.get())
        volume = self.choice1._check_state
        log = self.choice2._check_state
        data = api.data_request(ticker, periods, "1wk")

        # Create a process for scheduling plots 
        plot_process = multiprocessing.Process(target=schedule_plots, args=(ticker, volume, log, data))
        plot_process.start()
        
        return None
    
    def terminate_other_processes(self):
        current_process = multiprocessing.current_process()
        for process in multiprocessing.active_children():
            if process != current_process:
                process.terminate()
                process.join()  # Ensure the terminated process is cleaned up



if __name__ == "__main__":
    app = App()
    app.mainloop()