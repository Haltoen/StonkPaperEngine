import matplotlib.pyplot as plt
import mplfinance as mpf 

import ApiHandler as api 

colors = mpf.make_marketcolors(up="#00ff00",
                               down="#ff0000",
                               wick="inherit",
                               edge="inherit",
                               volume="in")

cutom_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

def make_plot (data, show_volume, logarithmic): 
    fig, axlist = mpf.plot(data ,type="candle", style = cutom_style, volume=show_volume, returnfig=True)
    if logarithmic:
        ax = axlist[0]
        ax.set_yscale('log')
    return fig


data = api.data_request("BTC", 20, "1wk")

fig = make_plot(data, False, True)

# Set the background image filename (adjust the filename and path as needed)
background_image_filename = 'background_image.png'

# Save the figure as an image file
fig.patch.set_facecolor('white')
fig.savefig(background_image_filename)  


import ctypes
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, background_image_filename, 3)