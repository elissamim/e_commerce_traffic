from functools import reduce
import matplotlib.pyplot as plt
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
    
    if device in ["Android - Smartphone", "iPhone", "Mobile - Other"]:
        return "Mobile"
    elif device in ["Android - Tablet", "iPad"]:
        return "Tablet"
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