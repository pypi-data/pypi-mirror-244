"""Embdding Pretrain using Kmeans
"""
import numpy as np
import scipy.sparse as sp
import torch

from ....model.graph_clustering.disjoint.vgae_kmeans import VGAEKmeans
from ....utils.evaluation import evaluation


def kmeans_pretrain(
    features_lil: torch.Tensor,
    adj_csr: torch.Tensor,
    n_clusters: int,
    label: np.ndarray,
) -> sp.csr_matrix:
    """kmeans pretraining

    Args:
        features_lil (torch.Tensor): features.
        adj_csr (torch.Tensor): adj.
        n_clusters (int): num of clusters.
        label (np.ndarray): labels.

    Returns:
        sp.csr_matrix: one hot cluster embbeding for nodes.
    """
    _model = VGAEKmeans(
        in_features=features_lil.shape[1],
        hidden_units_1=128,
        hidden_units_2=64,
        lr=0.01,
        early_stopping_epoch=20,
        n_epochs=400,
    )
    _model.fit(features_lil, adj_csr, n_clusters)
    _label = _model.get_memberships()
    row = []
    col = []
    data = []
    for i in range(n_clusters):
        line = np.nonzero(_label == i)[0].tolist()
        col.extend(line)
        row.extend([i] * len(line))
        data.extend([1] * len(line))
    emb = (sp.csr_matrix((data, (row, col)),
                         shape=(n_clusters, max(col) + 1),
                         dtype=np.int32).todense().T)
    (
        ARI_score,
        NMI_score,
        ACC_score,
        Micro_F1_score,
        Macro_F1_score,
    ) = evaluation(label, _label)
    print("\n"
          f"ARI:{ARI_score}\n"
          f"NMI:{ NMI_score}\n"
          f"ACC:{ACC_score}\n"
          f"Micro F1:{Micro_F1_score}\n"
          f"Macro F1:{Macro_F1_score}\n")

    return emb
