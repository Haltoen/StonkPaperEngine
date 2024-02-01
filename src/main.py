## application layer

import customtkinter as ctk
import ApiHandler as api
import Plots as my_plt
import os 
import time
import multiprocessing

 
# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System") 
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
appWidth, appHeight = 600, 300


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



def schedule_plots(ticker, periods, period_size, volume, log):
    interval_seconds = 30
    first = True
    while True:
        last_execution_time = read_last_execution_time()
        current_time = time.time()

        if (current_time - last_execution_time >= interval_seconds and api.is_market_open(ticker)) or first :
            # get data
            data = api.data_request(ticker, periods, period_size)
            # update plot
            print("attempt at data retrival")
            my_plt.plot_as_background(data, ticker, volume, log)
            # Update last execution time
            write_last_execution_time(current_time)

        time.sleep(60)  # Sleep for 1 minute 

# converts periods entry filed to (int) days
def string_to_days(s: str) -> int:
    if s == "day": return 1
    elif s == "week": return 7
    elif s == "month": return 30
    elif s == "6-month": return 183
    elif s == "year": return 365
    elif s == "5-year": return 365 * 5
    elif s == "max": return 365*200

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
 
        # Period settings Label
        self.timeLabel = ctk.CTkLabel(self,
                                     text="Time and Granualarity")
        self.timeLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")
 
        # n periods field
        self.periodsEntry = ctk.CTkOptionMenu(self,
                            values = ["day", "week", "month", "6-month", "year", "5-year", "max"]
                            )
        
        self.periodsEntry.grid(row=1, column=1, 
                            padx=20, pady=20, sticky="ew")
        
        # period size field
        self.period_sizeEntry = ctk.CTkOptionMenu(self,
                            values = ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo", "3mo"]
                            )
        self.period_sizeEntry.grid(row=1, column=2,
                            padx=20, pady=20, sticky="ew")
        

 
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
        periods = string_to_days(self.periodsEntry.get())
        period_size = self.period_sizeEntry.get()
        volume = self.choice1._check_state
        log = self.choice2._check_state
        
        # Create a process for scheduling plots 
        plot_process = multiprocessing.Process(target=schedule_plots, args=(ticker, periods, period_size, volume, log))
        plot_process.start()
    
    def terminate_other_processes(self):
        current_process = multiprocessing.current_process()
        for process in multiprocessing.active_children():
            if process != current_process:
                process.terminate()
                process.join()  # Ensure the terminated process is cleaned up


if __name__ == "__main__":
    app = App()
    app.mainloop()