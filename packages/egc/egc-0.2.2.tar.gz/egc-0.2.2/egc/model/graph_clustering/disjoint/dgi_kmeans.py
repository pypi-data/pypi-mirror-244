"""DGI + Kmeans Graph Clustering
"""
from typing import List

import dgl
import torch

from ....utils import sk_clustering
from ...node_embedding import DGIEmbed
from ..base import Base


class DGIKmeans(Base):
    """DGI + Kmeans

    Args:
        in_feats (int): input feature dimension.
        out_feats_list (List[int]): List of hidden units dimensions.
        n_epochs (int, optional): number of embedding training epochs. Defaults to 10000.
        early_stopping_epoch (int, optional): early stopping threshold. Defaults to 20.
        batch_size (int, optional): batch size. Defaults to 1024.
        neighbor_sampler_fanouts (List[int] or int, optional): List of neighbors to sample
            for each GNN layer, with the i-th element being the fanout for the i-th GNN layer.
            Defaults to -1.

            - If only a single integer is provided, DGL assumes that every layer will
              have the same fanout.

            - If -1 is provided on one layer, then all inbound edges will be included.
        lr (float, optional): learning rate. Defaults to 0.001.
        l2_coef (float, optional): weight decay. Defaults to 0.0.
        activation (str): activation of gcn layer. Defaults to prelu.
        model_filename (str, optional): path to save best model parameters. Defaults to `dgi`.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_epochs: int = 10000,
        early_stopping_epoch: int = 20,
        batch_size: int = 1024,
        neighbor_sampler_fanouts: List[int] or int = -1,
        lr: float = 0.001,
        l2_coef: float = 0.0,
        activation: str = "prelu",
        model_filename: str = "dgi",
    ) -> None:
        super().__init__()
        self.n_clusters = None
        self.model = DGIEmbed(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            n_epochs=n_epochs,
            early_stopping_epoch=early_stopping_epoch,
            batch_size=batch_size,
            neighbor_sampler_fanouts=neighbor_sampler_fanouts,
            lr=lr,
            l2_coef=l2_coef,
            activation=activation,
            model_filename=model_filename,
        )

    def fit(
            self,
            graph: dgl.DGLGraph,
            n_clusters: int,
            device: torch.device = torch.device("cpu"),
    ):
        """Fit for Specific Graph

        Args:
            graph (dgl.DGLGraph): dgl graph.
            n_clusters (int): cluster num.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.n_clusters = n_clusters
        self.model.fit(
            graph=graph,
            device=device,
        )

    def get_embedding(
        self,
        graph: dgl.DGLGraph,
        device: torch.device = torch.device("cpu"),
        model_filename: str = None,
    ) -> torch.Tensor:
        """Get the embeddings.

        Args:
            graph (dgl.DGLGraph): dgl graph.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
            model_filename (str, optional): Model file to load. Defaults to None.

        Returns:
            torch.Tensor: Embeddings.
        """
        return self.model.get_embedding(graph, device, model_filename)

    def get_memberships(
        self,
        graph: dgl.DGLGraph,
        device: torch.device = torch.device("cpu"),
        model_filename: str = None,
    ) -> torch.Tensor:
        """Get the memberships.

        Args:
            graph (dgl.DGLGraph): dgl graph.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
            model_filename (str, optional): Model file to load. Defaults to None.

        Returns:
            torch.Tensor: Embeddings.
        """
        return sk_clustering(
            torch.squeeze(
                self.get_embedding(
                    graph,
                    device,
                    model_filename,
                ),
                0,
            ).cpu(),
            self.n_clusters,
            name="kmeans",
        )


# for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import set_device
#     from utils import set_seed
#     import scipy.sparse as sp
#     import time

#     set_seed(4096)
#     device = set_device('0')

#     graph, label, n_clusters = load_data(
#         dataset_name='Cora',
#         directory='./data',
#     )
#     features = graph.ndata["feat"]
#     adj_csr = graph.adj_external(scipy_fmt='csr')
#     edges = graph.edges()
#     features_lil = sp.lil_matrix(features)

#     start_time = time.time()
#     model = DGIKmeans(
#         in_feats=features.shape[1],
#         hidden_units=512,
#         model_filename='dgi_test',
#         n_epochs=1000,
#     )
#     model.fit(graph=graph, n_clusters=n_clusters, device=device)
#     res = model.get_memberships()
#     elapsed_time = time.time() - start_time
#     (
#         ARI_score,
#         NMI_score,
#         ACC_score,
#         Micro_F1_score,
#         Macro_F1_score,
#     ) = evaluation(label, res)
#     print("\n"
#           f"Elapsed Time:{elapsed_time:.2f}s\n"
#           f"ARI:{ARI_score}\n"
#           f"NMI:{ NMI_score}\n"
#           f"ACC:{ACC_score}\n"
#           f"Micro F1:{Micro_F1_score}\n"
#           f"Macro F1:{Macro_F1_score}\n")
