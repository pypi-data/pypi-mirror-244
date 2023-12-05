"""
Graph Contrastive Learning Model for SUBLIME
"""
import copy

import torch
import torch.nn.functional as F
from torch import nn
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Sequential

from .gcn_sublime import GCNConv_dense
from .gcn_sublime import GCNConv_dgl

# pylint:disable=no-else-return,protected-access


class GCL_SUBLIME(nn.Module):
    """Graph contrastive learning of SUBLIME

    Args:
        nlayers (int): Number of gcn layers
        in_dim (int): Number of input dim
        hidden_dim (int): Number of hidden dim
        emb_dim (int): Number of embedding dimension
        proj_dim (int): Number of projection dimension
        dropout (float): Dropout rate
        dropout_adj (float): Drop edge rate
        sparse (int): If sparse mode
    """

    def __init__(
        self,
        nlayers,
        in_dim,
        hidden_dim,
        emb_dim,
        proj_dim,
        dropout,
        dropout_adj,
        sparse,
    ):
        super().__init__()

        self.encoder = GraphEncoder(nlayers, in_dim, hidden_dim, emb_dim,
                                    proj_dim, dropout, dropout_adj, sparse)

    def forward(self, x, Adj_, branch=None):
        z, embedding = self.encoder(x, Adj_, branch)
        return z, embedding

    @staticmethod
    def calc_loss(x, x_aug, temperature=0.2, sym=True):
        batch_size, _ = x.size()
        x_abs = x.norm(dim=1)
        x_aug_abs = x_aug.norm(dim=1)

        sim_matrix = torch.einsum("ik,jk->ij", x, x_aug) / torch.einsum(
            "i,j->ij", x_abs, x_aug_abs)
        sim_matrix = torch.exp(sim_matrix / temperature)
        pos_sim = sim_matrix[range(batch_size), range(batch_size)]
        if sym:
            loss_0 = pos_sim / (sim_matrix.sum(dim=0) - pos_sim)
            loss_1 = pos_sim / (sim_matrix.sum(dim=1) - pos_sim)

            loss_0 = -torch.log(loss_0).mean()
            loss_1 = -torch.log(loss_1).mean()
            loss = (loss_0 + loss_1) / 2.0
            return loss
        else:
            loss_1 = pos_sim / (sim_matrix.sum(dim=1) - pos_sim)
            loss_1 = -torch.log(loss_1).mean()
            return loss_1


class SparseDropout(nn.Module):
    """Sparse Dropout

    Args:
        dprob (float): dprob is ratio of dropout. Defaults to 0.5.
    """

    def __init__(self, dprob=0.5):
        super().__init__()
        # dprob is ratio of dropout
        # convert to keep probability
        self.kprob = 1 - dprob

    def forward(self, x):
        mask = ((torch.rand(x._values().size()) + (self.kprob)).floor()).type(
            torch.bool)
        rc = x._indices()[:, mask]
        val = x._values()[mask] * (1.0 / self.kprob)
        return torch.sparse.FloatTensor(rc, val, x.shape)


class GraphEncoder(nn.Module):
    """Graph Encoder of GSL model

    Args:
        nlayers (int): Number of gcn layers
        in_dim (int): Number of input dim
        hidden_dim (int): Number of hidden dim
        emb_dim (int): Number of embedding dimension
        proj_dim (int): Number of projection dimension
        dropout (float): Dropout rate
        dropout_adj (float): Drop edge rate
        sparse (int): If sparse mode
    """

    def __init__(
        self,
        nlayers,
        in_dim,
        hidden_dim,
        emb_dim,
        proj_dim,
        dropout,
        dropout_adj,
        sparse,
    ):
        super().__init__()
        self.dropout = dropout
        self.dropout_adj_p = dropout_adj
        self.sparse = sparse

        self.gnn_encoder_layers = nn.ModuleList()
        if sparse:
            self.gnn_encoder_layers.append(GCNConv_dgl(in_dim, hidden_dim))
            for _ in range(nlayers - 2):
                self.gnn_encoder_layers.append(
                    GCNConv_dgl(hidden_dim, hidden_dim))
            self.gnn_encoder_layers.append(GCNConv_dgl(hidden_dim, emb_dim))
        else:
            self.gnn_encoder_layers.append(GCNConv_dense(in_dim, hidden_dim))
            for _ in range(nlayers - 2):
                self.gnn_encoder_layers.append(
                    GCNConv_dense(hidden_dim, hidden_dim))
            self.gnn_encoder_layers.append(GCNConv_dense(hidden_dim, emb_dim))

        if self.sparse:
            self.dropout_adj = SparseDropout(dprob=dropout_adj)
        else:
            self.dropout_adj = nn.Dropout(p=dropout_adj)

        self.proj_head = Sequential(Linear(emb_dim, proj_dim),
                                    ReLU(inplace=True),
                                    Linear(proj_dim, proj_dim))

    def forward(self, x, Adj_, branch=None):
        if self.sparse:
            if branch == "anchor":
                Adj = copy.deepcopy(Adj_)
            else:
                Adj = Adj_
            Adj.edata["w"] = F.dropout(Adj.edata["w"],
                                       p=self.dropout_adj_p,
                                       training=self.training)
        else:
            Adj = self.dropout_adj(Adj_)

        for conv in self.gnn_encoder_layers[:-1]:
            x = conv(x, Adj)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.gnn_encoder_layers[-1](x, Adj)
        z = self.proj_head(x)
        return z, x
