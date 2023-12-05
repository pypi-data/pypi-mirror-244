"""Metrics
"""
import torch

######################################################################################
# START: This section of code is adapted from https://github.com/bwilder0/clusternet #
######################################################################################


def get_soft_assignment_matrix(
    data: torch.Tensor,
    miu: torch.Tensor,
    cluster_temp: float = 30,
    dist_type: str = "cosine_similarity",
) -> torch.Tensor:
    """Get soft assignment matrix from data points and cluster centers.

    Args:
        data (torch.Tensor): data embeddings.
        miu (torch.Tensor): cluster center embeddings.
        cluster_temp (float, optional): softmax temperature. Defaults to 30.
        dist_type (str, optional): distance type. Defaults to 'cosine_similarity'.

    Returns:
        torch.Tensor: soft assignment matrix.
    """
    n = data.shape[0]
    d = data.shape[1]
    k = miu.shape[0]

    if dist_type == "cosine_similarity":
        dist = torch.cosine_similarity(
            data[:, None].expand(n, k, d).reshape((-1, d)),
            miu[None].expand(n, k, d).reshape((-1, d)),
        ).reshape((n, k))
    elif dist_type == "dot":
        dist = data @ miu.t()

    soft_assignment_matrix = torch.softmax(cluster_temp * dist, 1)

    return soft_assignment_matrix


def get_modularity_matrix(adj_nodia: torch.Tensor) -> torch.Tensor:
    """Get Modularity Matrix.

    .. math::

        A_{vw} - \\frac{K_vk_w}{2m}

    Args:
        adj (torch.Tensor): adjacency matrix without diag.

    Returns:
        torch.Tensor: modularity matrix.
    """
    degrees = adj_nodia.sum(dim=0).unsqueeze(1)
    mod = adj_nodia - degrees @ degrees.t() / adj_nodia.sum()
    return mod


def get_modularity_value(
    bin_adj_nodiag: torch.Tensor,
    r: torch.Tensor,
    mod: torch.Tensor,
) -> torch.Tensor:
    """Get Modularity.

    .. math::

        Q(r)=\\frac{1}{2m}\\sum_{u,v\\in V}\\sum_{k=1}^K[A_{uv}-\\frac{d_ud_v}{2m}]r_{uk}r_{vk}

    Args:
        bin_adj_nodiag (torch.Tensor): n x n. Boolean adj matrix without diag.
        r (torch.Tensor): n x k. Soft assignment probability matrix.
        mod (torch.Tensor): n x n. Modularity matrix.

    Returns:
        torch.Tensor: Modularity value.
    """
    return (1.0 / bin_adj_nodiag.sum()) * (r.t() @ mod @ r).trace()


######################################################################################
# END:   This section of code is adapted from https://github.com/bwilder0/clusternet #
######################################################################################
