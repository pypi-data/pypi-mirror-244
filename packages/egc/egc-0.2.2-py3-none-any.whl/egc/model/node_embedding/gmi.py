"""Embedding By GMI

Adapted From: https://github.com/zpeng27/GMI
"""
from typing import Tuple

import numpy as np
import scipy.sparse as sp
import torch
from torch import nn

from ...module import GMI
from ...utils import get_repeat_shuffle_nodes_list
from ...utils import normalize_feature
from ...utils import sparse_mx_to_torch_sparse_tensor
from ...utils import symmetrically_normalize_adj


def mi_loss_jsd(pos: torch.Tensor, neg: torch.Tensor) -> torch.Tensor:
    """Jensen-Shannon MI Estimator

    Args:
        pos (torch.Tensor): :math:`D_w(h_i, x_i) or D_w(h_i, x_j)`.
        neg (torch.Tensor): :math:`D_w(h_i, x'_i) or D_w(h_i, x'_j)`.

    Returns:
        (torch.Tensor): JSD loss.

        .. math::

            & sp(-D_w(h_i,x_i))+E(sp(D_w(h_i,x'_i)))\\\\
            & \\textbf{or} \\\\
            & sp(-D_w(h_i,x_j))+E(sp(D_w(h_i,x'_j))). \\\\
    """
    e_pos = torch.mean(torch.log(1 + torch.exp(-pos)))
    e_neg = torch.mean(torch.mean(torch.log(1 + torch.exp(neg)), 0))
    return e_pos + e_neg


def reconstruct_loss(pred: torch.Tensor, gnd: torch.Tensor) -> torch.Tensor:
    """Loss of Rebuilt Adj

    Args:
        pred (torch.Tensor): :math:`w_{ij}`.
        gnd (torch.Tensor): :math:`a_{ij}`.

    Returns:
        (torch.Tensor): reconstruction loss.

        .. math::
            \\text{reconstruct}_{loss} =
            & \\frac{n^2}{n^2 - |E|} * AVG(\\frac{-(n^2-|E|)}{|E|} *
            a_{ij} * \\log(w_{ij} + e^{-10}) \\\\
            & - (1 - a_{ij}) * \\log(1 - w_{ij} + e^{-10})).
    """
    nodes_n = gnd.shape[0]
    edges_n = np.sum(gnd) / 2
    weight1 = (nodes_n * nodes_n - edges_n) * 1.0 / edges_n
    weight2 = nodes_n * nodes_n * 1.0 / (nodes_n * nodes_n - edges_n)
    gnd = torch.FloatTensor(gnd).cuda()
    temp1 = gnd * torch.log(pred + (1e-10)) * (-weight1)
    temp2 = (1 - gnd) * torch.log(1 - pred + (1e-10))
    return torch.mean(temp1 - temp2) * weight2


def preprocess_adj(
        adj_orig: sp.csr_matrix) -> Tuple[torch.Tensor, torch.Tensor]:
    """Preprocess of Adjacency Matrix for Row Avarage and Self Loop

    Args:
        adj_orig (<class 'scipy.sparse.csr.csr_matrix'>): input origin adjacency matrix.

    Returns:
        adj_orig, adj_target (<class 'scipy.sparse.csr.csr_matrix'>, <class 'numpy.matrix'>):
        row avarage and self loop adj
    """
    adj_dense = adj_orig.toarray()
    adj_row_avg = 1.0 / np.sum(adj_dense, axis=1)
    adj_row_avg[np.isnan(adj_row_avg)] = 0.0
    adj_row_avg[np.isinf(adj_row_avg)] = 0.0
    adj_dense = adj_dense * 1.0
    for i in range(adj_orig.shape[0]):
        adj_dense[i] = adj_dense[i] * adj_row_avg[i]
    adj_orig = sp.csr_matrix(adj_dense, dtype=np.float32)
    adj_target = adj_dense + np.eye(adj_dense.shape[0])
    return adj_orig, adj_target


class GMIEmbed(nn.Module):
    """GMI Embedding

    Args:
        in_features (int): input feature dimension.
        hidden_units (int, optional): hidden units size of gcn. Defaults to 512.
        n_epochs (int, optional): number of embedding training epochs. Defaults to 550.
        early_stopping_epoch (int, optional): early stopping threshold. Defaults to 20.
        lr (float, optional): learning rate. Defaults to 0.001.
        l2_coef (float, optional): weight decay. Defaults to 0.0.
        alpha (float, optional): parameter for :math:`I(h_i; x_i)`. Defaults to 0.8.
        beta (float, optional): parameter for :math:`I(h_i; x_j)`. Defaults to 1.0.
        gamma (float, optional): parameter for :math:`I(w_ij; a_ij)`. Defaults to 1.0.
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
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.features_norm = None
        self.adj_orig = None
        self.adj_norm = None
        self.adj_target = None

        self.model = GMI(in_features,
                         hidden_units,
                         gcn_depth=gcn_depth,
                         activation=activation)
        self.optimizer = torch.optim.Adam(self.model.parameters(),
                                          lr=lr,
                                          weight_decay=l2_coef)

    def calc_loss(
        self,
        mi_pos: torch.Tensor,
        mi_neg: torch.Tensor,
        local_mi_pos: torch.Tensor,
        local_mi_neg: torch.Tensor,
        adj_rebuilt: torch.Tensor,
    ) -> torch.Tensor:
        """Calculate Loss

        Args:
            mi_pos (torch.Tensor): :math:`D_w(h_i, x_i)`.
            mi_neg (torch.Tensor): :math:`D_w(h_i, x'_i)`.
            local_mi_pos (torch.Tensor): :math:`D_w(h_i, x_j)`.
            local_mi_neg (torch.Tensor): :math:`D_w(h_i, x'_j)`.
            adj_rebuilt (torch.Tensor): :math:`w_{ij}`

        Returns:
            (torch.Tensor): loss.

            .. math::

                loss = & \\alpha * sp(-D_w(h_i,x_i))+E(sp(D_w(h_i,x'_i))) \\\\
                & + \\beta * sp(-D_w(h_i,x_j))+E(sp(D_w(h_i,x'_j))) \\\\
                & + \\gamma * \\text{reconstruct}_{loss} \\\\
        """
        return (self.alpha * mi_loss_jsd(mi_pos, mi_neg) +
                self.beta * mi_loss_jsd(local_mi_pos, local_mi_neg) +
                self.gamma * reconstruct_loss(adj_rebuilt, self.adj_target))

    def forward(self, neg_sample_list: torch.Tensor) -> torch.Tensor:
        """Forward Propagation

        Args:
            neg_sample_list (torch.Tensor): negative sample list.

        Returns:
            torch.Tensor: loss.
        """
        mi_pos, mi_neg, local_mi_pos, local_mi_neg, adj_rebuilt = self.model(
            self.features_norm, self.adj_orig, self.adj_norm, neg_sample_list)
        return self.calc_loss(mi_pos, mi_neg, local_mi_pos, local_mi_neg,
                              adj_rebuilt)

    def fit(
        self,
        features: sp.lil_matrix,
        adj_orig: sp.csr_matrix,
        neg_list_num: int = 5,
    ) -> None:
        """Fit for Specific Graph

        Args:
            features (sp.lil_matrix): 2D sparse features.
            adj_orig (sp.csr_matrix): 2D sparse adj.
            neg_list_num (int, optional): negative sample times. Defaults to 5.
        """
        self.features_norm = torch.FloatTensor(
            normalize_feature(features)[np.newaxis])

        self.adj_norm = sparse_mx_to_torch_sparse_tensor(
            symmetrically_normalize_adj(adj_orig + sp.eye(adj_orig.shape[0])))
        self.adj_orig, self.adj_target = preprocess_adj(adj_orig)

        if torch.cuda.is_available():
            print("GPU available: GMI Embedding Using CUDA")
            self.model.cuda()
            self.features_norm = self.features_norm.cuda()
            self.adj_norm = self.adj_norm.cuda()

        best = 1e9
        cnt_wait = 0
        for epoch in range(self.n_epochs):
            self.model.train()
            self.optimizer.zero_grad()
            neg_sample_list = get_repeat_shuffle_nodes_list(
                adj_orig.shape[0], neg_list_num)
            loss = self.forward(neg_sample_list)

            print(f"Epoch:{epoch+1}  Loss:{loss}")
            if loss < best:
                best = loss
                cnt_wait = 0
                torch.save(self.model.state_dict(), "best_gmi.pkl")
            else:
                cnt_wait += 1

            if cnt_wait == self.early_stopping_epoch:
                print("Early stopping!")
                break

            loss.backward()
            self.optimizer.step()

    def set_features_norm(self, features_norm) -> None:
        """Set the features row normalized

        Args:
            features_norm (torch.Tensor): normalized 3D features tensor in shape of [1, xx, xx]
        """
        self.features_norm = features_norm

    def set_adj_norm(self, adj_norm) -> None:
        """Set the adjacency symmetrically normalized

        Args:
            adj_norm (torch.Tensor): symmetrically normalized 2D adjacency tensor
        """
        self.adj_norm = adj_norm

    def get_features_norm(self) -> torch.Tensor:
        """Get the features row normalized

        Returns:
            features_norm (torch.Tensor): normalized 3D features tensor in shape of [1, xx, xx]
        """
        return self.features_norm

    def get_adj_norm(self) -> torch.Tensor:
        """Get the adjacency symmetrically normalized

        Returns:
            adj_norm (torch.Tensor): symmetrically normalized 2D adjacency tensor
        """
        return self.adj_norm

    def get_embedding(self) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        self.model.load_state_dict(torch.load("best_gmi.pkl"))
        return self.model.get_embedding(self.features_norm, self.adj_norm)
