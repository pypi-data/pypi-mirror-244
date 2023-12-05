"""
Sample Method
"""
import multiprocessing
import random
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
import torch


def get_repeat_shuffle_nodes_list(n_nodes, sample_times):
    """Get Negative Sample Nodes List By Repeatable Shuffle

    Args:
        n_nodes (int): node number in all.
        sample_times (int): sample times.

    Returns:
        (List): list of multiple repeatable nodes index shuffle lists.
    """
    sample_list = []
    for _ in range(sample_times):
        sample_iter = []
        i = 0
        while True:
            randnum = np.random.randint(0, n_nodes)
            if randnum != i:
                sample_iter.append(randnum)
                i = i + 1
            if len(sample_iter) == n_nodes:
                break
        sample_list.append(sample_iter)
    return sample_list


def normal_reparameterize(mu: torch.Tensor,
                          logvar: torch.Tensor,
                          training: bool = True) -> torch.Tensor:
    """Reparameterization trick for normal distribution

    Args:
        mu (torch.Tensor): mu
        logvar (torch.Tensor): logsigma
        training (bool):  isTraining

    Returns:
        (torch.Tensor)
    """
    if training:
        std = torch.exp(logvar)
        eps = torch.randn_like(std)
        return eps.mul(std).add_(mu)
    return mu


######################################################################################
# START: This section of code is adapted from https://github.com/SamJia/CommunityGAN #
######################################################################################


def agm(x: np.ndarray) -> np.ndarray:
    """AGM probability

    Args:
        x (np.ndarray): 1-d array

    Returns:
        np.ndarray: AGM probability
    """
    agm_x = 1 - np.exp(-x)
    agm_x[np.isnan(agm_x)] = 0
    return np.clip(agm_x, 1e-6, 1)


def choice(samples: List[int], weight: np.ndarray) -> int:
    """choose next node

    Args:
        samples (List[int]): neighbors
        weight (np.ndarray): wights

    Returns:
        int: node chosen
    """
    s = np.sum(weight)
    target = random.random() * s
    for si, wi in zip(samples, weight):
        if target < wi:
            return si
        target -= wi
    return samples[-1]


class CommunityGANSampling:
    """CommunityGAN Sampling

    Args:
        n_threads (int): cores of multiprocessing.
        args (Tuple[int, int, bool]): root, n_sample, only_neg.
                root (int): root node id
                n_sample (int): num of motif sampled
                only_neg (bool): only return negative samples
        motif_size (int): motif size.
        total_motifs (List[List[Tuple]]): list of all motifs indexed by node id.
        theta_g (np.ndarray): node embedding of generator.
        neighbor_set (Dict): neighbor set Dict indexed by node id.
    """

    def __init__(
        self,
        n_threads: int,
        args: Tuple[int, int, bool],
        motif_size: int,
        total_motifs: List[List[Tuple]],
        theta_g: np.ndarray,
        neighbor_set: Dict,
    ) -> None:
        super().__init__()
        self.n_threads = n_threads
        self.args = args
        self.motif_size = motif_size
        self.total_motifs = total_motifs
        self.theta_g = theta_g
        self.neighbor_set = neighbor_set

    def g_v(self, roots: List[int]) -> Tuple[int, List[int]]:
        """get next node

        Args:
            roots (List[int]): list of node sampled before

        Returns:
            Tuple[int, List[int]]: current_node, path walked
        """
        g_v_v = self.theta_g[roots[0]]
        for nid in roots[1:]:
            g_v_v *= self.theta_g[nid]
        current_node = roots[-1]
        previous_nodes = set()
        path = []
        is_root = True
        while True:
            node_neighbor = (list({
                neighbor
                for root in roots
                for neighbor in self.neighbor_set[root]
            }) if is_root else list(self.neighbor_set[current_node]))

            if len(node_neighbor) == 0:
                return None, None

            tmp_g = g_v_v if is_root else g_v_v * self.theta_g[current_node]

            relevance_probability = agm(
                np.sum(self.theta_g[node_neighbor] * tmp_g, axis=1))
            next_node = choice(node_neighbor, relevance_probability)

            if next_node in previous_nodes:  # terminating condition
                break
            previous_nodes.add(current_node)
            current_node = next_node
            path.append(current_node)
            is_root = False

        return current_node, path

    def g_s(self, args: Tuple[int, int,
                              bool]) -> Tuple[List[Tuple], List[List[int]]]:
        """sampling for community gan generator

        Args:
            args (Tuple[int, int, bool]): root, n_sample, only_neg
                root (int): root node id
                n_sample (int): num of motif sampled
                only_neg (bool): only return negative samples

        Returns:
            Tuple[List[Tuple], List[List[int]]]: motifs, paths
        """
        root, n_sample, only_neg = args
        _motifs = []
        _paths = []
        for _ in range(2 * n_sample):
            if len(_motifs) >= n_sample:
                break

            motif = [root]
            path = [root]
            for _ in range(1, self.motif_size):
                v, p = self.g_v(motif)
                if v is None:
                    break
                motif.append(v)
                path.extend(p)

            if len(set(motif)) < self.motif_size:
                continue

            motif = tuple(sorted(motif))
            if only_neg and motif in self.total_motifs:
                continue
            _motifs.append(motif)
            _paths.append(path)

        return _motifs, _paths

    def run(self) -> Tuple[List[Tuple], List[List[int]]]:
        """sampling for community gan

        Returns:
            Tuple[List[Tuple], List[List[int]]]: motifs, paths.
        """
        with multiprocessing.Pool(self.n_threads) as p:
            motifs, paths = zip(*p.map(self.g_s, self.args))
        return motifs, paths


######################################################################################
# END:   This section of code is adapted from https://github.com/SamJia/CommunityGAN #
######################################################################################
