"""
DANMF implement
Repository: https://github.com/benedekrozemberczki/DANMF
Author: benedekrozemberczki
"""
import networkx as nx
import pandas as pd
from texttable import Texttable


def read_graph(args):
    """
    Method to read graph and create a target matrix with matrix powers.
    :param args: Arguments object.
    """
    print("\nTarget matrix creation started.\n")
    graph = nx.from_edgelist(pd.read_csv(args.edge_path).values.tolist())
    return graph


def loss_printer(losses):
    """
    Printing the losses for each iteration.
    :param losses: List of losses in each iteration.
    """
    txt = Texttable()
    txt.add_rows([[
        "Iteration",
        "Reconstrcution Loss I.",
        "Reconstruction Loss II.",
        "Regularization Loss",
    ]])
    txt.add_rows(losses)
    print(txt.draw())
