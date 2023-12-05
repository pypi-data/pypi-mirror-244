"""
GMI
Adapted From: https://github.com/zpeng27/GMI
"""
from typing import List

import scipy.sparse as sp
import torch
from torch import nn

from ...utils import sparse_mx_to_torch_sparse_tensor
from .disc_gmi import DiscGMI
from .gcn import GCN


def avg_neighbor(features: torch.Tensor,
                 adj_orig: sp.csr_matrix) -> torch.Tensor:
    """Aggregate Neighborhood Using Original Adjacency Matrix

    Args:
        features (torch.Tensor): 2D row-normalized features.
        adj_orig (<class 'scipy.sparse.csr.csr_matrix'>): row-avaraged adj.

    Returns:
        (torch.Tensor): row-avaraged aggregation of neighborhood.
    """
    adj_orig = sparse_mx_to_torch_sparse_tensor(adj_orig)
    if torch.cuda.is_available():
        adj_orig = adj_orig.cuda()
    return torch.unsqueeze(torch.spmm(adj_orig, torch.squeeze(features, 0)), 0)


class GMI(nn.Module):
    """GMI

    Args:
        in_features (int): input feature dimension.
        hidden_units (int): output hidden units dimension.
        activation (str): activation of gcn layer. Defaults to prelu.
    """

    def __init__(
        self,
        in_features: int,
        hidden_units: int,
        gcn_depth: int = 2,
        activation: str = "prelu",
    ) -> None:
        super().__init__()
        self.gcn_depth = gcn_depth
        if gcn_depth == 2:
            self.gcn_1 = GCN(in_features, hidden_units, activation)
            self.gcn_2 = GCN(hidden_units, hidden_units, activation)
        elif gcn_depth == 1:
            self.gcn_1 = GCN(in_features, hidden_units, activation)
        else:
            raise ValueError(
                "Now gcn_depth only supports 1 or 2 layers, otherwise modify the code on you own."
            )
        self.disc_1 = DiscGMI(in_features, hidden_units, activation="sigmoid")
        self.disc_2 = DiscGMI(hidden_units, hidden_units, activation="sigmoid")
        self.prelu = nn.PReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(
        self,
        features_norm: torch.Tensor,
        adj_orig: sp.csr_matrix,
        adj_norm: torch.Tensor,
        neg_sample_list: List,
    ):
        """Forward Propagation

        Args:
            features_norm (torch.Tensor): row-normalized features.
            adj_orig (sp.csr_matrix): row-avaraged adj.
            adj_norm (torch.Tensor): symmetrically normalized sparse tensor adj.
            neg_sample_list (List): list of multiple repeatable shuffle of nodes index list.

        Returns:
            mi_pos, mi_neg, local_mi_pos, local_mi_neg, adj_rebuilt (torch.Tensor):
                D_w(h_i, x_i), D_w(h_i, x'_i), D_w(h_i, x_j), D_w(h_i, x'_j), w_{ij}
        """
        if self.gcn_depth == 1:
            h_2, h_w = self.gcn_1(features_norm, adj_norm)
        else:
            h_1, h_w = self.gcn_1(features_norm, adj_norm)
            h_2, _ = self.gcn_2(h_1, adj_norm)
        h_neighbor = self.prelu(avg_neighbor(h_w, adj_orig))

        mi_pos, mi_neg = self.disc_1(features_norm, h_2, neg_sample_list)
        local_mi_pos, local_mi_neg = self.disc_2(h_neighbor, h_2,
                                                 neg_sample_list)

        adj_rebuilt = self.sigmoid(
            torch.mm(torch.squeeze(h_2), torch.t(torch.squeeze(h_2))))
        return mi_pos, mi_neg, local_mi_pos, local_mi_neg, adj_rebuilt

    def get_embedding(self, features_norm, adj_norm):
        """Get Node Embedding

        Args:
            features_norm (torch.Tensor): row-normalized features.
            adj_norm (torch.Tensor): symmetrically normalized adj.

        Returns:
            (torch.Tensor): node embedding.
        """
        if self.gcn_depth == 1:
            h_2, _ = self.gcn_1(features_norm, adj_norm)
        else:
            h_1, _ = self.gcn_1(features_norm, adj_norm)
            h_2, _ = self.gcn_2(h_1, adj_norm)

        return h_2.detach()
