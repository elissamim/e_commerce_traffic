from functools import reduce

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