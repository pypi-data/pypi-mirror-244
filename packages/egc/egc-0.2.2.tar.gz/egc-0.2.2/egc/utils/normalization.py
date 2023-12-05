"""
Normalization Utils
"""
import sys

import numpy as np
import scipy.sparse as sp
import torch

# pylint: disable=no-else-return
EOS = 1e-10

############################################################################
# START: This section of code is adapted from https://github.com/tkipf/gcn #
############################################################################


def normalize_feature(features: sp.lil_matrix) -> np.array:
    """Row-normalize feature matrix.

    Args:
        features (scipy.sparse.lil.lil_matrix): 2D sparse features

    Returns:
        features_norm (numpy.matrix): 2D row-normalized features
    """
    row_sum_inv = np.power(np.array(features.sum(1)), -1).flatten()
    row_sum_inv[np.isinf(row_sum_inv)] = 0.0
    row_sum_inv_diag = sp.diags(row_sum_inv)
    return row_sum_inv_diag.dot(features).todense()


def symmetrically_normalize_adj(adj: sp.csr_matrix) -> sp.coo_matrix:
    """Symmetrically normalize adjacency matrix.

    Args:
        adj (scipy.sparse.csr.csr_matrix): 2D sparse adjacency matrix

    Returns:
        daj_norm (scipy.sparse.coo.coo_matrix): 2D Symmetrically normalized sparse adjacency matrix
    """
    adj = sp.coo_matrix(adj)
    rowsum = np.array(adj.sum(1))
    d_inv_sqrt = np.power(rowsum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).tocoo()


############################################################################
# END:   This section of code is adapted from https://github.com/tkipf/gcn #
############################################################################


def asymmetric_normalize_adj(adj, loop=True):
    """Get convolution operator

    Args:
         adj (ndarray) : the adjacency matrix of improved graph
         loop (boolean,optional) : add self loop

     Returns:
     (ndarray)
     convolution_operator = D'^-1 * A'
    """
    if loop:
        adj = adj + sp.eye(adj.shape[0])
    if sp.issparse(adj):
        adj = adj.todense()
    rowsum = np.array(adj.sum(1))
    d_inv = np.power(rowsum, -1.0).flatten()
    d_inv[np.isinf(d_inv)] = 0.0
    d_mat_inv = sp.diags(d_inv)
    conv_operator = d_mat_inv.dot(adj)
    return conv_operator


def normalize_sublime(adj, mode, sparse=False):
    """Normalize adjacency matrix for SUBLIME model

    Args:
        adj: adjacency matrix
        mode (str): mode of normalize adjacency matrix
        sparse (boolean,optional): if use sparse. Defaults to False.

    Returns:
        adj after normalize
    """
    if not sparse:
        if mode == "sym":
            inv_sqrt_degree = 1.0 / (
                torch.sqrt(adj.sum(dim=1, keepdim=False)) + EOS)
            return inv_sqrt_degree[:, None] * adj * inv_sqrt_degree[None, :]
        elif mode == "row":
            inv_degree = 1.0 / (adj.sum(dim=1, keepdim=False) + EOS)
            return inv_degree[:, None] * adj
        else:
            sys.exit("wrong norm mode")
    else:
        adj = adj.coalesce()
        if mode == "sym":
            inv_sqrt_degree = 1.0 / (torch.sqrt(
                torch.sparse.sum(adj, dim=1).values()))
            D_value = (inv_sqrt_degree[adj.indices()[0]] *
                       inv_sqrt_degree[adj.indices()[1]])

        elif mode == "row":
            # aa = torch.sparse.sum(adj, dim=1)
            # bb = aa.values()
            inv_degree = 1.0 / (torch.sparse.sum(adj, dim=1).values() + EOS)
            D_value = inv_degree[adj.indices()[0]]
        else:
            sys.exit("wrong norm mode")
        new_values = adj.values() * D_value

        return torch.sparse.FloatTensor(adj.indices(), new_values, adj.size())
