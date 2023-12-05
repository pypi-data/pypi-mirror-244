"""
Self-Expressive module for SEComm
"""
import torch
from torch.nn.modules.module import Module
from torch.nn.parameter import Parameter


class SECommSelfExpr(Module):
    """
    Self-Expressive module for SEComm
    """

    def __init__(self, n):
        super().__init__()
        self.n = n
        self.weight = Parameter(torch.FloatTensor(n, n).uniform_(0, 0.01))

    def forward(self, x):
        # self.weight.data = F.relu(self.weight)
        output = torch.mm(
            self.weight - torch.diag(torch.diagonal(self.weight)), x)
        return self.weight, output

    def reset(self):
        self.weight.data = torch.FloatTensor(self.n, self.n).uniform_(0, 0.01)
