"""Used for age model
"""
import numpy as np
from sklearn.cluster import SpectralClustering

from ...node_embedding import AGE
from ..base import Base


class age_cluster(Base):
    """AGE Cluster Implement

    Args:
        dims (list,optional): Number of units in hidden layer 1.
        feat_dim (int,optional): input feature dimension.
        gnnlayers_num (int): Number of gnn layers
        linlayers_num (int, optional): Number of hidden layers
        lr (float, optional): learning rate.. Defaults to 0.001.
        upth_st (float, optional): Upper Threshold start.
        upth_ed (float, optional): Upper Threshold end.
        lowth_st (float, optional): Lower Threshold start.
        lowth_ed (float, optional): Lower Threshold end.
        upd (float, optional): Update epoch.
        bs (int,optional):Batchsize
        epochs (int,optional):Number of epochs to train.
        norm (str,optional):normalize mode of Laplacian matrix
        renorm (bool,optional):If with the renormalization trick
        estop_steps (int,optional):Number of early_stop steps.
        n_cluster (int,optinal):number of clusters
    """

    def __init__(
        self,
        dims: list = None,
        feat_dim: int = None,
        gnnlayers_num: int = 3,
        linlayers_num: int = 1,
        lr: float = 0.001,
        upth_st: float = 0.0015,
        upth_ed: float = 0.001,
        lowth_st: float = 0.1,
        lowth_ed: float = 0.5,
        upd: float = 10,
        bs: int = 10000,
        epochs: int = 400,
        norm: str = "sym",
        renorm: bool = True,
        estop_steps: int = 5,
        n_clusters: int = None,
    ) -> None:
        super().__init__()
        self.n_clusters = n_clusters
        self.model = AGE(
            dims,
            feat_dim,
            gnnlayers_num,
            linlayers_num,
            lr,
            upth_st,
            upth_ed,
            lowth_st,
            lowth_ed,
            upd,
            bs,
            epochs,
            norm,
            renorm,
            estop_steps,
        )

    def fit(self, adj_csr, features):
        """Fit for Specific Graph

        Args:
            adj_csr (sp.lil_matrix): 2D sparse features.
            features (torch.Tensor): node's features
        """
        self.model.fit(adj_csr, features)

    def get_embedding(self):
        """Get cluster embedding

        Returns:numpy.ndarray
        """
        return self.model.get_embedding().cpu().numpy()

    def get_memberships(self):
        """Get spectral cluster membership.

        Returns:numpy.ndarray
        """
        # from sklearn.cluster import KMeans
        # u = self.get_embedding()
        # kmeans = KMeans(n_clusters=self.n_clusters).fit(u)
        # predict_labels = kmeans.predict(u)
        # return predict_labels
        Cluster = SpectralClustering(n_clusters=self.n_clusters,
                                     affinity="precomputed")
        f_adj = np.matmul(self.get_embedding(),
                          np.transpose(self.get_embedding()))
        predict_labels = Cluster.fit_predict(f_adj)
        return predict_labels
