"""
GCN Layer
Adapted from: https://github.com/PetarV-/DGI
"""
from typing import Tuple

import torch
from torch import nn

from ...utils import init_weights


class GCN(nn.Module):
    """GCN Layer

    Args:
        in_feats (int): input feature dimension
        out_feats (int): output feature dimension
        activation (str): activation function. Defaults to prelu.
        bias (bool): whether to apply bias after calculate \\hat{A}XW. Defaults to True.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats: int,
        activation: str = "prelu",
        bias: bool = True,
    ) -> None:
        super().__init__()
        self.f_c = nn.Linear(in_feats, out_feats, bias=False)

        if activation == "prelu":
            self.activation = nn.PReLU()
        elif activation == "relu":
            self.activation = nn.ReLU()
        else:
            self.activation = activation

        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_feats))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter("bias", None)

        for module in self.modules():
            init_weights(module)

    def forward(self,
                features: torch.Tensor,
                adj_norm: torch.Tensor,
                sparse: bool = True) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward Propagation

        Args:
            features (torch.Tensor):
                normalized 3D features tensor in shape of torch.Size([1, xx, xx])
            adj_norm (torch.Tensor): symmetrically normalized 2D adjacency tensor
            sparse (bool): whether input sparse tensor

        Returns:
            out, hidden_layer (torch.Tensor, torch.Tensor): \\hat{A}XW and XW
        """
        hidden_layer = self.f_c(features)

        if sparse:
            out = torch.unsqueeze(
                torch.spmm(adj_norm, torch.squeeze(hidden_layer, 0)), 0)
        else:
            out = torch.unsqueeze(
                torch.bmm(adj_norm, torch.squeeze(hidden_layer, 0)), 0)

        if self.bias is not None:
            out = out + self.bias

        return self.activation(out), hidden_layer
