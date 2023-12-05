"""
Discriminator Layer
Adapted from: https://github.com/PetarV-/DGI
"""
import torch
from torch import nn

from ...utils import init_weights


# pylint:disable=no-self-use
class DiscMVGRL(nn.Module):
    """Discriminator for MVGRL and GDCL

    Args:
        n_h (int): hidden units dimension. Defaults to 512.
    """

    def __init__(self, n_h):
        super().__init__()
        self.f_k = nn.Bilinear(n_h, n_h, 1)

        for m in self.modules():
            init_weights(m)

    def forward(self, c1, c2, h1, h2, h3, h4):
        """Forward Propagation

        Args:
            c1 (torch.Tensor): readout of raw graph by Readout function
            c2 (torch.Tensor): readout of diffuse graph by Readout function
            h1 (torch.Tensor): node embedding of raw graph by one gcn layer
            h2 (torch.Tensor): node embedding of diffuse graph by one gcn layer
            h3 (torch.Tensor): node embedding of raw graph and shuffle features by one gcn layer
            h4 (torch.Tensor): node embedding of diffuse graph and shuffle features by one gcn layer

        Returns:
            logits (torch.Tensor): probability of positive or negtive node
        """
        c_x1 = torch.unsqueeze(c1, 1)
        c_x1 = c_x1.expand_as(h1).contiguous()
        c_x2 = torch.unsqueeze(c2, 1)
        c_x2 = c_x2.expand_as(h2).contiguous()

        # positive
        sc_1 = torch.squeeze(self.f_k(h2, c_x1), 2)
        sc_2 = torch.squeeze(self.f_k(h1, c_x2), 2)

        # negetive
        sc_3 = torch.squeeze(self.f_k(h4, c_x1), 2)
        sc_4 = torch.squeeze(self.f_k(h3, c_x2), 2)

        logits = torch.cat((sc_1, sc_2, sc_3, sc_4), 1)
        return logits
