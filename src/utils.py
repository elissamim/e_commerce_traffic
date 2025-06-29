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

import pandas as pd
from typing import List

def price_volume_effects(df: pd.DataFrame, list_products: List[str]) -> pd.DataFrame:
    """
    Computes a price-volume decomposition of revenue for each product and aggregates
    them into overall effects on web traffic revenue.

    Args:
        df (pd.DataFrame): DataFrame with daily prices and quantities for each product.
        list_products (List[str]): List of product names (suffixes in column names).

    Returns:
        pd.DataFrame: DataFrame with total volume effect, price effect, entry revenue,
                      and exit cost across all products, indexed like the input.
    """
    tmp = df.copy(deep=True)

    for product in list_products:
        q = tmp[f"quantity_{product}"]
        p = tmp[f"price_{product}"]

        # Define entry/exit flags
        flag_entry = (q.shift(1) == 0) & (q > 0)
        flag_exit = (q == 0) & (q.shift(1) > 0)

        tmp[f"flag_entree_{product}"] = flag_entry
        tmp[f"flag_sortie_{product}"] = flag_exit

        # Price and volume effects (masked where entry/exit occurs)
        volume_effect = p.shift(1) * (q - q.shift(1))
        price_effect = q * (p - p.shift(1))
        mask = ~(flag_entry | flag_exit)

        tmp[f"volume_effect_{product}"] = volume_effect.where(mask, 0)
        tmp[f"price_effect_{product}"] = price_effect.where(mask, 0)

        # Revenue from entries
        tmp[f"revenue_entree_{product}"] = (p * q).where(flag_entry, 0)

        # Cost from exits
        tmp[f"cout_sortie_{product}"] = (-p.shift(1) * q.shift(1)).where(flag_exit, 0)

    # Aggregate across all products
    tmp["web_traffic_volume_effect"] = tmp.filter(like="volume_effect_").sum(axis=1)
    tmp["web_traffic_price_effect"] = tmp.filter(like="price_effect_").sum(axis=1)
    tmp["web_traffic_entry_revenue"] = tmp.filter(like="revenue_entree_").sum(axis=1)
    tmp["web_traffic_exit_cost"] = tmp.filter(like="cout_sortie_").sum(axis=1)

    return tmp[[
        "web_traffic_volume_effect",
        "web_traffic_price_effect",
        "web_traffic_entry_revenue",
        "web_traffic_exit_cost"
    ]].iloc[1:]  # drop first row (NaNs due to .shift)
