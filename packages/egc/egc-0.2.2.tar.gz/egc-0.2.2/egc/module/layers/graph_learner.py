"""
Graph Learners for SUBLIME model
"""
import dgl
import torch
import torch.nn.functional as F
from torch import nn

from ...utils.sublime_utils import apply_non_linearity
from ...utils.sublime_utils import cal_similarity_graph
from ...utils.sublime_utils import knn_fast
from ...utils.sublime_utils import nearest_neighbors_pre_elu
from ...utils.sublime_utils import top_k
from .gcn_sublime import GCNConv_dgl

# pylint: disable=no-else-return


class FGP_learner(nn.Module):
    """FGP learner

    Args:
        features (torch.Tensor): node features
        k (int): _description_
        knn_metric (str): The distance metric used to calculate
                            the k-Neighbors for each sample point.
        i (int): _description_
        sparse (int): If sparse mode
    """

    def __init__(self, features, k, knn_metric, i, sparse):
        super().__init__()

        self.k = k
        self.knn_metric = knn_metric
        self.i = i
        self.sparse = sparse

        self.Adj = nn.Parameter(
            torch.from_numpy(
                nearest_neighbors_pre_elu(features, self.k, self.knn_metric,
                                          self.i)))

    # pylint: disable=unused-argument
    def forward(self, h):
        if not self.sparse:
            Adj = F.elu(self.Adj) + 1
        else:
            Adj = self.Adj.coalesce()
            Adj.values = F.elu(Adj.values()) + 1
        return Adj


class Attentive(nn.Module):
    """Attentive"""

    def __init__(self, isize):
        super().__init__()
        self.w = nn.Parameter(torch.ones(isize))

    def forward(self, x):
        return x @ torch.diag(self.w)


class ATT_learner(nn.Module):
    """ATT learner"""

    def __init__(self, nlayers, isize, k, knn_metric, i, sparse, mlp_act):
        super().__init__()

        self.i = i
        self.layers = nn.ModuleList()
        for _ in range(nlayers):
            self.layers.append(Attentive(isize))
        self.k = k
        self.knn_metric = knn_metric
        self.non_linearity = "relu"
        self.sparse = sparse
        self.mlp_act = mlp_act

    def internal_forward(self, h):
        for i, layer in enumerate(self.layers):
            h = layer(h)
            if i != (len(self.layers) - 1):
                if self.mlp_act == "relu":
                    h = F.relu(h)
                elif self.mlp_act == "tanh":
                    h = F.tanh(h)
        return h

    def forward(self, features):
        if self.sparse:
            embeddings = self.internal_forward(features)
            rows, cols, values = knn_fast(embeddings, self.k, 1000)
            rows_ = torch.cat((rows, cols))
            cols_ = torch.cat((cols, rows))
            values_ = torch.cat((values, values))
            values_ = apply_non_linearity(values_, self.non_linearity, self.i)
            adj = dgl.graph((rows_, cols_),
                            num_nodes=features.shape[0],
                            device="cuda")
            adj.edata["w"] = values_
            return adj
        else:
            embeddings = self.internal_forward(features)
            embeddings = F.normalize(embeddings, dim=1, p=2)
            similarities = cal_similarity_graph(embeddings)
            similarities = top_k(similarities, self.k + 1)
            similarities = apply_non_linearity(similarities,
                                               self.non_linearity, self.i)
            return similarities


class MLP_learner(nn.Module):
    """MLP learner"""

    def __init__(self, nlayers, isize, k, knn_metric, i, sparse, act):
        super().__init__()

        self.layers = nn.ModuleList()
        if nlayers == 1:
            self.layers.append(nn.Linear(isize, isize))
        else:
            self.layers.append(nn.Linear(isize, isize))
            for _ in range(nlayers - 2):
                self.layers.append(nn.Linear(isize, isize))
            self.layers.append(nn.Linear(isize, isize))

        self.input_dim = isize
        self.output_dim = isize
        self.k = k
        self.knn_metric = knn_metric
        self.non_linearity = "relu"
        self.param_init()
        self.i = i
        self.sparse = sparse
        self.act = act

    def internal_forward(self, h):
        for i, layer in enumerate(self.layers):
            h = layer(h)
            if i != (len(self.layers) - 1):
                if self.act == "relu":
                    h = F.relu(h)
                elif self.act == "tanh":
                    h = F.tanh(h)
        return h

    def param_init(self):
        for layer in self.layers:
            layer.weight = nn.Parameter(torch.eye(self.input_dim))

    def forward(self, features):
        if self.sparse:
            embeddings = self.internal_forward(features)
            rows, cols, values = knn_fast(embeddings, self.k, 1000)
            rows_ = torch.cat((rows, cols))
            cols_ = torch.cat((cols, rows))
            values_ = torch.cat((values, values))
            values_ = apply_non_linearity(values_, self.non_linearity, self.i)
            adj = dgl.graph((rows_, cols_),
                            num_nodes=features.shape[0],
                            device="cuda")
            adj.edata["w"] = values_
            return adj
        else:
            embeddings = self.internal_forward(features)
            embeddings = F.normalize(embeddings, dim=1, p=2)
            similarities = cal_similarity_graph(embeddings)
            similarities = top_k(similarities, self.k + 1)
            similarities = apply_non_linearity(similarities,
                                               self.non_linearity, self.i)
            return similarities


class GNN_learner(nn.Module):
    """GNN learner"""

    def __init__(self, nlayers, isize, k, knn_metric, i, sparse, mlp_act, adj):
        super().__init__()

        self.adj = adj
        self.layers = nn.ModuleList()
        if nlayers == 1:
            self.layers.append(GCNConv_dgl(isize, isize))
        else:
            self.layers.append(GCNConv_dgl(isize, isize))
            for _ in range(nlayers - 2):
                self.layers.append(GCNConv_dgl(isize, isize))
            self.layers.append(GCNConv_dgl(isize, isize))

        self.input_dim = isize
        self.output_dim = isize
        self.k = k
        self.knn_metric = knn_metric
        self.non_linearity = "relu"
        self.param_init()
        self.i = i
        self.sparse = sparse
        self.mlp_act = mlp_act

    def internal_forward(self, h):
        for i, layer in enumerate(self.layers):
            h = layer(h, self.adj)
            if i != (len(self.layers) - 1):
                if self.mlp_act == "relu":
                    h = F.relu(h)
                elif self.mlp_act == "tanh":
                    h = F.tanh(h)
        return h

    def param_init(self):
        for layer in self.layers:
            layer.weight = nn.Parameter(torch.eye(self.input_dim))

    def forward(self, features):
        if self.sparse:
            embeddings = self.internal_forward(features)
            rows, cols, values = knn_fast(embeddings, self.k, 1000)
            rows_ = torch.cat((rows, cols))
            cols_ = torch.cat((cols, rows))
            values_ = torch.cat((values, values))
            values_ = apply_non_linearity(values_, self.non_linearity, self.i)
            adj = dgl.graph((rows_, cols_),
                            num_nodes=features.shape[0],
                            device="cuda")
            adj.edata["w"] = values_
            return adj
        else:
            embeddings = self.internal_forward(features)
            embeddings = F.normalize(embeddings, dim=1, p=2)
            similarities = cal_similarity_graph(embeddings)
            similarities = top_k(similarities, self.k + 1)
            similarities = apply_non_linearity(similarities,
                                               self.non_linearity, self.i)
            return similarities
