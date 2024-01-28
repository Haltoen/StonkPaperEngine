import matplotlib.pyplot as plt
import mplfinance as mpf 
import os
import ctypes

import ApiHandler as api 

colors = mpf.make_marketcolors(up="#00ff00",
                               down="#ff0000",
                               wick="inherit",
                               edge="inherit",
                               volume="in")

custom_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

data = api.data_request("BTC-USD", 20, "1wk")

width = 1920  # Replace with your desired width
height = 1080  # Replace with your desired height

def plot_as_background(data, custom_style, show_volume, logarithmic, width, height):
    # Create a new figure with the specified width and height
    fig, axlist = mpf.plot(data, type="candle", style=custom_style, volume=show_volume, returnfig=True)

    # Set the facecolor of the figure to be white (non-transparent)
    fig.patch.set_facecolor('white')

    # Set the DPI based on the specified width and height
    dpi_value = int(width / fig.get_size_inches()[0])
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


def simple_plot (data, show_volume, logarithmic):
    plot_as_background(data, custom_style, show_volume, logarithmic, width, height)