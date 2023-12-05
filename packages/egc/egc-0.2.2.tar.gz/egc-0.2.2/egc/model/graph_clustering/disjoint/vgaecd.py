"""
VGAECD
"""
import math
from typing import Tuple

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from sklearn.mixture import GaussianMixture
from torch import nn

from ....utils import normal_reparameterize
from ....utils import sparse_mx_to_torch_sparse_tensor
from ....utils.initialization import init_weights
from ....utils.normalization import normalize_feature
from ....utils.normalization import symmetrically_normalize_adj
from ...node_embedding.vgae import Decoder
from ...node_embedding.vgae import Encoder
from ..base import Base


class VGAECD(Base, nn.Module):
    """VGAECD

    Args:
        in_features (int): input feature dimension.
        n_clusters (int): cluster num.
        alpha (float): coefficient of reconstruction loss. Defaults to 25.0.
        beta (float): coefficient of the loss except reconstruction loss. Defaults to 1.0.
        hidden_units_1 (int): hidden units size of gcn_1. Defaults to 32.
        hidden_units_2 (int): hidden units size of gcn_2. Defaults to 16.
        n_epochs (int, optional): number of embedding training epochs. Defaults to 200.
        early_stopping_epoch (int, optional): early stopping threshold. Defaults to 20.
        lr (float, optional): learning rate. Defaults to 0.01.
        l2_coef (float, optional): weight decay. Defaults to 0.0.
        activation (str, optional): activation of gcn layer_1. Defaults to 'relu'.
    """

    def __init__(
        self,
        in_features: int,
        n_clusters: int,
        alpha: float = 25.0,
        beta: float = 1.0,
        hidden_units_1: int = 32,
        hidden_units_2: int = 16,
        n_epochs: int = 800,
        early_stopping_epoch: int = 20,
        n_epochs_pretrain: int = 200,
        lr: float = 0.01,
        l2_coef: float = 0.0,
        activation: str = "relu",
    ):
        super().__init__()
        nn.Module.__init__(self)
        self.n_clusters = n_clusters
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.n_epochs_pretrain = n_epochs_pretrain
        self.alpha = alpha
        self.beta = beta
        self.encoder = Encoder(in_features, hidden_units_1, hidden_units_2,
                               activation)
        self.decoder = Decoder()

        self.pi = nn.Parameter(torch.FloatTensor(self.n_clusters))
        self.mu = nn.Parameter(
            torch.FloatTensor(self.n_clusters, hidden_units_2))
        self.logvar = nn.Parameter(
            torch.FloatTensor(self.n_clusters, hidden_units_2))
        self.optimizer = torch.optim.Adam(self.parameters(),
                                          lr=lr,
                                          weight_decay=l2_coef)
        self.features_norm = None
        self.adj_norm = None
        self.adj_label = None
        self.n_nodes = None
        self.pos_weight = None
        self.norm = None
        self.embedding_pretrain = None

    def _initialize_gmm(self) -> None:
        with torch.no_grad():
            mu, logvar, _ = self.encoder(self.features_norm, self.adj_norm)
            mu = torch.squeeze(mu, 0)
            logvar = torch.squeeze(logvar, 0)
            z = normal_reparameterize(mu, logvar, self.training)
        z = z.cpu().detach().numpy()
        gmm = GaussianMixture(n_components=self.n_clusters,
                              covariance_type="diag")
        gmm.fit(z)
        self.pi.data = torch.FloatTensor(gmm.weights_)
        self.mu.data = torch.FloatTensor(gmm.means_)
        self.logvar.data = torch.log(torch.FloatTensor(gmm.covariances_))

    def recon_loss(self, adj_hat: torch.Tensor) -> torch.Tensor:
        return self.norm * F.binary_cross_entropy_with_logits(
            adj_hat, self.adj_label, pos_weight=self.pos_weight)

    def _calculate_pretrain_loss(self, adj_hat: torch.Tensor, mu: torch.Tensor,
                                 logvar: torch.Tensor) -> torch.Tensor:
        recon_loss = self.recon_loss(adj_hat)
        kl = (-1 / (2 * self.n_nodes) * torch.mean(
            torch.sum(1 + 2 * logvar - mu.pow(2) - torch.exp(logvar).pow(2),
                      1)))
        return recon_loss + kl

    def _calculate_loss(self, adj_hat: torch.Tensor, mu: torch.Tensor,
                        logvar: torch.Tensor) -> torch.Tensor:
        recon_loss = self.recon_loss(adj_hat)

        z = normal_reparameterize(mu, logvar, self.training).unsqueeze(1)
        mu_c = self.mu.unsqueeze(0).cuda()
        logvar_c = self.logvar.unsqueeze(0).cuda()
        pi_c = self.pi.unsqueeze(0).unsqueeze(2).cuda()
        weights = torch.softmax(pi_c, dim=1)

        p_z_c = (torch.squeeze(weights, 2) * torch.exp(
            torch.sum(
                -0.5 * torch.log(2 * math.pi * torch.exp(logvar_c)) -
                0.5 * torch.square(z - mu_c) / torch.exp(logvar_c),
                dim=2,
            )) + 1e-10)
        gamma = p_z_c / torch.sum(p_z_c, dim=1, keepdim=True)
        hidden = z.shape[2]
        gamma_t = gamma.unsqueeze(2).repeat((1, 1, hidden))

        com_loss = torch.mean(
            torch.sum(
                0.5 * gamma_t *
                (logvar_c + torch.exp(
                    (2 * logvar).unsqueeze(1)) / torch.exp(logvar_c) +
                 torch.square(mu.unsqueeze(1) - mu_c) / torch.exp(logvar_c)),
                dim=(1, 2),
            ) - 0.5 * torch.sum(2 * logvar + 1, dim=1) -
            torch.sum(torch.log(torch.squeeze(weights, 2)) * gamma, dim=1) +
            torch.sum(torch.log(gamma) * gamma, dim=1))

        return self.alpha * recon_loss + self.beta * com_loss

    def forward(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        mu, logvar, _ = self.encoder(self.features_norm, self.adj_norm)
        adj_hat = self.decoder(mu, logvar, self.training)
        return adj_hat, torch.squeeze(mu, 0), torch.squeeze(logvar, 0)

    def fit(self, features: sp.lil_matrix, adj_orig: sp.csr_matrix) -> None:
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
        self.pi.data = torch.zeros_like(self.pi)
        self.mu.data = torch.zeros_like(self.mu)
        self.logvar.data = torch.zeros_like(self.logvar)

        for module in self.modules():
            init_weights(module)

        if torch.cuda.is_available():
            print("GPU available: VGAECD Embedding Using CUDA")
            self.cuda()
            self.features_norm = self.features_norm.cuda()
            self.adj_norm = self.adj_norm.cuda()
            self.adj_label = torch.FloatTensor(self.adj_label.todense()).cuda()
            self.pos_weight = torch.FloatTensor([self.pos_weight]).cuda()

        for epoch in range(self.n_epochs_pretrain):
            self.train()
            self.optimizer.zero_grad()
            adj_hat, mu, logvar = self.forward()
            loss = self._calculate_pretrain_loss(adj_hat, mu, logvar)

            print(f"Pretrain Epoch:{epoch+1}  Loss:{loss}")

            loss.backward()
            self.optimizer.step()

        self.embedding_pretrain, _, _ = self.encoder(self.features_norm,
                                                     self.adj_norm)
        self._initialize_gmm()

        best = 1e9
        cnt_wait = 0
        for epoch in range(self.n_epochs):
            self.train()
            self.optimizer.zero_grad()
            adj_hat, mu, logvar = self.forward()
            loss = self._calculate_loss(adj_hat, mu, logvar)

            print(f"Epoch:{epoch+1}  Loss:{loss}")
            if loss < best:
                best = loss
                cnt_wait = 0
                torch.save(self.state_dict(), "best_vgaecd.pkl")
            else:
                cnt_wait += 1

            if cnt_wait == self.early_stopping_epoch:
                print("Early stopping!")
                break

            loss.backward()
            self.optimizer.step()

    def get_embedding(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        self.load_state_dict(torch.load("best_vgaecd.pkl"))
        mu, _, _ = self.encoder(self.features_norm, self.adj_norm)
        return mu.detach()

    def get_memberships(self) -> np.ndarray:
        with torch.no_grad():
            mu, logvar, _ = self.encoder(self.features_norm, self.adj_norm)
            z = normal_reparameterize(torch.squeeze(mu, 0),
                                      torch.squeeze(logvar, 0),
                                      self.training).unsqueeze(1)
            mu_c = self.mu.unsqueeze(0).cuda()
            logvar_c = self.logvar.unsqueeze(0).cuda()
            pi_c = self.pi.unsqueeze(0).unsqueeze(2).cuda()
            weights = torch.softmax(pi_c, dim=1)

            p_z_c = torch.squeeze(weights, 2) * torch.exp(
                torch.sum(
                    -0.5 * torch.log(2 * math.pi * torch.exp(logvar_c)) -
                    0.5 * torch.square(z - mu_c) / (torch.exp(logvar_c)),
                    dim=2,
                ))
            y = p_z_c / torch.sum(p_z_c, dim=1, keepdim=True)

            pred = torch.argmax(y, dim=1)
        return pred.cpu().numpy()


# if __name__ == "__main__":
#     """for test only
#     """
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import sk_clustering
#     graph, label = load_data(dataset_name='Cora', directory='./data')
#     n_clusters = int(torch.max(label) - torch.min(label) + 1)
#     features = graph.ndata["feat"]
#     adj = graph.adj()
#     adj_csr = sp.csr_matrix(adj.to_dense())
#     features_lil = sp.lil_matrix(features)
#     model = VGAECD(in_features=features_lil.shape[1],
#                    n_clusters=n_clusters,
#                    hidden_units_1=128,
#                    hidden_units_2=64,
#                    alpha=25.0,
#                    beta=1.0,
#                    lr=0.01,
#                    early_stopping_epoch=20,
#                    n_epochs=800,
#                    n_epochs_pretrain=200,
#                    activation='relu')
#     model.fit(features_lil, adj_csr)
#     res = model.get_memberships()
#     emb, emb_pre = model.get_embedding()
#     res1 = sk_clustering(torch.squeeze(emb, 0).cpu(),
#                          n_clusters,
#                          name='kmeans')
#     res_pre = sk_clustering(torch.squeeze(emb_pre, 0).cpu(),
#                             n_clusters,
#                             name='kmeans')
#     if len(res) != 0:
#         (
#             ARI_score,
#             NMI_score,
#             ACC_score,
#             Micro_F1_score,
#             Macro_F1_score,
#         ) = evaluation(label, res)
#         print("\n"
#               f"ARI:{ARI_score}\n"
#               f"NMI:{ NMI_score}\n"
#               f"ACC:{ACC_score}\n"
#               f"Micro F1:{Micro_F1_score}\n"
#               f"Macro F1:{Macro_F1_score}\n")
#     if len(res1) != 0:
#         (
#             ARI_score,
#             NMI_score,
#             ACC_score,
#             Micro_F1_score,
#             Macro_F1_score,
#         ) = evaluation(label, res1)
#         print("\n"
#               f"ARI:{ARI_score}\n"
#               f"NMI:{ NMI_score}\n"
#               f"ACC:{ACC_score}\n"
#               f"Micro F1:{Micro_F1_score}\n"
#               f"Macro F1:{Macro_F1_score}\n")
#     if len(res_pre) != 0:
#         (
#             ARI_score,
#             NMI_score,
#             ACC_score,
#             Micro_F1_score,
#             Macro_F1_score,
#         ) = evaluation(label, res_pre)
#         print("\n"
#               f"ARI:{ARI_score}\n"
#               f"NMI:{ NMI_score}\n"
#               f"ACC:{ACC_score}\n"
#               f"Micro F1:{Micro_F1_score}\n"
#               f"Macro F1:{Macro_F1_score}\n")
