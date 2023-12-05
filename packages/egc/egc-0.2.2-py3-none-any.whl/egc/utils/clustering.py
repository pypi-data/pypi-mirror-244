"""Clustering Methods.
"""
from typing import Tuple

import numpy as np
import torch
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering

from .metrics import get_soft_assignment_matrix


def sk_clustering(
    X: torch.Tensor,
    n_clusters: int,
    name: str = "kmeans",
) -> np.ndarray:
    """sklearn clustering.

    Args:
        X (torch.Tensor): data embeddings.
        n_clusters (int): num of clusters.
        name (str, optional): type name. Defaults to 'kmeans'.

    Raises:
        NotImplementedError: clustering method not implemented.

    Returns:
        np.ndarray: cluster assignments.
    """
    if name == "kmeans":
        model = KMeans(n_clusters=n_clusters)
        label_pred = model.fit(X).labels_
        return label_pred

    if name == "spectral":
        model = SpectralClustering(n_clusters=n_clusters,
                                   affinity="precomputed")
        label_pred = model.fit(X).labels_
        return label_pred

    raise NotImplementedError


######################################################################################
# START: This section of code is adapted from https://github.com/bwilder0/clusternet #
######################################################################################


def soft_kmeans_clustering(
    data: torch.Tensor,
    miu: torch.Tensor,
    num_iter: int = 1,
    cluster_temp: float = 5,
    dist_type: str = "cosine_similarity",
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """pytorch (differentiable) implementation of soft k-means clustering.

    Args:
        data (torch.Tensor): data embeddings.
        miu (torch.Tensor, optional): cluster centers.
        num_iter (int, optional): num of iterations. Defaults to 1.
        cluster_temp (float, optional): softmax temperature. Defaults to 5.
        dist_type (str, optional): distance type. Defaults to 'cosine_similarity'.

    Returns:
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:\
            [cluster_centers, soft_assignment_matrix, distance]
    """
    n_clusters = miu.shape[0]
    data = torch.diag(1.0 / torch.norm(data, p=2, dim=1)) @ data

    for _ in range(num_iter):
        r = get_soft_assignment_matrix(
            data=data,
            miu=miu,
            cluster_temp=cluster_temp,
            dist_type=dist_type,
        )
        cluster_r = r.sum(dim=0)
        cluster_mean = (r.t().unsqueeze(1) @ data.expand(
            n_clusters,
            *data.shape,
        )).squeeze(1)
        new_miu = torch.diag(1 / cluster_r) @ cluster_mean
        miu = new_miu

    dist = data @ miu.t()
    r = torch.softmax(cluster_temp * dist, 1)
    return miu, r, dist


######################################################################################
# END:   This section of code is adapted from https://github.com/bwilder0/clusternet #
######################################################################################
