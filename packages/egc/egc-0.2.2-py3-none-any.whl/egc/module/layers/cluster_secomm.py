"""
ClusterModel for SEComm
"""
import torch
import torch.nn.functional as F


# pylint:disable=abstract-method
class SECommClusterModel(torch.nn.Module):
    """ClusterModel for SEComm"""

    def __init__(self, n_hid1, n_hid2, n_class, dropout):
        super().__init__()
        self.mlp1 = torch.nn.Linear(n_hid1, n_hid2)
        self.mlp2 = torch.nn.Linear(n_hid2, n_class)
        self.dropout = dropout
        # ~ torch.nn.init.xavier_uniform_(self.mlp1.weight)
        # ~ torch.nn.init.xavier_uniform_(self.mlp2.weight)

    def forward(self, x1: torch.Tensor) -> torch.Tensor:
        x2 = F.relu(self.mlp1(x1))
        if self.dropout > 0:
            x2 = F.dropout(x2, self.dropout, training=self.training)
        z = F.softmax(self.mlp2(x2), dim=-1)
        # z = F.relu(self.fc4(x3))
        return z
