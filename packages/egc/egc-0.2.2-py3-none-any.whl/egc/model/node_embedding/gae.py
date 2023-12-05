"""
GAE embedding
"""
import copy

import dgl
import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from dgl.nn.pytorch.conv import GraphConv
from torch import nn
from torch import optim

from ...module.layers import InnerProductDecoder


def bce_loss(preds, labels, norm, pos_weight):
    cost = norm * F.binary_cross_entropy_with_logits(
        preds,
        labels,
        pos_weight=pos_weight,
    )
    return cost


class DGL_GAE(nn.Module):
    """An implementation of "GAE"

    Args:
        epochs (int, optional): number of embedding training epochs. Defaults to 200.
        n_clusters (int): cluster num.
        fead_dim (int): dim of features
        n_nodes (int): number of nodes
        hidden_dim1 (int): hidden units size of gcn_1. Defaults to 32.
        dropout (int, optional): Dropout rate (1 - keep probability).
        lr (float, optional): learning rate.. Defaults to 0.001.
        early_stop (int, optional): early stopping threshold. Defaults to 10.
        activation (str, optional): activation of gcn layer_1. Defaults to 'relu'.
    """

    def __init__(
        self,
        epochs: int,
        n_clusters: int,
        fead_dim: int,
        n_nodes: int,
        hidden_dim1: int = 32,
        dropout: float = 0.0,
        lr: float = 0.01,
        early_stop: int = 10,
        activation: str = "relu",
    ):
        super().__init__()
        # ---------------Parameters---------------
        self.epochs = epochs
        self.n_clusters = n_clusters
        self.n_nodes = n_nodes
        self.lr = lr
        self.estop_steps = early_stop
        if activation == "prelu":
            self.activation = nn.PReLU()
        elif activation == "relu":
            self.activation = nn.ReLU()
        else:
            self.activation = activation

        self.best_model = None
        self.features = None
        self.adj_orig_graph = None
        self.norm = None
        self.pos_weight = None
        self.device = None

        # ----------------Layers---------------
        self.gconv1 = GraphConv(fead_dim, hidden_dim1)
        self.dc = InnerProductDecoder(dropout)

        # now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # model_name = f'gae_{now}'
        # print(model_name)
        # self.writer = SummaryWriter(f'logs/{model_name}')

    def Encode(self, graph, features):
        """Encoder for GAE

        Args:
            graph (dgl.DGLGraph): Graph data in dgl
            features (torch.Tensor): node's features

        Returns:
            h1 (torch.Tensor):Latent embedding of GAE
        """
        h1 = self.gconv1(graph, features)
        return h1

    def Decode(self, z):
        """Decoder for GAE

        Args:

            features (torch.Tensor): node's features

        Returns:
            h1 (torch.Tensor):Latent embedding of GAE
        """
        return self.dc(z)

    def forward(self):
        """Forward Propagation

        Returns:
            Graph_Reconstruction (torch.Tensor):Reconstructed adj matrix
            Latent_Representation (torch.Tensor):Latent embedding of GAE

        """
        Latent_Representation = self.Encode(self.adj_orig_graph, self.features)
        Graph_Reconstruction = self.Decode(Latent_Representation)
        return Graph_Reconstruction, Latent_Representation

    # pylint: disable=too-many-locals
    def fit(
            self,
            adj_csr: sp.csr_matrix,
            features: torch.Tensor,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        """Fitting a GAE model

        Args:
            adj_csr (sp.lil_matrix): 2D sparse features.
            features (torch.Tensor): node's features.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.device = device
        # ------------------Data--------------
        self.features = features
        # remove diagonal entries
        adj_orig = adj_csr - sp.dia_matrix(
            (adj_csr.diagonal()[np.newaxis, :], [0]), shape=adj_csr.shape)
        adj_orig.eliminate_zeros()

        adj_orig = adj_orig + sp.eye(adj_orig.shape[0])
        self.adj_orig_graph = dgl.from_scipy(adj_orig)

        self.pos_weight = float(adj_csr.shape[0] * adj_csr.shape[0] -
                                adj_csr.sum()) / adj_csr.sum()
        self.norm = (adj_csr.shape[0] * adj_csr.shape[0] / float(
            (adj_csr.shape[0] * adj_csr.shape[0] - adj_csr.sum()) * 2))

        best_loss = 1e9
        cnt = 0
        best_epoch = 0
        optimizer = optim.Adam(self.parameters(), lr=self.lr)

        self.to(self.device)
        self.adj_orig_graph = self.adj_orig_graph.to(self.device)
        self.features = self.features.to(self.device)
        self.pos_weight = torch.FloatTensor([self.pos_weight]).to(self.device)
        target = torch.from_numpy(adj_orig.toarray()).view(-1).to(self.device)

        for epoch in range(self.epochs):
            self.train()
            optimizer.zero_grad()
            Graph_Reconstruction, _ = self.forward()
            pred = Graph_Reconstruction.view(-1)

            loss = bce_loss(
                pred,
                target,
                self.norm,
                self.pos_weight,
            )
            loss.backward()
            cur_loss = loss.item()
            optimizer.step()

            print(
                f"EPOCH_{epoch}",
                f", Loss {cur_loss}",
            )
            if cur_loss < best_loss:
                cnt = 0
                best_epoch = epoch
                best_loss = cur_loss
                del self.best_model
                self.best_model = copy.deepcopy(self)

            else:
                cnt += 1
                print(f"loss increase count:{cnt}")
                if cnt >= self.estop_steps:
                    print(f"early stopping,best epoch:{best_epoch}")
                    break
        print("Optimization Finished!")

    def get_embedding(self) -> np.ndarray:
        """Get the embeddings (graph or node level).

        Returns:
            (numpy.ndarray): embedding.
        """
        self.eval()
        _, z_mu = self.best_model()
        return z_mu.detach()
