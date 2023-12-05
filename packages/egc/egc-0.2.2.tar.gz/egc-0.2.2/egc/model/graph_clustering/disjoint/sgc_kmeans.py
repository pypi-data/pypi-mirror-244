"""sgc_kmeans
"""
from typing import Callable
from typing import List

import dgl
import torch

from ....utils import sk_clustering
from ...node_embedding import SGC
from ..base import Base


class SGCKmeans(Base):
    """GAE Kmeans implement using dgl

    Args:
        epochs (int, optional): number of embedding training epochs. Defaults to 200.
        n_clusters (int): cluster num.
        fead_dim (int): dim of features
        n_nodes (int): number of nodes
        hidden_dim1 (int): hidden units size of gcn_1. Defaults to 32.
        dropout (int, optional): Dropout rate (1 - keep probability).
        lr (float, optional): learning rate.. Defaults to 0.001.
        early_stop (int, optional): early stopping threshold. Defaults to 10.
        activation (str, optional): activation of gcn layer_1. Defaults to 'relu'.
    """

    def __init__(
        self,
        in_feats: int,
        n_epochs: int = 400,
        hidden_units: List = [500],
        lr: float = 0.01,
        early_stop: int = 10,
        inner_act: Callable = lambda x: x,
        n_lin_layers: int = 1,
        n_gnn_layers: int = 10,
    ) -> None:
        super().__init__()
        self.model = SGC(
            in_feats=in_feats,
            hidden_units=hidden_units,
            n_lin_layers=n_lin_layers,
            n_gnn_layers=n_gnn_layers,
            lr=lr,
            n_epochs=n_epochs,
            inner_act=inner_act,
            early_stop=early_stop,
        )

    def fit(
            self,
            graph: dgl.DGLGraph,
            n_clusters: int,
            device: torch.device = torch.device("cpu"),
    ):
        """Fit for Specific Graph

        Args:
            graph (dgl.DGLGraph): dgl graph.
            n_clusters (int): cluster num.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.n_clusters = n_clusters
        self.model.fit(
            graph=graph,
            device=device,
        )

    def get_embedding(self):
        return self.model.get_embedding()

    def get_memberships(self):
        return sk_clustering(
            self.get_embedding().cpu(),
            self.n_clusters,
            name="kmeans",
        )
