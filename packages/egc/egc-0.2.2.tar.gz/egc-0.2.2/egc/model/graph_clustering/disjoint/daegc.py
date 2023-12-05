"""DAEGC implement
ref:https://github.com/kouyongqi/DAEGC
"""
import gc
import warnings
from copy import deepcopy

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from torch import nn
from torch.nn.parameter import Parameter
from torch.optim import Adam

from ....model.graph_clustering.base import Base
from ....module import GAT
from ....utils import sparse_mx_to_torch_sparse_tensor
from ....utils.evaluation import evaluation
from ....utils.normalization import symmetrically_normalize_adj

warnings.filterwarnings("ignore")


class DAEGC(Base, nn.Module):
    """DAEGC

    Args:
        num_features (int): input feature dimension.
        hidden_size (int): number of units in hiddin layer.
        embedding_size (int): number of output emb dim.
        alpha (float): Alpha for the leaky_relu.
        num_clusters (int): cluster num.
        pretrain_lr (float): learning rate of pretrain model.
        lr (float): learning rate of final model.
        weight_decay (float): weight decay.
        pre_epochs (int): number of epochs to pretrain model.
        epochs (int): number of epochs to final model.
        update_interval (int): update interval of DAEGC.
        estop_steps (int): Number of early_stop steps.
        v (int,optional): Degrees of freedom of the student t-distribution.Defaults to 1.
    """

    def __init__(
        self,
        num_features: int,
        hidden_size: int,
        embedding_size: int,
        alpha: float,
        num_clusters: int,
        pretrain_lr: float,
        lr: float,
        weight_decay: float,
        pre_epochs: int,
        epochs: int,
        update_interval: int,
        estop_steps: int,
        t: int,
        v: int = 1,
    ):
        super().__init__()
        nn.Module.__init__(self)
        # ------------- Parameters ----------------
        self.num_clusters = num_clusters
        self.pretrain_lr = pretrain_lr
        self.lr = lr
        self.weight_decay = weight_decay
        self.pre_epochs = pre_epochs
        self.epochs = epochs
        self.update_interval = update_interval
        self.estop_steps = estop_steps
        self.t = t
        self.v = v
        self.device = None
        self.adj = None
        self.M = None
        self.feats = None
        self.adj_label = None
        self.adj_norm = None

        # ---------------- Layer -------------------
        # GAT AE model
        self.gat = GAT(num_features, hidden_size, embedding_size, alpha)
        # cluster layer
        self.cluster_layer = Parameter(
            torch.Tensor(num_clusters, embedding_size))
        torch.nn.init.xavier_normal_(self.cluster_layer.data)

    def forward(self, x, adj, M):
        """Forward Propagation

        Args:
            x (torch.Tensor): features of nodes
            adj (torch.Tensor): adj matrix
            M (torch.Tensor): the topological relevance of node j to node i up to t orders.

        Returns:
            A_pred (torch.Tensor): Reconstructed adj matrix
            z (torch.Tensor): latent representation
            q (torch.Tensor): Soft assignments
        """
        A_pred, z = self.gat(x, adj, M)
        q = self.get_Q(z)
        return A_pred, z, q

    def fit(self, adj, feats, label):
        """Fitting a DAEGC model

        Args:
            adj (sp.lil_matrix): adj sparse matrix.
            feats (torch.Tensor): features.
            label (torch.Tensor): label of node's cluster
        """
        # -------------- pretrain -------------------
        print("pretrain GAT model...")
        # data preprocessing
        # adj = sparse_mx_to_torch_sparse_tensor(adj).to_dense()
        # adj += torch.eye(adj.shape[0])
        # self.adj_label = deepcopy(adj)
        # adj = normalize(adj, norm="l1")
        # self.adj_norm = torch.from_numpy(adj).to(dtype=torch.float)

        self.adj_label = adj + sp.eye(adj.shape[0])
        self.adj_norm = sparse_mx_to_torch_sparse_tensor(
            symmetrically_normalize_adj(self.adj_label)).to_dense()
        self.adj_label = sparse_mx_to_torch_sparse_tensor(
            self.adj_label).to_dense()

        # get M
        self.M = get_M(self.adj_norm, self.t)
        # feats and label
        self.feats = torch.FloatTensor(feats)
        y = label.cpu().numpy()
        # put data on gpu
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            print(f"GPU available: DAEGC Using {self.device}")
            self.cuda()
            self.adj_label = self.adj_label.to(self.device)
            self.adj_norm = self.adj_norm.to(self.device)
            self.M = self.M.to(self.device)
            self.feats = self.feats.to(self.device)
        else:
            self.device = torch.device("cpu")

        # best_loss = float('inf')
        # last_reduce = 0
        # reduce_cnt = 0
        # best_model = None
        pre_optimizer = Adam(self.gat.parameters(),
                             lr=self.pretrain_lr,
                             weight_decay=self.weight_decay)

        # pretrain model
        for epoch in range(self.pre_epochs):
            self.gat.train()
            A_pred, z = self.gat(self.feats, self.adj_norm, self.M)
            loss = F.binary_cross_entropy(A_pred.view(-1),
                                          self.adj_label.view(-1))
            pre_optimizer.zero_grad()
            cur_loss = loss.item()
            loss.backward()
            pre_optimizer.step()

            # if epoch == 0:
            #     continue
            # if cur_loss < best_loss:
            #     best_loss = cur_loss
            #     last_reduce = epoch
            #     reduce_cnt = 0
            #     best_model = deepcopy(self.gat)
            #     improve = '*'
            # else:
            #     improve = ''
            #     reduce_cnt += 1

            # if reduce_cnt > self.estop_steps:
            #     break

            # print(f'Epoch:{epoch},', f'Train Loss:{cur_loss} {improve}')
            print(f"Epoch:{epoch},", f"Train Loss:{cur_loss}")

        # print(f'Final Epoch:{last_reduce}')
        with torch.no_grad():
            # _, z = best_model(self.feats, self.adj_norm, self.M)
            _, z = self.gat(self.feats, self.adj_norm, self.M)

            kmeans = KMeans(n_clusters=self.num_clusters,
                            n_init=20).fit(z.data.cpu().numpy())

            (
                ARI_score,
                NMI_score,
                ACC_score,
                Micro_F1_score,
                Macro_F1_score,
            ) = evaluation(y, kmeans.labels_)
            print(
                "pretrain",
                f":ARI {ARI_score:.4f}",
                f", NMI {NMI_score:.4f}",
                f", ACC {ACC_score:.4f}",
                f", Micro_F1 {Micro_F1_score:.4f}",
                f", Macro_F1 {Macro_F1_score:.4f}",
            )
        # self.gat = deepcopy(best_model)
        del pre_optimizer, cur_loss, z
        torch.cuda.empty_cache()
        gc.collect()

        # ----------------- Training DAEGC -----------------
        print("Training DAEGC")

        with torch.no_grad():
            _, z = self.gat(self.feats, self.adj_norm, self.M)

        # get kmeans and pretrain cluster result
        kmeans = KMeans(n_clusters=self.num_clusters, n_init=20)
        _ = kmeans.fit_predict(z.data.cpu().numpy())
        self.cluster_layer.data = torch.Tensor(kmeans.cluster_centers_).to(
            self.device)

        # best_loss = float('inf')
        # last_reduce = 0
        # reduce_cnt = 0
        # best_model = None
        optimizer = Adam(self.parameters(),
                         lr=self.lr,
                         weight_decay=self.weight_decay)

        for epoch in range(self.epochs):
            self.train()
            if epoch % self.update_interval == 0:
                # update_interval
                _, _, Q = self(self.feats, self.adj_norm, self.M)

                q = Q.detach().data.cpu().numpy().argmax(1)  # Q

                (
                    ARI_score,
                    NMI_score,
                    ACC_score,
                    Micro_F1_score,
                    Macro_F1_score,
                ) = evaluation(y, q)
                print(
                    f"epoch {epoch}",
                    f":ARI {ARI_score:.4f}",
                    f", NMI {NMI_score:.4f}",
                    f", ACC {ACC_score:.4f}",
                    f", Micro_F1 {Micro_F1_score:.4f}",
                    f", Macro_F1 {Macro_F1_score:.4f}",
                )
            A_pred, z, q = self(self.feats, self.adj_norm, self.M)
            p = target_distribution(Q.detach())

            kl_loss = F.kl_div(q.log(), p, reduction="batchmean")
            re_loss = F.binary_cross_entropy(A_pred.view(-1),
                                             self.adj_label.view(-1))

            loss = 10 * kl_loss + re_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        #     cur_loss = loss.item()
        #     if cur_loss < best_loss:
        #         best_loss = cur_loss
        #         last_reduce = epoch
        #         reduce_cnt = 0
        #         best_model = deepcopy(self.gat)
        #         improve = '*'
        #     else:
        #         improve = ''
        #         reduce_cnt += 1

        #     if reduce_cnt > self.estop_steps:
        #         break
        #     print(f'Epoch:{epoch},', f'Train Loss:{cur_loss} {improve}')
        # print(f'Final Epoch:{last_reduce}')

    def get_Q(self, z):
        """get soft clustering assignment distribution

        Args:
            z (torch.Tensor): node embedding

        Returns:
            torch.Tensor: Soft assignments
        """
        q = 1.0 / (1.0 + torch.sum(
            torch.pow(z.unsqueeze(1) - self.cluster_layer, 2), 2) / self.v)
        q = q.pow((self.v + 1.0) / 2.0)
        q = (q.t() / torch.sum(q, 1)).t()
        return q

    def get_embedding(self):
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        _, z, _ = self(self.feats, self.adj, self.M)
        return z.detach()

    def get_memberships(self):
        """Get the memberships (graph or node level).

        Returns:
            (numpy.ndarray): memberships.
        """
        _, _, Q = self(self.feats, self.adj_norm, self.M)
        q = Q.detach().data.cpu().numpy().argmax(1)  # Q
        return q


def target_distribution(q):
    """get target distribution P

    Args:
        q (torch.Tensor): Soft assignments

    Returns:
        torch.Tensor: target distribution P
    """
    weight = q**2 / q.sum(0)
    return (weight.t() / weight.sum(1)).t()


def get_M(adj, t=2):
    """get the topological relevance of node j to node i up to t orders.

    Args:
        adj (torch.Tensor): adj matrix
        t (int,optional): t order
    Returns:
        torch.Tensor: M
    """
    adj_numpy = adj.cpu().numpy()

    tran_prob = normalize(adj_numpy, norm="l1", axis=0)
    M_numpy = sum(
        [np.linalg.matrix_power(tran_prob, i) for i in range(1, t + 1)]) / t
    return torch.Tensor(M_numpy)
