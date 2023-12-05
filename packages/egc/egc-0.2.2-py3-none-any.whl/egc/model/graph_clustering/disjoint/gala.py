"""GALA
"""
# import numpy as np
# import scipy.sparse as sp
import torch
import torch.nn.functional as F
from sklearn.cluster import SpectralClustering
from torch import nn
from torch import optim


class GALA(nn.Module):
    """
    GALA
    """

    def __init__(
        self,
        adj: torch.Tensor,
        X: torch.Tensor,
        lr: float = 1e-4,
        epochs: int = 1000,
        hidden1: int = 800,
        hidden2: int = 700,
        n_clusters: int = 7,
    ):
        super().__init__()

        self.A = adj
        self.D = torch.sum(adj.to_dense(), 1)
        X[X > 0.0] = 1.0
        self.X = X

        self.lr = lr
        self.epochs = epochs
        self.hidden1 = hidden1
        self.hidden2 = hidden2
        self.n_clusters = n_clusters
        self.labels = None

        self.encoder_1 = nn.Linear(self.X.shape[1], hidden1, bias=False)
        self.encoder_2 = nn.Linear(hidden1, hidden2, bias=False)

        self.decoder_1 = nn.Linear(hidden2, hidden1, bias=False)
        self.decoder_2 = nn.Linear(hidden1, self.X.shape[1], bias=False)

        self.encoder_operator = self.get_encoder_operator()
        self.decoder_operator = self.get_decoder_operator()
        self.init_weights()

    def forward(self):
        EH_1 = F.elu(self.encoder_1(torch.mm(self.encoder_operator, self.X)))
        EH_2 = F.elu(self.encoder_2(torch.mm(self.encoder_operator, EH_1)))

        DH_1 = F.elu(self.decoder_1(torch.mm(self.decoder_operator, EH_2)))
        DH_2 = F.elu(self.decoder_2(torch.mm(self.decoder_operator, DH_1)))
        return EH_2, DH_2

    def init_weights(self):
        """initial the parameter of networks"""
        nn.init.xavier_uniform_(self.encoder_1.weight)
        nn.init.xavier_uniform_(self.encoder_2.weight)
        nn.init.xavier_uniform_(self.decoder_1.weight)
        nn.init.xavier_uniform_(self.decoder_2.weight)
        self.encoder_1.weight.requires_grad_(True)
        self.encoder_2.weight.requires_grad_(True)
        self.decoder_1.weight.requires_grad_(True)
        self.decoder_2.weight.requires_grad_(True)

    def fit(self):
        if torch.cuda.is_available():
            self.A = self.A.cuda()
            self.D = self.D.cuda()
            self.X = self.X.cuda()
            self.encoder_1 = self.encoder_1.cuda()
            self.encoder_2 = self.encoder_2.cuda()
            self.decoder_1 = self.decoder_1.cuda()
            self.decoder_2 = self.decoder_2.cuda()
            self.encoder_operator = self.encoder_operator.cuda()
            self.decoder_operator = self.decoder_operator.cuda()

        weight_decay = 5e-4
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        for i in range(self.epochs):
            self.train()
            H, X_hat = self()
            rec_loss = torch.sum(
                torch.square(X_hat - self.X)) / 2 / X_hat.shape[0]
            for param in self.parameters():
                rec_loss += torch.sum(torch.square(param)) * weight_decay / 2
            optimizer.zero_grad()
            rec_loss.backward()
            optimizer.step()

            print(f"epcoh: {i}: training loss: {rec_loss}")
        self.eval()
        H, X_hat = self()
        spectral_clustering = SpectralClustering(n_clusters=self.n_clusters,
                                                 affinity="nearest_neighbors",
                                                 n_neighbors=20)
        self.labels = spectral_clustering.fit(H.detach().cpu().numpy()).labels_

    def get_encoder_operator(self):
        In = torch.eye(self.A.shape[0])
        A_prime = In + self.A.to_dense()
        D_prime = self.D + 1
        D_inv = torch.diag(torch.pow(D_prime, -0.5))
        encoder_operator = torch.mm(torch.mm(D_inv, A_prime), D_inv)
        return encoder_operator

    def get_decoder_operator(self):
        In = torch.eye(self.A.shape[0])
        A_hat = 2 * In - self.A.to_dense()
        D_hat = self.D + 2
        D_hat_inv = torch.diag(torch.pow(D_hat, -0.5))
        decoder_operator = torch.mm(torch.mm(D_hat_inv, A_hat), D_hat_inv)
        return decoder_operator

    def get_memberships(self):
        return self.labels
