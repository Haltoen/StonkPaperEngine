import matplotlib.pyplot as plt
import mplfinance as mpf 
import os
import ctypes
from screeninfo import get_monitors

import ApiHandler as api 

colors = mpf.make_marketcolors(up="#00ff00",
                               down="#ff0000",
                               wick="inherit",
                               edge="inherit",
                               volume="in")

custom_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

# Get information about the primary monitor
primary_monitor = get_monitors()[0]

# Retrieve width and height of the primary monitor
monitor_width = primary_monitor.width
monitor_height = primary_monitor.height
dpi_value = 96
figsize = (monitor_width / dpi_value, monitor_height / dpi_value)



def plot_as_background(data, ticker, show_volume, logarithmic):
    fig, axlist = mpf.plot(data, type="candle", style=custom_style, volume=show_volume, returnfig=True, figsize=figsize, )

    fig.suptitle(ticker, fontsize=20)

        # Extract the latest closing price from the 'Close' column in your data
    latest_close_price = data['Close'].iloc[-1]

    # Add a text annotation under the title with the current price
    fig.text(0.5, 0.9, f'Current Price: ${latest_close_price:.2f}', ha='center', fontsize=12)
    # Set the facecolor of the figure to be white (non-transparent)
    fig.patch.set_facecolor('white')

    # Set the DPI based on the specified width and height
    fig.set_dpi(dpi_value)

    # Set logarithmic scaling for the y-axis if requested
    if logarithmic:
        ax = axlist[0]
        ax.set_yscale('log')


    # Save the figure as an image file
    background_image_filename = 'background_image.png'
    fig.savefig(background_image_filename, dpi=dpi_value)

    ctypes.windll.user32.SystemParametersInfoW(20,0,os.path.abspath(background_image_filename),0)

    return fig

