from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def get_ux(device:str)->str:
    """
    Get the UX from the device.

    Args:
        device (str): Device used for purchasing.

    Returns:
        str: UX type.
    """
    
    if device in ["Android - Smartphone", "iPhone", "Mobile - Other",
                 "Android - Tablet", "iPad"]:
        return "Smartphone/Tablet"
    elif device == "Desktop":
        return "Desktop"
    return "Unknown"

def get_os(device:str)->str:
    """
    Get the OS from the device.

    Args:
        device (str): Device used for purchasing.

    Returns:
        str: OS type.
    """
    
    if device.startswith("Android"):
        return "Android"
    elif device in ["iPhone", "iPad"]:
        return "iOS"
    elif device == "Desktop":
        return "Desktop"
    return "Unknown"

def average_rate(rates:list)->float:
    """
    Returns the average rate from a list of rates.

    Args:
        rates (list): List of rates.

    Returns:
        float: Average rate of evolution.
    """

    n = len(rates)

    return (reduce(lambda x,y: (1+x)*(1+y), rates)**(1/n))-1
    
def plot_contributions(df: pd.DataFrame,
                       col_evolution: str,
                       cols_contributions: List[str]) -> None:
    """
    Plots a lineplot for a given evolution and stacked bar plots for 
    different contributions, correctly handling positive and negative values.

    Args:
        df (pd.DataFrame): DataFrame containing the whole data.
        col_evolution (str): Name of the evolution column.
        cols_contributions (list[str]): List of names of contributions.

    Returns:
        None.
    """

    plt.clf()
    plt.close("all")
    fig, ax = plt.subplots(figsize=(18, 6))

    cmap=plt.get_cmap("Set2")
    color_dict={
        col:cmap(i%10) for i,col in enumerate(cols_contributions)
    }

    # Initialize positive and negative bottoms
    bottom_pos = pd.Series(0, index=df.index)
    bottom_neg = pd.Series(0, index=df.index)

    for col in cols_contributions:
        values = df[col]

        # Where values are positive
        pos = values.where(values >= 0, 0)
        ax.bar(df.index,
               pos,
               bottom=bottom_pos,
               label=" ".join(col.split("_")[2:]) if (pos != 0).any() else None,
               color=color_dict[col])
        bottom_pos += pos

        # Where values are negative
        neg = values.where(values < 0, 0)
        ax.bar(df.index,
               neg,
               bottom=bottom_neg,
               label=" ".join(col.split("_")[2:]) if (neg < 0).all() else None,
               color=color_dict[col])
        bottom_neg += neg

    # Plot the evolution line
    ax.plot(df.index,
            df[col_evolution],
            label="Revenue evolution",
            color="black",
            linewidth=2)

    # Formatting
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)
    ax.set_title("Revenue monthly evolution")
    ax.set_xlabel("Date")
    ax.set_ylabel("Contributions to the revenue evolution")
    ax.legend(loc="center left", bbox_to_anchor=(1, .5))
    plt.tight_layout()
    plt.show()

def simplify_browser(browser:str)->str:
    """
    Simplifies the browser name by creating groups of Browsers.

    Args:
        browser (str): Name of the browser.

    Returns:
        str: New name for the browser.
    """
    if browser == "" or browser in ['unknown']:
        return 'Unknown'
    elif browser in ['chrome', 'chrome mobile', 'chrome mobile ios', 'chromium', 'comodo dragon', 'iron', 'mail.ru chromium browser']:
        return 'Chrome'
    elif browser in ['safari', 'mobile safari', 'mobile safari uiwebview', 'applemail']:
        return 'Safari'
    elif browser in ['firefox', 'firefox mobile', 'firefox ios', 'firefox beta', 'iceweasel', 
                     'pale moon (firefox variant)', 'firefox (minefield)', 'seamonkey']:
        return 'Firefox'
    elif browser in ['edge', 'edge mobile', 'ie', 'ie mobile']:
        return 'Edge/IE'
    elif browser in ['opera', 'opera mobile', 'opera mini', 'opera tablet']:
        return 'Opera'
    elif browser in ['adsbot-google', 'applebot', 'bingpreview', 'phantomjs']:
        return 'Bot/Crawler'
    elif browser in ['facebook', 'pinterest']:
        return 'Social In-App'
    elif browser in ['android', 'blackberry', 'blackberry webkit', 'ovi browser', 'amazon silk']:
        return 'Other Mobile'
    elif browser in ['yandex browser', 'vivaldi', 'maxthon', 'lunascape', 'sleipnir',
                     'netfront nx', 'avant', 'konqueror', 'midori', 'dolfin']:
        return 'Alternative'
    else:
        return 'Alternative' 
