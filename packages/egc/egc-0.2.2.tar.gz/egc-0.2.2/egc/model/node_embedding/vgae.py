"""GAE & VGEA

"""
import copy
from typing import Tuple

import dgl
import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from dgl.nn.pytorch.conv import GraphConv
from torch import nn
from torch import optim

from ...module import GCN
from ...module.layers import InnerProductDecoder
from ...utils import init_weights
from ...utils import load_model
from ...utils import normal_reparameterize
from ...utils import normalize_feature
from ...utils import save_model
from ...utils import sparse_mx_to_torch_sparse_tensor
from ...utils import symmetrically_normalize_adj


class Encoder(nn.Module):
    """Encoder for VGAE

    Args:
        in_features (int): input feature dimension.
        hidden_units_1 (int): hidden units size of gcn_1. Defaults to 32.
        hidden_units_2 (int): hidden units size of gcn_2. Defaults to 16.
        activation (str, optional): activation of gcn layer_1. Defaults to 'relu'.
    """

    def __init__(
        self,
        in_features: int,
        hidden_units_1: int = 32,
        hidden_units_2: int = 16,
        activation: str = "relu",
    ):
        super().__init__()
        self.in_features = in_features
        self.gcn_feat = GCN(in_features, hidden_units_1, activation)
        self.gcn_mu = GCN(hidden_units_1, hidden_units_2, lambda x: x)
        self.gcn_sigma = GCN(hidden_units_1, hidden_units_2, lambda x: x)

    def forward(
        self,
        features_norm: torch.Tensor,
        adj_norm: torch.Tensor,
    ) -> Tuple[torch.Tensor]:
        """forward

        Args:
            features_norm (torch.Tensor): features_norm
            adj_norm (torch.Tensor): adj_norm

        Returns:
            Tuple[torch.Tensor]: (mu, log_sigma, feat_hidden)
        """
        feat, _ = self.gcn_feat(features_norm, adj_norm)
        mu, _ = self.gcn_mu(feat, adj_norm)
        log_sigma, _ = self.gcn_sigma(feat, adj_norm)
        return mu, log_sigma, feat


# pylint: disable=no-self-use
class Decoder(nn.Module):
    """Decoder for VGAE"""

    def forward(
        self,
        mu: torch.Tensor,
        log_sigma: torch.Tensor,
        training: bool = True,
    ) -> torch.Tensor:
        """Decoder

        Args:
            mu (torch.Tensor): mu
            log_sigma (torch.Tensor): log_sigma
            training (bool):  isTraining

        Returns:
            (torch.Tensor): A_hat
        """
        z = normal_reparameterize(mu, log_sigma, training)
        return torch.mm(torch.squeeze(z, 0), torch.squeeze(z, 0).t())


class VGAE(nn.Module):
    """VGAE

    Args:
        in_features (int): input feature dimension.
        hidden_units_1 (int): hidden units size of gcn_1. Defaults to 32.
        hidden_units_2 (int): hidden units size of gcn_2. Defaults to 16.
        n_epochs (int, optional): number of embedding training epochs. Defaults to 200.
        early_stopping_epoch (int, optional): early stopping threshold. Defaults to 20.
        lr (float, optional): learning rate.. Defaults to 0.001.
        l2_coef (float, optional): weight decay. Defaults to 0.0.
        activation (str, optional): activation of gcn layer_1. Defaults to 'relu'.
        model_filename (str, optional): path to save best model parameters. Defaults to `vgae`.
    """

    def __init__(
        self,
        in_features: int,
        hidden_units_1: int = 32,
        hidden_units_2: int = 16,
        n_epochs: int = 200,
        early_stopping_epoch: int = 20,
        lr: float = 0.01,
        l2_coef: float = 0.0,
        activation: str = "relu",
        model_filename: str = "vgae",
    ) -> None:
        super().__init__()
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.encoder = Encoder(
            in_features,
            hidden_units_1,
            hidden_units_2,
            activation,
        )
        self.decoder = Decoder()
        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )
        self.features_norm = None
        self.adj_norm = None
        self.adj_label = None
        self.n_nodes = None
        self.pos_weight = None
        self.norm = None

        for module in self.modules():
            init_weights(module)

    def _calculate_loss(
        self,
        adj_hat: torch.Tensor,
        mu: torch.Tensor,
        log_sigma: torch.Tensor,
    ) -> torch.Tensor:
        """Calculation Loss

        Args:
            adj_hat (torch.Tensor): reconstructed adj
            mu (torch.Tensor): mu
            log_sigma (torch.Tensor): logsigma

        Returns:
            torch.Tensor: loss
        """
        reconstruct_loss = self.norm * torch.mean(
            torch.binary_cross_entropy_with_logits(
                adj_hat, self.adj_label, pos_weight=self.pos_weight))

        kl_divergence = (-0.5 / self.n_nodes * torch.mean(
            torch.sum(
                1 + 2 * log_sigma - torch.pow(mu, 2) -
                torch.exp(2 * log_sigma), 1)))

        return reconstruct_loss + kl_divergence

    def forward(self):
        """forward

        Returns:
            loss (torch.Tensor): loss
        """
        mu, log_sigma, _ = self.encoder(self.features_norm, self.adj_norm)

        adj_hat = self.decoder(mu, log_sigma, self.training)

        # NOTE: BUG here when `squeeze(0)` left out as loss will be less after `torch.mean`
        return self._calculate_loss(adj_hat, mu.squeeze(0),
                                    log_sigma.squeeze(0))

    def fit(
        self,
        features: sp.lil_matrix,
        adj_orig: sp.csr_matrix,
    ) -> None:
        """fit

        Args:
            features (sp.lil_matrix): 2D sparse features.
            adj_orig (sp.csr_matrix): 2D sparse adj.
        """
        self.features_norm = torch.FloatTensor(
            normalize_feature(features)[np.newaxis])

        self.adj_label = adj_orig + sp.eye(adj_orig.shape[0])
        self.adj_norm = sparse_mx_to_torch_sparse_tensor(
            symmetrically_normalize_adj(self.adj_label))

        self.n_nodes = adj_orig.shape[0]
        adj_sum = adj_orig.sum()
        self.norm = self.n_nodes * self.n_nodes / float(
            2 * (self.n_nodes * self.n_nodes - adj_sum))
        self.pos_weight = float(self.n_nodes * self.n_nodes -
                                adj_sum) / adj_sum

        if torch.cuda.is_available():
            print("GPU available: VGAE Embedding Using CUDA")
            self.cuda()
            self.features_norm = self.features_norm.cuda()
            self.adj_norm = self.adj_norm.cuda()
            self.adj_label = torch.FloatTensor(self.adj_label.todense()).cuda()
            self.pos_weight = torch.FloatTensor([self.pos_weight]).cuda()

        best = 1e9
        cnt_wait = 0
        for epoch in range(self.n_epochs):
            self.train()
            loss_epoch = 0
            self.optimizer.zero_grad()
            loss = self.forward()

            loss.backward()
            self.optimizer.step()

            loss_epoch = loss_epoch + loss.item()

            print(f"Epoch:{epoch+1}  Loss:{loss}")
            if loss < best:
                best = loss
                cnt_wait = 0
                save_model(
                    self.model_filename,
                    self,
                    self.optimizer,
                    epoch,
                    loss_epoch,
                )
            else:
                cnt_wait += 1

            if cnt_wait == self.early_stopping_epoch:
                print("Early stopping!")
                break

    def get_embedding(
        self,
        model_filename: str = None,
    ) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Args:
            model_filename (str, optional): Model file to load. Defaults to None.

        Returns:
            (torch.Tensor): embedding.
        """
        self, _, _, _ = load_model(
            model_filename
            if model_filename is not None else self.model_filename,
            self,
            self.optimizer,
        )
        mu, _, _ = self.encoder(self.features_norm, self.adj_norm)
        return mu.detach()


def loss_function(preds, labels, mu, logvar, n_nodes, norm, pos_weight):
    pos_weight = torch.FloatTensor([pos_weight])
    cost = norm * F.binary_cross_entropy_with_logits(
        preds,
        labels,
        pos_weight=pos_weight,
    )

    # see Appendix B from VAE paper:
    # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
    # https://arxiv.org/abs/1312.6114
    # 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD = (-0.5 / n_nodes * torch.mean(
        torch.sum(1 + 2 * logvar - mu.pow(2) - logvar.exp().pow(2), 1)))
    return cost + KLD


# -------- DGL_VGEA ------
class DGL_VGAE(nn.Module):
    """DGL_VGAE

    Args:
        epochs (int, optional): number of embedding training epochs. Defaults to 200.
        n_clusters (int): cluster num.
        fead_dim (int): dim of features
        n_nodes (int): number of nodes
        hidden_dim1 (int): hidden units size of gcn_1. Defaults to 32.
        hidden_dim2 (int): hidden units size of gcn_2. Defaults to 16.
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
        hidden_dim2: int = 16,
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

        # self.embedding = None
        # self.memberships = None
        self.features = None
        self.adj_orig_graph = None
        self.norm = None
        self.pos_weight = None
        self.best_model = None
        self.device = None

        # ----------------Layers---------------
        self.gc1 = GraphConv(fead_dim, hidden_dim1, activation=self.activation)
        self.gc2 = GraphConv(hidden_dim1, hidden_dim2)
        self.gc3 = GraphConv(hidden_dim1, hidden_dim2)
        # must have activation
        self.dc = InnerProductDecoder(dropout, act=lambda x: x)

    def encode(self, g, feat):
        """Encoder for VGAE

        Args:
            g (dgl.DGLGraph): Graph data in dgl
            feat (torch.Tensor): node's features
        Returns:
            self.gc2(g, hidden1) (torch.Tensor):latent mean
            self.gc3(g, hidden1) (torch.Tensor):latent log variance
        """
        hidden1 = self.gc1(g, feat)
        return self.gc2(g, hidden1), self.gc3(g, hidden1)

    def reparameterize(self, mu, logvar):
        """reparameterization trick

        Args:
            mu: (torch.Tensor):latent mean
            logvar: (torch.Tensor):latent log variance
        Returns:
            mu: (torch.Tensor):latent mean after reparameterization trick
        """
        if self.training:
            std = torch.exp(logvar)
            eps = torch.randn_like(std)
            return eps.mul(std).add_(mu)
        return mu

    def forward(self):
        """Forward Propagation

        Returns:
            self.dc(z): Reconstructed adj matrix
            mu: (torch.Tensor):latent mean
            logvar: (torch.Tensor):latent log variance
        """
        mu, logvar = self.encode(self.adj_orig_graph, self.features)
        z = self.reparameterize(mu, logvar)
        return self.dc(z), mu, logvar

    # pylint: disable=too-many-locals
    def fit(self, adj_csr, features):
        """Fitting a VGAE model

        Args:
            adj_csr (sp.lil_matrix): 2D sparse features.
            features (torch.Tensor): node's features
        """
        # ------------------Data--------------
        self.features = features
        # remove diagonal entries
        adj_orig = adj_csr - sp.dia_matrix(
            (adj_csr.diagonal()[np.newaxis, :], [0]), shape=adj_csr.shape)
        adj_orig.eliminate_zeros()

        adj_label = adj_orig + sp.eye(adj_orig.shape[0])
        adj_label = torch.FloatTensor(adj_label.toarray())
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

        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            print(f"GPU available: VGAE Embedding Using {self.device}")
            self.cuda()
            self.adj_orig_graph = self.adj_orig_graph.to(self.device)
            self.features = self.features.cuda()
        else:
            self.device = torch.device("cpu")

        for epoch in range(self.epochs):
            self.train()
            optimizer.zero_grad()
            recovered, mu, logvar = self.forward()
            loss = loss_function(
                preds=recovered.cpu(),
                labels=adj_label,
                mu=mu.cpu(),
                logvar=logvar.cpu(),
                n_nodes=self.n_nodes,
                norm=self.norm,
                pos_weight=self.pos_weight,
            )
            loss.backward()
            cur_loss = loss.item()
            optimizer.step()

            # kmeans = KMeans(n_clusters=self.n_clusters,
            #                 n_init=20).fit(mu.data.cpu().numpy())
            # (
            #     ARI_score,
            #     NMI_score,
            #     ACC_score,
            #     Micro_F1_score,
            #     Macro_F1_score,
            # ) = evaluation(label, kmeans.labels_)

            print(
                f"Epoch_{epoch}",
                # f":ARI {ARI_score:.4f}",
                # f", NMI {NMI_score:.4f}",
                # f", ACC {ACC_score:.4f}",
                # f", Micro_F1 {Micro_F1_score:.4f}",
                # f", Macro_F1 {Macro_F1_score:.4f}",
                f", Loss {cur_loss}",
            )
            # if epoch < 10:
            #     continue
            # early stopping
            if cur_loss < best_loss:
                cnt = 0
                best_epoch = epoch
                best_loss = cur_loss
                del self.best_model
                self.best_model = copy.deepcopy(self.to(self.device))
                # self.embedding = mu.data.cpu().numpy()
                # self.memberships = kmeans.labels_
            else:
                cnt += 1
                print(f"loss increase count:{cnt}")
                if cnt >= self.estop_steps:
                    print(f"early stopping,best epoch:{best_epoch}")
                    break

        print("Optimization Finished!")

    def get_embedding(self):
        """Get cluster embedding.

        Returns:numpy.ndarray

        """
        _, mu, _ = self.best_model()
        return mu.detach()

    def get_memberships(self):
        """Get cluster membership.

        Returns:numpy.ndarray

        """
        return self.memberships
