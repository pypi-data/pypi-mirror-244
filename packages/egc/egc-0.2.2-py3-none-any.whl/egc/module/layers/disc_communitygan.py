"""
Discriminator Layer
Adapted from: https://github.com/SamJia/CommunityGAN
"""
import random
from typing import Callable
from typing import List
from typing import Tuple

import numpy as np
import torch
from torch import nn


class DiscComGAN(nn.Module):
    """Discriminator of CommunityGAN

    Args:
        n_nodes (int): num of nodes.
        node_emd_init (torch.Tensor): node embedding in agm format pretrained in advance.
        n_epochs (int): num of training epochs.
        dis_interval (int): interval for discriminator.
        update_ratio (float): update ratio.
        n_sample_dis (int): num of samples for discriminator.
        lr_dis (float): learning rate.
        l2_coef (float): l2 coef.
        batch_size (int): batch size
        max_value (int): max value for embedding matrix.
    """

    def __init__(
        self,
        n_nodes: int,
        node_emd_init: torch.Tensor,
        n_epochs: int,
        dis_interval: int,
        update_ratio: float,
        n_sample_dis: int,
        lr_dis: float,
        l2_coef: float,
        batch_size: int,
        max_value: int,
    ):
        super().__init__()
        self.n_nodes = n_nodes
        self.n_epochs = n_epochs
        self.dis_interval = dis_interval
        self.update_ratio = update_ratio
        self.n_sample_dis = n_sample_dis
        self.batch_size = batch_size
        self.max_value = max_value

        self.embedding_matrix = nn.Parameter(torch.FloatTensor(node_emd_init),
                                             requires_grad=True)
        self.embedding_matrix.data = torch.FloatTensor(node_emd_init)
        self.optimizer = torch.optim.Adam(self.parameters(),
                                          lr=lr_dis,
                                          weight_decay=l2_coef)

    def prepare_data_for_d(
            self, sampling: Callable,
            id2motifs: List[List[Tuple]]) -> Tuple[List[Tuple], List[List]]:
        """generate positive and negative samples for the discriminator

        Args:
            sampling (Callable): sampling function.
            id2motifs (List[List[Tuple]]): list of motifs indexed by node id.

        Returns:
            Tuple[List[Tuple], List[List]]: (list of motifs sampled, list of labels)
        """
        motifs = []
        labels = []
        g_s_args = []
        poss = []
        negs = []
        for i in range(self.n_nodes):
            if np.random.rand() < self.update_ratio:
                pos = random.sample(id2motifs[i],
                                    min(len(id2motifs[i]), self.n_sample_dis))
                poss.append(pos)
                g_s_args.append((i, len(pos), True))

        negs, _ = sampling(g_s_args)
        for pos, neg in zip(poss, negs):
            if len(pos) != 0 and neg is not None:
                motifs.extend(pos)
                labels.extend([1] * len(pos))
                motifs.extend(neg)
                labels.extend([0] * len(neg))

        motifs_idx = list(range(len(motifs)))
        np.random.shuffle(motifs_idx)
        motifs = [motifs[i] for i in motifs_idx]
        labels = [labels[i] for i in motifs_idx]
        return motifs, labels

    def forward(self,
                motifs: List[Tuple],
                label: List[List] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """forward

        Args:
            motifs (List[Tuple]): motifs
            label (List[List], optional): labels. Defaults to None.

        Returns:
            Tuple[torch.Tensor,torch.Tensor]: (loss, reward)
        """
        score = torch.sum(torch.prod(self.embedding_matrix[motifs], dim=1),
                          dim=1)
        p = torch.clip(1 - torch.exp(-score), 1e-5, 1)
        reward = 1 - p

        loss = (-torch.sum(label * p + (1 - label) *
                           (1 - p)) if label is not None else None)
        return loss, reward

    def get_reward(self,
                   motifs: List[Tuple],
                   label: List[List] = None) -> np.ndarray:
        """get reward

        Args:
            motifs (List[Tuple]): motifs.
            label (List[List], optional): labels. Defaults to None.

        Returns:
            np.ndarray: reward.
        """
        _, reward = self.forward(motifs, label)
        return reward.detach().numpy()

    def fit(self, sampling: Callable, id2motifs: List[List[Tuple]]) -> None:
        """fit

        Args:
            sampling (Callable): sampling funciton.
            id2motifs (List[List[Tuple]]): list of motifs indexed by node id.
        """
        motifs = []
        labels = []
        for epoch in range(self.n_epochs):
            self.train()
            if epoch % self.dis_interval == 0:
                motifs, labels = self.prepare_data_for_d(sampling, id2motifs)

            train_size = len(motifs)
            start_list = list(range(0, train_size, self.batch_size))
            np.random.shuffle(start_list)

            for start in start_list:
                self.zero_grad()
                end = start + self.batch_size
                loss, _ = self.forward(torch.LongTensor(motifs[start:end]),
                                       torch.Tensor(labels[start:end]))
                loss.backward()
                self.optimizer.step()
                self.embedding_matrix.data = torch.clip(
                    self.embedding_matrix.data, 0, self.max_value)
            print(f"discriminator epoch {epoch} loss {loss}")

    def get_embedding(self) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        return self.embedding_matrix.detach()
