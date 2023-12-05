"""Graph Statistics"""
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

import numpy as np
import torch


def count_label(label: torch.Tensor) -> Dict:
    """count label

    Args:
        label (torch.Tensor): label list Tensor

    Returns:
        Dict: label cnt dict
    """
    label_cnt = {}
    if torch.is_tensor(label):
        for l in label.unique():
            label_cnt[l.item()] = torch.sum(label == l).item()
    else:
        for l in np.unique(label):
            label_cnt[l] = np.sum(label == l)

    return label_cnt


def get_intra_class_edges(
    edges: Tuple[np.ndarray, np.ndarray],
    label: List or np.ndarray,
) -> Dict:
    """Get the Dict of intra-class edges index list

    Args:
        edges (Tuple[np.ndarray, np.ndarray]): edges in the format of\
            [(v1,v2,...,vn), (u1,u2,...un))]
        label (Listornp.ndarray): label list

    Returns:
        Dict: edges index list indexed by label
    """
    u, v = edges
    label_dicts = {l: np.nonzero(label == l)[0] for l in np.unique(label)}
    edge_idx = {}
    for l in label_dicts.keys():
        # _u - idx of class l's nodes in u
        # _v - idx of class l's nodes in v
        # np.nonzero(_u & _v)[0] - idx of edges with nodes both in class l
        _u = np.in1d(u, label_dicts[l])
        _v = np.in1d(v, label_dicts[l])
        edge_idx[l] = np.nonzero(_u & _v)[0]
    return edge_idx


def get_intra_class_mean_distance(
    embedding: torch.Tensor,
    label: List or np.ndarray,
) -> Dict:
    """Get intra-class Mean distance between node embeddings and community embeddings

    Args:
        embedding (torch.Tensor): node embedding matrix
        label (Listornp.ndarray): label

    Returns:
        torch.Tensor: mean distance matrix
    """
    label_dicts = {
        l: np.nonzero(label == l)[0]
        for l in sorted(np.unique(label))
    }
    community_embed = {l: embedding[label_dicts[l]] for l in label_dicts}
    intra_class_mean_distance = {
        l:
        torch.mean(
            torch.sum(
                torch.square(community_embed[l] -
                             torch.mean(community_embed[l], dim=0)),
                dim=1,
            ))
        for l in label_dicts
    }
    return torch.stack(list(intra_class_mean_distance.values()))


######################################################################################
# START: This section of code is adapted from https://github.com/SamJia/CommunityGAN #
######################################################################################


def get_neighbor_set(edges: Tuple[torch.Tensor, torch.Tensor]) -> Dict:
    """get neighbor set from edges tuple

    Args:
        edges (Tuple[torch.Tensor, torch.Tensor]): edges list

    Returns:
        Dict: neighbor set indexed by node id
    """
    neighbor_set = {}
    u, v = edges
    u, v = u.numpy(), v.numpy()
    node_set = set(u) | set(v)
    for node in node_set:
        neighbor_set[node] = set(v[u == node]) | set(u[v == node])
    return neighbor_set


def get_motifs_with_one_more_node(motifs: Set[Tuple],
                                  neighbor_set: Dict) -> Set[Tuple]:
    """get motifs recursively

    Args:
        motifs (Set[Tuple]): motifs set
        neighbor_set (Dict): neighbor set indexed by node id

    Returns:
        Set[Tuple]: motifs set enlarged with one more node for each motif
    """
    motifs_next = set()
    for motif in motifs:
        nei = neighbor_set[motif[0]] - set(motif)
        for node in motif[1:]:
            nei = nei & neighbor_set[node]
        for node in nei:
            motifs_next.add(tuple(sorted(list(motif) + [node])))
    return motifs_next


def get_undireced_motifs(
    n_nodes: int, motif_size: int, edges: Tuple[torch.Tensor, torch.Tensor]
) -> Tuple[List[List[Tuple]], Dict, Set[Tuple]]:
    """get motifs(n-clique) of undirected graph

    Args:
        n_nodes (int): node num
        motif_size (int): motif size
        edges (Tuple[torch.Tensor, torch.Tensor]): edges tunple

    Returns:
        Tuple[List[List[Tuple]], Dict, Set[Tuple]]: (motif list indexed by node id, \
            neighbor set indexed by node id, set of notifs)
    """
    motifs = set((node, ) for node in range(n_nodes))
    neighbor_set = get_neighbor_set(edges)
    for i in range(motif_size - 1):
        motifs = get_motifs_with_one_more_node(motifs, neighbor_set)
        print(f"Get {len(motifs)} motifs of {i + 2}-clique")
    id2motifs = [[] for _ in range(n_nodes)]
    for motif in motifs:
        for nid in motif:
            id2motifs[nid].append(motif)
    return id2motifs, neighbor_set, motifs


######################################################################################
# END:   This section of code is adapted from https://github.com/SamJia/CommunityGAN #
######################################################################################
