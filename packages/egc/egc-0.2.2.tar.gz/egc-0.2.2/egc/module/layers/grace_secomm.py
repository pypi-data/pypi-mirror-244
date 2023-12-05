"""
GraceModel for SEComm
"""
# pylint:disable=W0223
import dgl
import torch
import torch.nn.functional as F
from dgl.nn.pytorch.conv import GraphConv
from torch import nn


class SECommEncoder(torch.nn.Module):
    """SECommEncoder, k层GCN"""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        activation,
        base_model=GraphConv,
        k: int = 2,
    ):
        super().__init__()
        self.base_model = base_model
        assert k >= 2
        self.k = k
        self.conv = [
            base_model(
                in_channels,
                2 * out_channels,
                activation=activation,
            )
        ]
        for _ in range(1, k - 1):
            self.conv.append(
                base_model(
                    2 * out_channels,
                    2 * out_channels,
                    activation=activation,
                ))

        self.conv.append(
            base_model(
                2 * out_channels,
                out_channels,
                activation=activation,
            ))
        self.conv = nn.ModuleList(self.conv)

    def forward(self, g: dgl.DGLGraph, feats: torch.Tensor):
        g = dgl.add_self_loop(g)
        for i in range(self.k):
            x = self.conv[i](g, feats)
            feats = x
        return x


class SECommGraceModel(torch.nn.Module):
    """GraceModel for SEComm"""

    def __init__(
        self,
        encoder: SECommEncoder,
        num_hidden: int,
        num_proj_hidden: int,
        tau: float = 0.5,
    ):
        super().__init__()
        self.encoder: SECommEncoder = encoder
        self.tau: float = tau

        self.fc1 = torch.nn.Linear(num_hidden, num_proj_hidden)
        self.fc2 = torch.nn.Linear(num_proj_hidden, num_hidden)

    def forward(self, g: dgl.DGLGraph, feats: torch.Tensor) -> torch.Tensor:
        return self.encoder(g, feats)

    def projection(self, z: torch.Tensor) -> torch.Tensor:
        z = F.elu(self.fc1(z))
        return self.fc2(z)

    # pylint:disable=R0201
    def sim(self, z1: torch.Tensor, z2: torch.Tensor):
        z1 = F.normalize(z1)
        z2 = F.normalize(z2)
        return torch.mm(z1, z2.t())

    def semi_loss(self, z1: torch.Tensor, z2: torch.Tensor):
        f = lambda x: torch.exp(x / self.tau)
        refl_sim = f(self.sim(z1, z1))
        between_sim = f(self.sim(z1, z2))

        return -torch.log(
            between_sim.diag() /
            (refl_sim.sum(1) + between_sim.sum(1) - refl_sim.diag()))

    def batched_semi_loss(
        self,
        z1: torch.Tensor,
        z2: torch.Tensor,
        batch_size: int,
    ):
        # Space complexity: O(BN) (semi_loss: O(N^2))
        device = z1.device
        num_nodes = z1.size(0)
        num_batches = (num_nodes - 1) // batch_size + 1
        f = lambda x: torch.exp(x / self.tau)
        indices = torch.arange(0, num_nodes).to(device)
        rand_indices = torch.randperm(num_nodes).to(device)
        losses = []

        # for i in range(num_batches):
        #    mask = indices[i * batch_size:(i + 1) * batch_size]
        #    refl_sim = f(self.sim(z1[mask], z1))  # [B, N]
        #    between_sim = f(self.sim(z1[mask], z2))  # [B, N]

        #    losses.append(-torch.log(
        #        between_sim[:, i * batch_size:(i + 1) * batch_size].diag()
        #        / (refl_sim.sum(1) + between_sim.sum(1)
        #           - refl_sim[:, i * batch_size:(i + 1) * batch_size].diag())))

        for i in range(num_batches):
            ordered_mask = indices[i * batch_size:(i + 1) * batch_size]
            random_mask = rand_indices[i * batch_size:(i + 1) * batch_size]
            refl_sim = f(self.sim(z1[ordered_mask], z1[random_mask]))  # [B, N]
            between_sim = f(self.sim(
                z1[ordered_mask],
                z2[random_mask],
            ))  # [B, N]

            # losses.append(-torch.log(
            #    f((F.normalize(z1[ordered_mask])*F.normalize(z2[ordered_mask])).sum(1))
            #    / (refl_sim.sum(1) + between_sim.sum(1))))
            losses.append(
                torch.log(refl_sim.sum(1) + between_sim.sum(1)) -
                (F.normalize(z1[ordered_mask]) *
                 F.normalize(z2[ordered_mask])).sum(1) / self.tau)

        return torch.cat(losses)

    def loss(
        self,
        z1: torch.Tensor,
        z2: torch.Tensor,
        mean: bool = True,
        batch_size: int = 0,
    ):
        h1 = self.projection(z1)
        h2 = self.projection(z2)

        if batch_size == 0:
            l1 = self.semi_loss(h1, h2)
            l2 = self.semi_loss(h2, h1)
        else:
            l1 = self.batched_semi_loss(h1, h2, batch_size)
            l2 = self.batched_semi_loss(h2, h1, batch_size)

        ret = (l1 + l2) * 0.5
        ret = ret.mean() if mean else ret.sum()

        return ret
