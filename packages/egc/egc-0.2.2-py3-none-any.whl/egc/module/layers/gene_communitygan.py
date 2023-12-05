"""
Generator Layer
Adapted from: https://github.com/SamJia/CommunityGAN
"""
from typing import Callable
from typing import List
from typing import Tuple

import numpy as np
import torch
from torch import nn


class GeneComGAN(nn.Module):
    """Generator of CommunityGAN

    Args:
        n_nodes (int): num of nodes.
        node_emd_init (torch.Tensor): node embedding in agm format.
        n_epochs (int): num of training epochs.
        gen_interval (int): interval of generator.
        update_ratio (float): update ration.
        n_sample_gen (int): num of samples for generator.
        lr_gen (float): learning rate.
        l2_coef (float): l2 coef.
        batch_size (int): batch size.
        max_value (int): max value for embedding matrix.
    """

    def __init__(
        self,
        n_nodes: int,
        node_emd_init: torch.Tensor,
        n_epochs: int,
        gen_interval: int,
        update_ratio: float,
        n_sample_gen: int,
        lr_gen: float,
        l2_coef: float,
        batch_size: int,
        max_value: int,
    ):
        super().__init__()
        self.n_nodes = n_nodes
        self.n_epochs = n_epochs
        self.gen_interval = gen_interval
        self.update_ratio = update_ratio
        self.n_sample_gen = n_sample_gen
        self.batch_size = batch_size
        self.max_value = max_value

        self.embedding_matrix = nn.Parameter(torch.FloatTensor(node_emd_init),
                                             requires_grad=True)
        self.embedding_matrix.data = torch.FloatTensor(node_emd_init)
        self.optimizer = torch.optim.Adam(self.parameters(),
                                          lr=lr_gen,
                                          weight_decay=l2_coef)

    def prepare_data_for_g(
            self, rewardFunc: Callable,
            sampling: Callable) -> Tuple[List[Tuple], List[List]]:
        """sample subsets for the generator

        Args:
            rewardFunc (Callable): function of getting discriminator reward.
            sampling (Callable): sampling function.

        Returns:
            Tuple[List[Tuple], List[List]]: (list of motifs sampled, list of labels)
        """
        g_s_args = []
        for i in range(self.n_nodes):
            if torch.rand(1) < self.update_ratio:
                g_s_args.append((i, self.n_sample_gen, False))

        motifs_new, _ = sampling(g_s_args)
        motifs_new = [j for i in motifs_new for j in i]

        reward_new = []
        for i in range(0, len(motifs_new), 10000):
            reward_new.append(rewardFunc(np.array(motifs_new[i:i + 10000])))
        reward_new = np.concatenate(reward_new)

        motifs_idx = list(range(len(motifs_new)))
        np.random.shuffle(motifs_idx)
        motifs_new = [motifs_new[i] for i in motifs_idx]
        reward_new = [reward_new[i] for i in motifs_idx]

        return motifs_new, reward_new

    def forward(self, motifs: List[Tuple], reward: List[List]) -> torch.Tensor:
        """forward

        Args:
            motifs (List[Tuple]): motifs.
            reward (List[List]): reward.

        Returns:
            torch.Tensor: loss.
        """
        score = torch.sum(torch.prod(self.embedding_matrix[motifs], dim=1),
                          dim=1)
        p = torch.clip(1 - torch.exp(-score), 1e-5, 1)

        loss = -torch.mean(p * reward)
        return loss

    def fit(self, rewardFunc: Callable, sampling: Callable) -> None:
        """fit

        Args:
            rewardFunc (Callable): function for getting discriminator reward.
            sampling (Callable): sampling function.
        """
        motifs = []
        reward = []
        for epoch in range(self.n_epochs):
            self.train()

            if epoch % self.gen_interval == 0:
                motifs, reward = self.prepare_data_for_g(rewardFunc, sampling)

            train_size = len(motifs)
            start_list = list(range(0, train_size, self.batch_size))
            np.random.shuffle(start_list)

            for start in start_list:
                self.zero_grad()
                end = start + self.batch_size
                loss = self.forward(torch.LongTensor(motifs[start:end]),
                                    torch.Tensor(reward[start:end]))
                loss.backward()
                self.optimizer.step()
                self.embedding_matrix.data = torch.clip(
                    self.embedding_matrix.data, 0, self.max_value)
            print(f"generator epoch {epoch} loss {loss}")

    def get_embedding(self) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        return self.embedding_matrix.detach()
