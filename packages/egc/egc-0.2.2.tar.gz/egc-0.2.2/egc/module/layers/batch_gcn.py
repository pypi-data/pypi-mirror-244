"""
GCN Layer
Adapted from: https://github.com/PetarV-/DGI
"""
import torch
from torch import nn

from ...utils import init_weights


# Borrowed from https://github.com/PetarV-/DGI
class BATCH_GCN(nn.Module):
    """GCN Layer

    Args:
        in_ft (int): input feature dimension
        out_ft (int): output feature dimension
        bias (bool): whether to apply bias after calculate \\hat{A}XW. Defaults to True.
    """

    def __init__(self, in_ft, out_ft, bias=True):
        super().__init__()
        self.fc = nn.Linear(in_ft, out_ft, bias=False)
        self.act = nn.PReLU()

        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter("bias", None)

        for m in self.modules():
            init_weights(m)

    # Shape of seq: (batch, nodes, features)
    def forward(self, seq, adj, sparse=False):
        """Forward Propagation

        Args:
            seq (torch.Tensor):
                normalized 3D features tensor. Shape of seq: (batch, nodes, features)
            adj (torch.Tensor): symmetrically normalized 2D adjacency tensor
            sparse (bool): whether input sparse tensor

        Returns:
            out (torch.Tensor): \\hat{A}XW
        """
        seq_fts = self.fc(seq)
        if sparse:
            out = torch.unsqueeze(torch.spmm(adj, torch.squeeze(seq_fts, 0)),
                                  0)
        else:
            out = torch.bmm(adj, seq_fts)
        if self.bias is not None:
            out += self.bias
        return self.act(out)
