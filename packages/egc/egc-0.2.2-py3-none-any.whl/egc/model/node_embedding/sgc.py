"""SGC"""
import copy
from typing import Callable
from typing import List
from typing import Tuple

import dgl
import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from torch import nn

from ...module import InnerProductDecoder
from ...utils import init_weights


def eliminate_zeros(adj: sp.spmatrix) -> sp.spmatrix:
    """Remove self-loops and edges with value of zero.

    Args:
        adj (sp.spmatrix): adjacent matrix.

    Returns:
        sp.spmatrix: adjacent matrix.
    """
    adj = adj - sp.dia_matrix(
        (adj.diagonal()[np.newaxis, :], [0]),
        shape=adj.shape,
    )
    adj.eliminate_zeros()
    return adj


def scale(z):
    """Feature Scale
    Args:
        z (torch.Tensor):hidden embedding

    Returns:
        z_scaled (torch.Tensor):scaled embedding
    """
    zmax = z.max(dim=1, keepdim=True)[0]
    zmin = z.min(dim=1, keepdim=True)[0]
    z_std = (z - zmin) / (zmax - zmin)
    z_scaled = z_std
    return z_scaled


class LinTrans(nn.Module):
    """Linear Transform Model

    Args:
        layers (int):number of linear layers.
        dims (list):Number of units in hidden layers.
    """

    def __init__(self, layers, dims):
        super().__init__()
        self.layers = nn.ModuleList()
        for i in range(layers):
            self.layers.append(nn.Linear(dims[i], dims[i + 1]))

    def forward(self, x):
        """Forward Propagation

        Args:
            x (torch.Tensor):feature embedding

        Returns:
            out (torch.Tensor):hiddin embedding
        """
        out = x
        for layer in self.layers:
            out = layer(out)
        out = scale(out)
        out = F.normalize(out)
        return out


class SGC(nn.Module):

    def __init__(
        self,
        in_feats: int,
        hidden_units: List,
        n_lin_layers: int = 1,
        n_gnn_layers: int = 10,
        lr: float = 0.001,
        n_epochs: int = 400,
        inner_act: Callable = lambda x: x,
        early_stop: int = 10,
    ) -> None:
        super().__init__()
        self.n_gnn_layers = n_gnn_layers
        self.n_lin_layers = n_lin_layers
        self.hidden_units = hidden_units
        self.lr = lr
        self.n_epochs = n_epochs
        self.estop_steps = early_stop
        self.device = None
        self.sm_fea_s = None
        self.lbls = None
        self.best_model = None

        self.encoder = LinTrans(self.n_lin_layers, [in_feats] + hidden_units)
        self.inner_product_decoder = InnerProductDecoder(act=inner_act)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)

        for module in self.modules():
            init_weights(module)

    @staticmethod
    def bce_loss(preds, labels, norm=1.0, pos_weight=None):
        return norm * F.binary_cross_entropy_with_logits(
            preds,
            labels,
            pos_weight=pos_weight,
        )

    def preprocess_graph(
        self,
        adj: sp.csr_matrix,
        layer: int,
        norm: str = "sym",
        renorm: bool = True,
        lbd: float = 2 / 3,
    ) -> torch.Tensor:
        """Generalized Laplacian Smoothing Filter

        Args:
            adj (sp.csr_matrix): 2D sparse adj *without self-loops*
            layer (int):numbers of linear layers
            norm (str):normalize mode of Laplacian matrix
            renorm (bool): If with the renormalization trick

        Returns:
            adjs (sp.csr_matrix):Laplacian Smoothing Filter
        """
        adj = sp.coo_matrix(adj)
        ident = sp.eye(adj.shape[0])
        if renorm:
            adj_ = adj + ident
        else:
            adj_ = adj

        self.adj_orig = adj_

        rowsum = np.array(adj_.sum(1))

        if norm == "sym":
            degree_mat_inv_sqrt = sp.diags(np.power(rowsum, -0.5).flatten())
            adj_normalized = (adj_.dot(degree_mat_inv_sqrt).transpose().dot(
                degree_mat_inv_sqrt).tocoo())
            laplacian = ident - adj_normalized
        elif norm == "left":
            degree_mat_inv_sqrt = sp.diags(np.power(rowsum, -1.0).flatten())
            adj_normalized = degree_mat_inv_sqrt.dot(adj_).tocoo()
            laplacian = ident - adj_normalized

        reg = [lbd] * (layer)

        adjs = []
        for i in reg:
            adjs.append(ident - (i * laplacian))

        return adjs

    def update_features(self, adj):
        """Check whether adj matrix needs to remove self-loops"""
        sm_fea_s = sp.csr_matrix(self.features).toarray()

        adj_cp = copy.deepcopy(adj)

        adj_norm_s = self.preprocess_graph(
            adj_cp,
            layer=1,
            norm="sym",
        )
        adj_csr = adj_norm_s[0] if len(adj_norm_s) > 0 else adj_cp

        for a in adj_norm_s:
            sm_fea_s = a.dot(sm_fea_s)
        self.sm_fea_s = torch.FloatTensor(sm_fea_s).to(self.device)

        self.pos_weight = torch.FloatTensor([
            (float(adj_csr.shape[0] * adj_csr.shape[0] - adj_csr.sum()) /
             adj_csr.sum())
        ]).to(self.device)
        self.norm_weights = (adj_csr.shape[0] * adj_csr.shape[0] / float(
            (adj_csr.shape[0] * adj_csr.shape[0] - adj_csr.sum()) * 2))

        self.lbls = torch.FloatTensor(adj_csr.todense()).view(-1).to(
            self.device)

        # self.pos_weight = torch.FloatTensor(
        #     [
        #         float(self.adj_orig.shape[0] * self.adj_orig.shape[0] - self.adj_orig.sum())
        #         / self.adj_orig.sum()
        #     ]
        # ).to(self.device)
        # self.norm_weights = (
        #     self.adj_orig.shape[0]
        #     * self.adj_orig.shape[0]
        #     / float((self.adj_orig.shape[0] * self.adj_orig.shape[0] - self.adj_orig.sum()) * 2)
        # )
        # self.lbls = torch.FloatTensor(self.adj_orig.todense()).view(-1).to(self.device)

    def forward(self):
        z = self.encoder(self.sm_fea_s)
        preds = self.inner_product_decoder(z).view(-1)
        return z, preds

    def fit(
        self,
        graph: dgl.DGLGraph,
        device: torch.device,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Fitting

        Args:
            adj (sp.csr_matrix): 2D sparse adj.
            features (torch.Tensor): features.
        """
        self.device = device
        self.features = graph.ndata["feat"]
        adj = self.adj_orig = graph.adj_external(scipy_fmt="csr")
        self.n_nodes = self.features.shape[0]

        adj = eliminate_zeros(adj)

        self.to(self.device)

        self.update_features(adj=adj)

        best_loss = 1e9
        cnt = 0
        best_epoch = 0

        for epoch in range(self.n_epochs):
            self.train()
            self.optimizer.zero_grad()

            _, preds = self.forward()
            loss = self.bce_loss(
                preds,
                self.lbls,
                norm=self.norm_weights,
                pos_weight=self.pos_weight,
            )

            loss.backward()

            self.optimizer.step()
            cur_loss = loss.item()

            print(f"Epoch: {epoch}, embeds_loss={cur_loss}")

            if cur_loss < best_loss:
                cnt = 0
                best_epoch = epoch
                best_loss = cur_loss
                del self.best_model
                self.best_model = copy.deepcopy(self).to(self.device)
                # self.embedding = z_mu.data.cpu().numpy()
                # self.memberships = kmeans.labels_

            else:
                cnt += 1
                print(f"loss increase count:{cnt}")
                if cnt >= self.estop_steps:
                    print(f"early stopping,best epoch:{best_epoch}")
                    break

        return

    def get_embedding(self):
        # with torch.no_grad():
        #     mu = self.encoder(self.sm_fea_s)

        mu, _ = self.best_model()
        return mu.detach()
