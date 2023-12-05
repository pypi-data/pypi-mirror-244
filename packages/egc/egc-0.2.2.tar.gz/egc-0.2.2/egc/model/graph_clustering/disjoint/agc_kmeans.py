"""AGC Kmeans"""
import torch
from sklearn.cluster import KMeans

from ...node_embedding import AGCEmbed
from ..base import Base


class AGC(Base):
    """SENet Kmeans

    Args:
        feature (FloatTensor): node's feature.
        labels (IntTensor): node's label.
        adj (FloatTensor): graph's adjacency matrix
        n_clusters (int): clusters
        epochs (int,optional):  number of embedding training epochs.Defaults to  60,
        rep (int,optional): times of calculate intra(c)
    """

    def __init__(
        self,
        adj: torch.sparse.Tensor,
        feature: torch.Tensor,
        labels: torch.Tensor,
        epochs: int = 60,
        n_clusters: int = 7,
        rep: int = 10,
    ):
        super().__init__()
        feature[feature - 0.0 > 0.001] = 1
        self.n_clusters = n_clusters
        self.model = AGCEmbed(adj, feature, labels, epochs, n_clusters, rep)

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
        u = self.get_embedding()
        kmeans = KMeans(n_clusters=self.n_clusters).fit(u)
        predict_labels = kmeans.predict(u)
        return predict_labels
