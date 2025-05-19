from dataclasses import dataclass
import random
import pandas as pd

import networkx as nx


@dataclass
class BenchmarkGraph:
    """A graph used for benchmarking.
    
    Attributes
    ----------
    name : str
        The name of the graph.
    graph : nx.Graph
        The graph object.
    """
    name: str
    graph: nx.Graph

    @classmethod
    def from_func(cls, func, *args, **kwargs) -> "BenchmarkGraph":
        """
        Create a BenchmarkGraph from a graph-generating function and its arguments.

        Parameters:
            func (Callable): The graph-generating function.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            BenchmarkGraph: An instance with the generated name and graph.
        """
        name = graph_name_from_func(func, *args, **kwargs)
        graph = func(*args, **kwargs)
        return cls(name, graph)


def graph_name_from_func(func, *args, **kwargs) -> str:
    """Generate a string name for a graph-generating function and its arguments.

    This function takes a graph constructor (such as a NetworkX generator),
    along with its positional and keyword arguments, and returns a string
    of the form: 'function_name(arg1, arg2, ..., kwarg1=val1, ...)'.

    Parameters:
        func (Callable): The graph-generating function.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        str: A string representation of the function and its arguments,
             suitable for labeling graphs in benchmarks or plots.

    Example:
        >>> graph_name_from_func(nx.erdos_renyi_graph, 100, 0.1)
        'erdos_renyi_graph(100, 0.1)'

        >>> graph_name_from_func(nx.grid_2d_graph, 5, 5, periodic=True)
        'grid_2d_graph(5, 5, periodic=True)'
    """
    func_name = func.__name__
    args_str = ", ".join(map(str, args))
    kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    all_args = ", ".join(filter(None, [args_str, kwargs_str]))
    return f"{func_name}({all_args})"


def generate_weighted_graph(
    max_weight: float,
    graph_func,
    *args,
    **kwargs
) -> nx.Graph:
    """
    Generate a graph using the given function and assign random edge weights.

    Parameters:
        max_weight (float): Maximum random weight (min is 1).
        graph_func (Callable): The graph-generating function.
        *args: Positional arguments for the graph function.
        **kwargs: Keyword arguments for the graph function.

    Returns:
        nx.Graph: A graph with randomly weighted edges.
    """
    G = graph_func(*args, **kwargs)
    for u, v in G.edges():
        G[u][v]["weight"] = random.randint(0, max_weight)
    return G


def fetch_drug_interaction_network():
    # Drug-drug interaction network
    # https://snap.stanford.edu/biodata/datasets/10001/10001-ChCh-Miner.html
    data = pd.read_csv(
        "https://snap.stanford.edu/biodata/datasets/10001/files/ChCh-Miner_durgbank-chem-chem.tsv.gz",
        sep="\t",
        header=None,
    )
    return nx.from_pandas_edgelist(data, source=0, target=1)
