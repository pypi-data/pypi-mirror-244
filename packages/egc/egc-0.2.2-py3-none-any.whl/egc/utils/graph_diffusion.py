"""
utils of MVGRL
"""
import numpy as np
from scipy.linalg import fractional_matrix_power
from scipy.linalg import inv


def compute_ppr(adj: np.ndarray, alpha: float = 0.2, self_loop: bool = True):
    """Compute Personalized PageRank (PPR) matrix

    Args:
        adj (np.ndarray): adjacency matrix
        alpha (float): Restart probability,. Defaults to 0.2.
        self_loop (bool): add self loop. Defaults to True.

    Returns:
        (np.ndarray): diffusion graph adjacency matrix
    """
    adj = adj.astype(np.float32)
    if self_loop:
        adj = adj + np.eye(adj.shape[0])  # A^ = A + I_n
    d = np.diag(np.sum(adj, 1))  # D^ = Sigma A^_ii
    dinv = fractional_matrix_power(d, -0.5)  # D^(-1/2)
    at = np.matmul(np.matmul(dinv, adj), dinv)  # A~ = D^(-1/2) x A^ x D^(-1/2)
    return alpha * inv(
        (np.eye(adj.shape[0]) - (1 - alpha) * at))  # a(I_n-(1-a)A~)^-1
