"""
Discriminator Layer
Adapted from: https://github.com/PetarV-/DGI
"""
import torch
from torch import nn

from ...utils import init_weights


class DiscDGI(nn.Module):
    """Discriminator for DGI

    Args:
        hidden_units (int): hidden units dimension. Defaults to 512.
        bias (bool): whether to apply bias to xWy. Defaults to False.
    """

    def __init__(self, hidden_units: int = 512, bias: bool = True) -> None:
        super().__init__()
        self.f_k = nn.Bilinear(hidden_units, hidden_units, 1, bias)

        for module in self.modules():
            init_weights(module)

    def forward(
        self,
        g: torch.Tensor,
        h: torch.Tensor,
        h_shf: torch.Tensor,
    ) -> torch.Tensor:
        """Forward Propagation

        Args:
            g (torch.Tensor): avg readout of whole graph, 1D tensor.
            h (torch.Tensor): node embedding. 3D tensor.
            h_shf (torch.Tensor): shuffled node embedding as \
                corrupted graph node embedding. 3D tensor.

        Returns:
            (torch.Tensor): concat of pos and neg disc output.
        """
        g_x = g if g.shape == h.shape else torch.unsqueeze(g, 1).expand_as(h)

        s_c_pos = torch.squeeze(self.f_k(h, g_x), 2)
        s_c_neg = torch.squeeze(self.f_k(h_shf, g_x), 2)

        return torch.cat((s_c_pos, s_c_neg), 1)
