"""
GCN Layer for SUBLIME model
"""
import dgl.function as fn
import torch
from torch import nn


class GCNConv_dgl(nn.Module):
    """GCN layer using dgl.

    Args:
        input_size (int): input size
        output_size (int): output size
    """

    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x, g):
        with g.local_scope():
            g.ndata["h"] = self.linear(x)
            g.update_all(fn.u_mul_e("h", "w", "m"), fn.sum(msg="m", out="h"))
            return g.ndata["h"]


class GCNConv_dense(nn.Module):
    """GCN layer dense.

    Args:
        input_size (int): input size
        output_size (int): output size
    """

    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def init_para(self):
        self.linear.reset_parameters()

    def forward(self, x, A, sparse=False):
        hidden = self.linear(x)
        if sparse:
            output = torch.sparse.mm(A, hidden)
        else:
            output = torch.matmul(A, hidden)
        return output
