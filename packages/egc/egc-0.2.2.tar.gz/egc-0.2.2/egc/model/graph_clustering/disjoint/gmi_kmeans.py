"""GMI Kmeans Graph Clustering
"""
import scipy.sparse as sp
import torch

from ....utils import sk_clustering
from ...node_embedding import GMIEmbed
from ..base import Base


class GMIKmeans(Base):
    """GMI Kmeans

    Args:
        in_features (int): input feature dimension.
        hidden_units (int, optional): hidden units size of gcn. Defaults to 512.
        n_epochs (int, optional): number of embedding training epochs. Defaults to 550.
        early_stopping_epoch (int, optional): early stopping threshold. Defaults to 20.
        lr (float, optional): learning rate. Defaults to 0.001.
        l2_coef (float, optional): weight decay. Defaults to 0.0.
        alpha (float, optional): parameter for I(h_i; x_i). Defaults to 0.8.
        beta (float, optional): parameter for I(h_i; x_j). Defaults to 1.0.
        gamma (float, optional): parameter for I(w_ij; a_ij). Defaults to 1.0.
        activation (str, optional): activation of gcn layer. Defaults to "prelu".
    """

    def __init__(
        self,
        in_features: int,
        hidden_units: int = 512,
        n_epochs: int = 550,
        early_stopping_epoch: int = 20,
        lr: float = 0.001,
        l2_coef: float = 0.0,
        alpha: float = 0.8,
        beta: float = 1.0,
        gamma: float = 1.0,
        activation: str = "prelu",
        gcn_depth: int = 2,
    ) -> None:
        super().__init__()
        self.n_clusters = None
        self.model = GMIEmbed(
            in_features,
            hidden_units,
            n_epochs,
            early_stopping_epoch,
            lr,
            l2_coef,
            alpha,
            beta,
            gamma,
            activation,
            gcn_depth=gcn_depth,
        )

    def fit(
        self,
        features_lil: sp.lil_matrix,
        adj_csr: sp.csr_matrix,
        n_clusters: int,
        neg_list_num: int = 5,
    ):
        """Fit for Specific Graph

        Args:
            features (sp.lil_matrix): 2D sparse features.
            adj_orig (sp.csr_matrix): 2D sparse adj.
            n_clusters (int): cluster num.
            neg_list_num (int, optional): negative sample times. Defaults to 5.
        """
        self.n_clusters = n_clusters
        self.model.fit(features_lil, adj_csr, neg_list_num)

    def get_embedding(self):
        return self.model.get_embedding()

    def get_memberships(self):
        return sk_clustering(torch.squeeze(self.get_embedding(), 0).cpu(),
                             self.n_clusters,
                             name="kmeans")
