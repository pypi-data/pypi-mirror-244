"""pca_kmeans
"""
import numpy as np

from ....utils import MF
from ....utils import sk_clustering


def pca_kmeans(
    X: np.ndarray,
    n_clusters: int,
    n_components: int or float or str = None,
) -> np.ndarray:
    """Principal component analysis (PCA).

    Args:
        X (np.ndarray): array-like of shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        n_clusters (int): num of clusters.
        n_components (int or float or str): Number of components to keep. Defaults to None.

    Returns:
        np.ndarray: Community memberships.
    """
    embedding = MF(X, n_components, name="PCA")
    label_pred = sk_clustering(embedding, n_clusters, name="kmeans")
    return label_pred
