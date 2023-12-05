"""
vgae_kmeans
"""
import scipy.sparse as sp
import torch

from ....utils import sk_clustering
from ...node_embedding.vgae import DGL_VGAE
from ...node_embedding.vgae import VGAE
from ..base import Base


class DGL_VGAEKmeans(Base):
    """VGAE Kmeans implement using dgl

    Args:
        epochs (int, optional): number of embedding training epochs. Defaults to 200.
        n_clusters (int): cluster num.
        fead_dim (int): dim of features
        n_nodes (int): number of nodes
        hidden_dim1 (int): hidden units size of gcn_1. Defaults to 32.
        hidden_dim2 (int): hidden units size of gcn_2. Defaults to 16.
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
        hidden_dim2: int = 16,
        dropout: float = 0.0,
        lr: float = 0.01,
        early_stop: int = 10,
        activation: str = "relu",
    ) -> None:
        super().__init__()
        self.n_clusters = n_clusters
        # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = DGL_VGAE(
            epochs,
            n_clusters,
            fead_dim,
            n_nodes,
            hidden_dim1,
            hidden_dim2,
            dropout,
            lr,
            early_stop,
            activation,
        )

    def fit(self, adj_csr, features):
        """Fit for Specific Graph

        Args:
            adj_csr (sp.lil_matrix): 2D sparse features.
            features (torch.Tensor): node's features
        """
        self.model.fit(adj_csr, features)

    def get_embedding(self):
        return self.model.get_embedding()

    def get_memberships(self):
        return sk_clustering(self.get_embedding().cpu(),
                             self.n_clusters,
                             name="kmeans")


class VGAEKmeans(Base):
    """VGAE Kmeans

    Args:
        in_features (int): input feature dimension.
        hidden_units_1 (int, optional): gcn_1 hidden units. Defaults to 32.
        hidden_units_2 (int, optional): gcn_2 hidden units. Defaults to 16.
        n_epochs (int, optional): node embedding epochs. Defaults to 400.
        early_stopping_epoch (int, optional): early stopping epoch number. Defaults to 20.
        lr (float, optional): learning rate. Defaults to 0.001.
        l2_coef (float, optional): l2 weight decay. Defaults to 0.0.
        activation (str, optional): activation of gcn layer. Defaults to 'relu'.
        model_filename: str = 'vgae_kmeans',
    """

    def __init__(
        self,
        in_features: int,
        hidden_units_1: int = 32,
        hidden_units_2: int = 16,
        n_epochs: int = 400,
        early_stopping_epoch: int = 20,
        lr: float = 0.001,
        l2_coef: float = 0.0,
        activation: str = "relu",
        model_filename: str = "vgae_kmeans",
    ) -> None:
        super().__init__()
        self.n_clusters = None
        self.model = VGAE(
            in_features,
            hidden_units_1,
            hidden_units_2,
            n_epochs,
            early_stopping_epoch,
            lr,
            l2_coef,
            activation,
            model_filename,
        )

    def fit(self, features_lil: sp.lil_matrix, adj_csr: sp.csr_matrix,
            n_clusters: int):
        """Fit for Specific Graph

        Args:
            features (sp.lil_matrix): 2D sparse features.
            adj_orig (sp.csr_matrix): 2D sparse adj.
            n_clusters (int): cluster num.
            neg_list_num (int, optional): negative sample times. Defaults to 5.
        """
        self.n_clusters = n_clusters
        self.model.fit(features_lil, adj_csr)

    def get_embedding(self):
        return self.model.get_embedding()

    def get_memberships(self):
        return sk_clustering(torch.squeeze(self.get_embedding(), 0).cpu(),
                             self.n_clusters,
                             name="kmeans")
