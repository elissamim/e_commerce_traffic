from functools import reduce
import matplotlib.pyplot as plt
import pandas as pd

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
                       cols_contributions: list[str]) -> None:
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

    fig, ax = plt.subplots(figsize=(12, 6))

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
               label=col if (pos != 0).any() else None)
        bottom_pos += pos

        # Where values are negative
        neg = values.where(values < 0, 0)
        ax.bar(df.index,
               neg,
               bottom=bottom_neg,
               label=None)  # Hide legend for negative duplicate
        bottom_neg += neg

    # Plot the evolution line
    ax.plot(df.index,
            df[col_evolution],
            label=col_evolution,
            color="black",
            linewidth=2)

    # Formatting
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)
    ax.set_title("Revenue monthly evolution")
    ax.set_xlabel("Date")
    ax.set_ylabel("Contributions to the revenue evolution")
    ax.legend()
    plt.tight_layout()
    plt.show()
