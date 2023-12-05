"""
GAT for DAEGC
"""
# pylint:disable=no-self-use
import torch
import torch.nn.functional as F
from torch import nn


class GAT(nn.Module):
    """GAT for DAEGC

    Args:
        num_features (int): input feature dimension.
        hidden_size (int): number of units in hiddin layer.
        embedding_size (int): number of output emb dim.
        alpha (float): Alpha for the leaky_relu.
    """

    def __init__(self, num_features, hidden_size, embedding_size, alpha):
        super().__init__()
        self.hidden_size = hidden_size
        self.embedding_size = embedding_size
        self.alpha = alpha
        self.conv1 = GATLayer(num_features, hidden_size, alpha)
        self.conv2 = GATLayer(hidden_size, embedding_size, alpha)

    def forward(self, x, adj, M):
        """Forward Propagation

        Args:
            x (torch.Tensor): features of nodes
            adj (torch.Tensor): adj matrix
            M (torch.Tensor): the topological relevance of node j to node i up to t orders.

        Returns:
            A_pred (torch.Tensor): Reconstructed adj matrix
            z (torch.Tensor): latent representation
        """
        h = self.conv1(x, adj, M)
        h = self.conv2(h, adj, M)
        z = F.normalize(h, p=2, dim=1)
        A_pred = self.dot_product_decode(z)
        return A_pred, z

    def dot_product_decode(self, Z):
        """dot product decode

        Args:
            Z (torch.Tensor): node embedding.

        Returns:
            torch.Tensor: Reconstructed adj matrix
        """
        A_pred = torch.sigmoid(torch.matmul(Z, Z.t()))
        return A_pred


class GATLayer(nn.Module):
    """Simple GAT layer, similar to https://arxiv.org/abs/1710.10903

    Args:
        in_features (int): dim num of input
        out_features (int): dim num of output
        alpha (float): Alpha for the leaky_relu.
    """

    def __init__(self, in_features, out_features, alpha=0.2):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha

        self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
        nn.init.xavier_uniform_(self.W.data, gain=1.414)

        self.a_self = nn.Parameter(torch.zeros(size=(out_features, 1)))
        nn.init.xavier_uniform_(self.a_self.data, gain=1.414)

        self.a_neighs = nn.Parameter(torch.zeros(size=(out_features, 1)))
        nn.init.xavier_uniform_(self.a_neighs.data, gain=1.414)

        self.leakyrelu = nn.LeakyReLU(self.alpha)

    # pylint:disable=no-else-return
    def forward(self, x, adj, M, concat=True):
        """Forward Propagation

        Args:
            x (torch.Tensor): features of nodes
            adj (torch.Tensor): adj matrix
            M (torch.Tensor): the topological relevance of node j to node i up to t orders.
            concat (bool,optional):if concat

        Returns:
            (torch.Tensor): latent representation

        """
        h = torch.mm(x, self.W)

        attn_for_self = torch.mm(h, self.a_self)  # (N,1)
        attn_for_neighs = torch.mm(h, self.a_neighs)  # (N,1)
        attn_dense = attn_for_self + torch.transpose(attn_for_neighs, 0, 1)
        attn_dense = torch.mul(attn_dense, M)
        attn_dense = self.leakyrelu(attn_dense)  # (N,N)

        zero_vec = -9e15 * torch.ones_like(adj)
        adj = torch.where(adj > 0, attn_dense, zero_vec)
        attention = F.softmax(adj, dim=1)
        h_prime = torch.matmul(attention, h)

        if concat:
            return F.elu(h_prime)
        else:
            return h_prime

    def __repr__(self):
        return (self.__class__.__name__ + " (" + str(self.in_features) +
                " -> " + str(self.out_features) + ")")
