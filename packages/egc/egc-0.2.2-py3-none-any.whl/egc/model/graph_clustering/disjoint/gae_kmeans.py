"""gae_kmeans
"""
# import torch
import scipy.sparse as sp
import torch

from ....utils import sk_clustering
from ...node_embedding import DGL_GAE
from ..base import Base


class DGL_GAEKmeans(Base):
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
        epochs: int,
        n_clusters: int,
        fead_dim: int,
        n_nodes: int,
        hidden_dim1: int = 32,
        dropout: float = 0.0,
        lr: float = 0.01,
        early_stop: int = 10,
        activation: str = "relu",
    ) -> None:
        super().__init__()
        self.n_clusters = n_clusters
        # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = DGL_GAE(
            epochs,
            n_clusters,
            fead_dim,
            n_nodes,
            hidden_dim1,
            dropout,
            lr,
            early_stop,
            activation,
        )

    def fit(
            self,
            adj_csr: sp.csr_matrix,
            features: torch.Tensor,
            device: torch.device = torch.device("cpu"),
    ):
        """Fit for Specific Graph

        Args:
            adj_csr (sp.lil_matrix): 2D sparse features.
            features (torch.Tensor): node's features
        """
        self.model.fit(adj_csr, features, device=device)

    def get_embedding(self):
        return self.model.get_embedding()

    def get_memberships(self):
        return sk_clustering(
            self.get_embedding().cpu(),
            self.n_clusters,
            name="kmeans",
        )
