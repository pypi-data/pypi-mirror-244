"""
CommunityGAN
Adapted from: https://github.com/SamJia/CommunityGAN
"""
import math
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

import numpy as np
import torch
from torch import nn

from ....module import DiscComGAN
from ....module import GeneComGAN
from ....utils import CommunityGANSampling
from ..base import Base


class CommunityGAN(Base, nn.Module):
    """CommunityGAN

    Args:
        n_nodes (int): num of nodes.
        node_emd_init_gen (torch.Tensor): initial node embedding for generator.
        node_emd_init_dis (torch.Tensor): initial node embedding for discriminator.
        max_value (float, optional): max value of embedding. Defaults to 1000.
        n_epochs (int, optional): num of training epochs. Defaults to 10.
        n_epochs_gen (int, optional): num of training epochs for generator. Defaults to 3.
        n_epochs_dis (int, optional): num of traing epochs for discriminator. Defaults to 3.
        gen_interval (int, optional): interval of generator. Defaults to 3.
        dis_interval (int, optional): interval of discriminator. Defaults to 3.
        update_ratio (float, optional): update ratio. Defaults to 1.0.
        n_sample_gen (int, optional): num of samples of generator. Defaults to 5.
        n_sample_dis (int, optional): num of samples of discriminator. Defaults to 5.
        lr_gen (float, optional): learning rate of generator. Defaults to 1e-3.
        lr_dis (float, optional): learning rate of discriminator. Defaults to 1e-3.
        l2_coef (float, optional): l2 coef of optimizers. Defaults to 0.0.
        batch_size_gen (int, optional): batch size of generator. Defaults to 64.
        batch_size_dis (int, optional): batch size of discriminator. Defaults to 64.
    """

    def __init__(
        self,
        n_nodes: int,
        node_emd_init_gen: torch.Tensor,
        node_emd_init_dis: torch.Tensor,
        max_value: float = 1000,
        n_epochs: int = 10,
        n_epochs_gen: int = 3,
        n_epochs_dis: int = 3,
        gen_interval: int = 3,
        dis_interval: int = 3,
        update_ratio: float = 1.0,
        n_sample_gen: int = 5,
        n_sample_dis: int = 5,
        lr_gen: float = 1e-3,
        lr_dis: float = 1e-3,
        l2_coef: float = 0.0,
        batch_size_gen: int = 64,
        batch_size_dis: int = 64,
    ) -> None:
        super().__init__()
        nn.Module.__init__(self)
        self.n_epochs = n_epochs
        self.generator = GeneComGAN(
            n_nodes=n_nodes,
            node_emd_init=node_emd_init_gen,
            n_epochs=n_epochs_gen,
            gen_interval=gen_interval,
            update_ratio=update_ratio,
            n_sample_gen=n_sample_gen,
            lr_gen=lr_gen,
            l2_coef=l2_coef,
            batch_size=batch_size_gen,
            max_value=max_value,
        )
        self.discriminator = DiscComGAN(
            n_nodes=n_nodes,
            node_emd_init=node_emd_init_dis,
            n_epochs=n_epochs_dis,
            dis_interval=dis_interval,
            update_ratio=update_ratio,
            n_sample_dis=n_sample_dis,
            lr_dis=lr_dis,
            l2_coef=l2_coef,
            batch_size=batch_size_dis,
            max_value=max_value,
        )
        self.motif_size = None
        self.total_motifs = None
        self.neighbor_set = None

    def sampling(
        self, g_s_args: Tuple[int, int,
                              bool]) -> Tuple[List[Tuple], List[List[int]]]:
        """sampling

        Args:
            g_s_args (Tuple[int,int,bool]): args tuple for each sample thread.

        Returns:
            Tuple[List[Tuple], List[List[int]]]: (motifs_new, path_new)
        """
        sampler = CommunityGANSampling(
            16,
            g_s_args,
            self.motif_size,
            self.total_motifs,
            self.generator.get_embedding().numpy(),
            self.neighbor_set,
        )
        motifs_new, path_new = sampler.run()
        return motifs_new, path_new

    def forward(self, id2motifs: List[List[Tuple]]) -> None:
        """forward

        Args:
            id2motifs (List[List[Tuple]]): motif lists indexed by node id.
        """
        self.discriminator.fit(self.sampling, id2motifs)
        self.generator.fit(self.discriminator.get_reward, self.sampling)

    def fit(
        self,
        total_motifs: Set[Tuple],
        id2motifs: List[List[Tuple]],
        neighbor_set: Dict,
        motif_size: int = 3,
    ) -> None:
        """fit

        Args:
            total_motifs (Set[Tuple]): set of motifs.
            id2motifs (List[List[Tuple]]): motif lists indexed by node id.
            neighbor_set (Dict): neighbor set Dict indexed by node id.
            motif_size (int, optional): motif size. Defaults to 3.
        """
        self.motif_size = motif_size
        self.total_motifs = total_motifs
        self.neighbor_set = neighbor_set
        # # for test only
        # ce = CommunityEval(community_filename, ground_truth_m)
        # result = ce.eval_community(self.generator.get_embedding())
        # print("gen:" + str(result) + "\n")

        for epoch in range(self.n_epochs):
            print(f"epoch {epoch}")
            self.forward(id2motifs)
            # # for test only
            # ce = CommunityEval(community_filename, ground_truth_m)
            # result = ce.eval_community(self.generator.get_embedding())
            # print("gen:" + str(result) + "\n")

    def get_embedding(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        return (self.generator.get_embedding(),
                self.discriminator.get_embedding())

    def get_memberships(self) -> np.ndarray:
        pred, _ = self.get_disjoint_memberships()
        return pred

    def get_disjoint_memberships(self) -> Tuple[np.ndarray, np.ndarray]:
        """get disjoint membership

        Returns:
            Tuple[np.ndarray, np.ndarray]: generator membership, discriminator membership
        """
        return (
            torch.argmax(self.generator.get_embedding(), dim=1).cpu().numpy(),
            torch.argmax(self.discriminator.get_embedding(),
                         dim=1).cpu().numpy(),
        )

    def get_overlapping_memberships(self) -> Tuple[np.ndarray, np.ndarray]:
        """get overlapping membership

        Returns:
            Tuple[np.ndarray, np.ndarray]: generator membership, discriminator membership
        """
        # ref to BIGCLAM
        epsilon = 1e-8
        threshold = math.sqrt(-math.log(1 - epsilon))
        return (
            self.generator.get_embedding() > threshold,
            self.discriminator.get_embedding() > threshold,
        )
