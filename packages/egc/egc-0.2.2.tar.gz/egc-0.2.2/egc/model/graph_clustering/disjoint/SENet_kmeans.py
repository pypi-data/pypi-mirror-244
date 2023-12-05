"""SENet Kmeans"""
import torch
from sklearn.cluster import KMeans

from ...node_embedding import SENetEmbed
from ..base import Base


class SENetKmeans(Base):
    """SENet Kmeans

    Args:
        feature (FloatTensor): node's feature.
        labels (IntTensor): node's label.
        adj (FloatTensor): graph's adjacency matrix
        n_clusters (int): clusters
        hidden0 (int,optional): hidden units size of gnn layer1. Defaults to 16,
        hidden1 (int,optional): hidden units size of gnn layer2. Defaults to 16,,
        lr (float,optional): learning rate. Defaults to 3e-2,
        epochs (int,optional):  number of embedding training epochs.Defaults to  50,
        weight_decay (float,optional): weight decay.Defaults to 0.0,
        lam (float,optional):Used for construct improved graph . Defaults to 1.0,
        n_iter (int,optional):the times of convoluting feature . Defaults to 3,
    """

    def __init__(
        self,
        feature: torch.FloatTensor,
        labels: torch.IntTensor,
        adj: torch.FloatTensor,
        n_clusters: int,
        hidden0: int = 16,
        hidden1: int = 16,
        lr: float = 3e-2,
        epochs: int = 50,
        weight_decay: float = 0.0,
        lam: float = 1.0,
        n_iter: int = 3,
    ):
        super().__init__()
        self.n_clusters = n_clusters
        feature[(feature - 0.0) > 0.001] = 1.0
        self.model = SENetEmbed(
            feature,
            labels,
            adj.to_dense().numpy(),
            n_clusters,
            hidden0,
            hidden1,
            lr,
            epochs,
            weight_decay,
            lam,
            n_iter,
        )

    def fit(self):
        """Fit for Specific Graph"""
        self.model.fit()

    def get_embedding(self):
        """Get embedding from trained model

        Returns:
            (torch.floatTensor)
            node embedding
        """
        return self.model.get_embedding()

    def get_memberships(self):
        """Get predict label by kmeans

        Returns:
            (torch.intTensor)
            predict label
        """
        Z = self.get_embedding()
        kmeans = KMeans(n_clusters=self.n_clusters).fit(Z)
        return kmeans.predict(Z)
