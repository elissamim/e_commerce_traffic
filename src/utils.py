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

def plot_contributions(df:pd.DataFrame,
                      col_evolution:str,
                      cols_contributions:list[str]) -> None:
    """
    Plots a lineplot for a given evolution and stacked bar plots for 
    different contributions.

    Args:
        df (pd.DataFrame): DataFrame containing the whole data.
        col_evolution (str): Name of the evolution column.
        cols_contributions (list[str]): List of names of contributions.

    Returns:
        None.
    """

    fig, ax = plt.subplots(figsize=(12, 6))

    # Contributions
    list_past_contributions = []

    ax.bar(df.index,
          df[cols_contributions[0]],
          label=cols_contributions[0])
    list_past_contributions.append(cols_contributions[0])

    ax.bar(df.index,
          df[cols_contributions[1]],
          bottom=list_past_contributions,
          label=cols_contributions[1])
    list_past_contributions.append(cols_contributions[1])

    if len(cols_contributions) > 2:
    
        for col in cols_contributions[2:]:
            
            ax.bar(df.index, 
                   df[col],
                   bottom=reduce(lambda x,y: df[x]+df[y],
                                list_past_contributions),
                   label=col)
            list_past_contributions.append(col)
    
    # Evolution
    ax.plot(df.index, 
            df[col_evolution], 
            label="Revenue monthly evolution", 
            color="black", 
            linewidth=2)
    
    # Add legend and labels
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)
    ax.set_title("Revenue monthly evolution")
    ax.set_xlabel("Date")
    ax.set_ylabel("Contributions to the revenue evolution")
    ax.legend()
    
    plt.tight_layout()
    plt.show()