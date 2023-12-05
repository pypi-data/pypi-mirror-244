"""SENet Kmeans"""
import numpy as np
import scipy.sparse as sp
import torch
from torch import nn
from torch import optim

from ...utils.normalization import asymmetric_normalize_adj


def get_improved_graph(adj: np.ndarray, lam: float) -> np.ndarray:
    """Get adjacency matrix of the improved graph.

    Args:
        adj (np.ndarray): the adjacency matrix of graph.
        lam (float): hyper-parameters.

    Returns:
        np.ndarray: improved graph.

    :math:`S=|N(v_i)∩N(v_j)|min{N(vi),N(v_j)}`

    :math:`S'_{ij} = S_{ij} >= min{S_{iq} | V q ∈ N(v_i)} ? S_{ij} : 0`

    :math:`A'=A+lamda*S'`
    """
    if sp.issparse(adj):
        adj = adj.todense()
    mask = np.zeros(adj.shape)
    mask[adj > 0] = 1
    # NN_adj
    adj = adj + sp.eye(adj.shape[0])  # Add self loop
    D = np.sum(adj, 1).reshape(-1, 1)  # The degree of each node
    D_t = D.transpose()
    min_node_num = np.minimum(np.tile(D, (1, adj.shape[0])),
                              np.tile(D_t, (adj.shape[0], 1)))
    # min_common_node(i,j) equals the min{|N(vi)|,|N(vj)|}
    common_node_num = adj.dot(adj)
    # adj^2(i,j) : the num of route which length equals two and
    # connect vi and vj  == |N(vi) ∩ N(vj)|
    similarity_matrix = common_node_num / min_node_num

    D_adj = similarity_matrix * mask  # only preserve connected node
    D_adj[D_adj == 0] = 10

    min_adj = np.min(D_adj, 1)
    # get the min simiarity of node vi with its one-hop neighbor
    min_a = min_adj[np.newaxis, :].reshape(-1, 1)
    K_a = similarity_matrix - min_a
    similarity_matrix[K_a < 0] = 0
    # if node vi and node vj are unconnected and their similarity samller than
    # the minimum similarity of its one-hop neighbor,set theri similarity to zero

    imporved_adj = adj + lam * similarity_matrix
    return imporved_adj


class SENetEmbed(nn.Module):
    """SENet Embedding

    Args:
        feature (FloatTensor): node's feature.
        labels (IntTensor): node's label.
        adj (ndarray): graph's adjacency matrix
        n_clusters (int): clusters
        hidden0 (int,optional): hidden units size of gnn layer1. Defaults to 16,
        hidden1 (int,optional): hidden units size of gnn layer2. Defaults to 16,,
        lr (float,optional): learning rate. Defaults to 3e-2,
        epochs (int,optional):  number of embedding training epochs.Defaults to  50,
        weight_decay (float,optional): weight decay.Defaults to 0.0,
        lam (float,optional):Used for construct improved graph . Defaults to 1.0,
        n_iter (int,optional):the times of convoluting feature . Defaults to 3,
        seed (int,optional): random seed. Defaults to 20.
    """

    def __init__(
        self,
        feature: torch.FloatTensor,
        labels: torch.IntTensor,
        adj: np.array,
        n_clusters: int,
        hidden0: int = 16,
        hidden1: int = 16,
        lr: float = 3e-2,
        epochs: int = 50,
        weight_decay: float = 0.0,
        lam: float = 1.0,
        n_iter: int = 3,
    ):
        super().__init__()
        self.feature = feature
        self.labels = labels
        self.n_clusters = n_clusters
        self.adj = adj

        self.W0 = nn.Linear(feature.shape[1], hidden0)
        self.W1 = nn.Linear(hidden0, hidden1)
        self.W2 = nn.Linear(hidden1, self.n_clusters)

        self.lr = lr
        self.epochs = epochs
        self.weight_decay = weight_decay

        self.improved_adj = get_improved_graph(adj, lam)
        self.conv_operator = torch.FloatTensor(
            asymmetric_normalize_adj(self.improved_adj))
        self.improved_feature = self.get_imporved_feature(n_iter, self.feature)
        self.sqrtDb_K_sqrtDb = self.get_normalized_kernel_martix(
            self.improved_feature)

        self.init_weights()

    def forward(self):
        """Get embedding by three networks

        Returns:
            (torch.floatTensor, torch.floatTensor, torch.floatTensor)
            Z1 = tanh(D'^-1 * A' * X * W1)
            Z2 = tanh(D'^-1 * A' * Z1 * W2)
            F = Z2 * W3
            F^T * F = Q * Q^T
            Z3 = F * (Q^-1)^t
        """
        Z_1 = torch.tanh(
            self.W0(torch.matmul(self.conv_operator, self.feature)))
        Z_2 = torch.tanh(self.W1(torch.matmul(self.conv_operator, Z_1)))

        F = self.W2(Z_2)  # F
        FT_mul_F = torch.matmul(F.t(), F)  # FT * F
        Q = torch.cholesky(FT_mul_F)  # Get Q ,FT*F = Q*QT
        Z_3 = torch.matmul(F, Q.inverse().t())  # Z3 = F(Q^-1)T
        return Z_1, Z_2, Z_3

    def get_imporved_feature(self, n_iter, features):
        """Get the improved feature after three convolutions

        Args:
            n_iter (int) : the times of convolution
            features (tensor) : origin graph feature

        Returns:
            (tensor)
            X' = (D'^-1 * A')^3 * X
        """
        if torch.cuda.is_available():
            self.conv_operator = self.conv_operator.cuda()
            features = features.cuda()
        for _ in range(n_iter):  # Get feature after three convolution
            features = self.conv_operator.matmul(features)
        return features

    def get_normalized_kernel_martix(self, feature):
        """Get kernel martix

        Args:
            features (tensor) : improved graph feature

        Returns:
        (tensor)
        K = Relu(X' * X'^T)
        K = (K + K^T)/2
        """
        K = torch.nn.functional.relu(torch.matmul(feature, feature.t()))
        m, _ = torch.sort(K, dim=1, descending=True)
        eps = m[:, round(feature.shape[0] / self.n_clusters)]
        eps = eps.reshape(-1, 1)
        tol = -0.03
        K_m = K - eps
        K[K_m < tol] = 0
        K = (K + K.t()) / 2

        D_bar = torch.sum(K, dim=0)
        sqrt_D_bar = torch.diag(torch.pow(D_bar, -0.5))
        sqrtDb_K_sqrtDb = torch.matmul(torch.matmul(sqrt_D_bar, K), sqrt_D_bar)
        # D^-.5 * K * D^-.5
        return sqrtDb_K_sqrtDb

    def init_weights(self):
        """initial the parameter of networks"""
        nn.init.xavier_uniform_(self.W2.weight)
        nn.init.xavier_uniform_(self.W0.weight)
        nn.init.xavier_uniform_(self.W1.weight)
        self.W2.weight.requires_grad_(True)
        self.W0.weight.requires_grad_(True)
        self.W1.weight.requires_grad_(True)

    def get_embedding(self):
        """Get kernel martix

        Returns:
        (tensor)
        Z = [Z1,Z2,Z3]
        """
        Z_1, Z_2, Z_3 = self()
        Z_1 = Z_1.detach().clone().cpu().numpy()
        Z_2 = Z_2.detach().clone().cpu().numpy()
        Z_3 = Z_3.detach().clone().cpu().numpy()
        Z = np.concatenate((Z_1, Z_2, Z_3), axis=1)
        return torch.Tensor(Z)

    def fit(self):
        """train model"""
        if torch.cuda.is_available():
            self.feature = self.feature.cuda()
            self.improved_feature = self.improved_feature.cuda()
            self.conv_operator = self.conv_operator.cuda()
            self.sqrtDb_K_sqrtDb = self.sqrtDb_K_sqrtDb.cuda()
            self.cuda()
        optimizer = optim.Adam(self.parameters(),
                               lr=self.lr,
                               weight_decay=self.weight_decay)
        for epoch in range(self.epochs):
            self.train()
            _, _, Z_3 = self()
            loss_val = -torch.trace(
                torch.matmul(torch.matmul(Z_3.t(), self.sqrtDb_K_sqrtDb), Z_3))
            # -tr(Z3^T * D^-0.5 * K * D^-0.5 * Z3)
            optimizer.zero_grad()
            loss_val.backward()
            optimizer.step()

            print(f"epoch: {epoch} train loss: {loss_val}")
