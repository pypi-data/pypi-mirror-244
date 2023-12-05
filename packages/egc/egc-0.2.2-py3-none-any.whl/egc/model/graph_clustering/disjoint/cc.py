"""Contrastive Clustering

- Adapted from https://github.com/Yunfan-Li/Contrastive-Clustering
"""
from typing import List

import dgl
import numpy as np
import scipy.sparse as sp
import torch
from torch import nn
from torch.nn.functional import normalize
from tqdm import tqdm

from ....module import ClusterLoss
from ....module import InstanceLoss
from ....module import MultiLayerGNN
from ....utils import init_weights
from ....utils import load_model
from ....utils import NaiveDataLoader
from ....utils import normalize_feature
from ....utils import save_model
from ..base import Base

# pylint:disable=self-cls-assignment


class ContrastiveClustering(Base, nn.Module):
    """ContrastiveClustering

    Args:
        in_feats (int): Input feature size.
        out_feats_list (List[int]): List of hidden units dimensions.
        n_clusters (int): Num of clusters.
        aggregator_type (str, optional): Aggregator type to use \
            (``mean``, ``gcn``, ``pool``, ``lstm``). Defaults to 'gcn'.
        bias (bool, optional): If True, adds a learnable bias to the output. Defaults to True.
        batch_size (int, optional): Batch size. Defaults to 1024.
        instance_temperature (float, optional): Instance Contrastive Head temperature. \
            Defaults to 0.5.
        cluster_temperature (float, optional): Cluster Contrastive Head temperature. \
            Defaults to 1.0.
        aug_types (List, optional): Augmentation types list. Defaults to ['edge', 'edge'].
        n_epochs (int, optional): Maximum training epochs. Defaults to 1000.
        lr (float, optional): Learning Rate. Defaults to 0.001.
        l2_coef (float, optional): Weight decay. Defaults to 0.0.
        early_stopping_epoch (int, optional): Early stopping threshold. Defaults to 20.
        model_filename (str, optional): Path to store model parameters. Defaults to 'cc'.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_clusters: int,
        aggregator_type: str = "gcn",
        bias: bool = True,
        batch_size: int = 1024,
        instance_temperature: float = 0.5,
        cluster_temperature: float = 1.0,
        aug_types: List = None,
        n_epochs: int = 1000,
        lr: float = 0.001,
        l2_coef: float = 0.0,
        early_stopping_epoch: int = 20,
        model_filename: str = "cc",
    ):
        super().__init__()
        nn.Module.__init__(self)
        self.batch_size = batch_size
        self.aug_types = aug_types if aug_types is not None else [
            "random_mask", "random_mask"
        ]
        self.n_clusters = n_clusters
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.sage = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            aggregator_type=aggregator_type,
            bias=bias,
        )
        self.n_layers = len(out_feats_list)
        self.instance_projector = nn.Sequential(
            nn.Linear(out_feats_list[-1], out_feats_list[-1]),
            nn.ReLU(),
            nn.Linear(out_feats_list[-1], out_feats_list[-1] // 4),
        )
        self.cluster_projector = nn.Sequential(
            nn.Linear(out_feats_list[-1], out_feats_list[-1]),
            nn.ReLU(),
            nn.Linear(out_feats_list[-1], n_clusters),
            nn.Softmax(dim=1),
        )
        self.instance_loss = InstanceLoss(batch_size, instance_temperature)
        self.cluster_loss = ClusterLoss(n_clusters, cluster_temperature)
        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def forward(self, blocks_i, blocks_j):
        input_feat_i = blocks_i[0].srcdata["feat"]
        input_feat_j = blocks_j[0].srcdata["feat"]
        h_i = self.sage(blocks_i, input_feat_i)
        h_j = self.sage(blocks_j, input_feat_j)

        z_i = normalize(self.instance_projector(h_i), dim=1)
        z_j = normalize(self.instance_projector(h_j), dim=1)

        c_i = self.cluster_projector(h_i)
        c_j = self.cluster_projector(h_j)

        return z_i, z_j, c_i, c_j

    def forward_cluster(self, blocks):
        h = self.sage(blocks, blocks[0].srcdata["feat"])
        c = self.cluster_projector(h)
        return torch.argmax(c, dim=1)

    def forward_instance(self, blocks):
        return self.sage(blocks, blocks[0].srcdata["feat"])

    def fit(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        """fit

        Args:
            graph (dgl.DGLGraph): graph.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        graph.apply_nodes(
            lambda nodes: {
                "feat":
                torch.FloatTensor(
                    normalize_feature(sp.lil_matrix(nodes.data["feat"])))
            })
        self.to(device)

        data_loader = NaiveDataLoader(
            graph=graph,
            batch_size=self.batch_size,
            n_layers=self.n_layers,
            aug_types=self.aug_types,
            device=device,
            drop_last=True,
        )

        cnt_wait = 0
        best = 1e9
        for epoch in range(self.n_epochs):
            self.train()

            loss_epoch = 0
            for step, (
                (_, _, blocks_i),
                (_, _, blocks_j),
            ) in enumerate(data_loader):
                self.optimizer.zero_grad()

                z_i, z_j, c_i, c_j = self.forward(blocks_i, blocks_j)

                instance_loss = self.instance_loss(z_i, z_j)
                cluster_loss = self.cluster_loss(c_i, c_j)
                loss = instance_loss + cluster_loss

                if step % 50 == 0:
                    print(f"Step:{step+1:04d}\tLoss:{loss:.8f}\t"
                          f"Instance Loss:{instance_loss:.8f}\t"
                          f"Cluster Loss:{cluster_loss:.8f}")

                loss.backward()
                self.optimizer.step()
                loss_epoch += loss.item()

            print(
                f"Epoch: {epoch+1:04d}\tEpoch Loss:{loss_epoch / len(data_loader) :.8f}"
            )

            if round(loss_epoch, 5) < best:
                best = loss_epoch
                cnt_wait = 0
                save_model(
                    self.model_filename,
                    self,
                    self.optimizer,
                    epoch,
                    loss_epoch,
                )
            else:
                cnt_wait += 1

            if cnt_wait == self.early_stopping_epoch:
                print("Early stopping!")
                break

    def get_embedding(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        self, _, _, _ = load_model(self.model_filename, self, self.optimizer)

        graph.apply_nodes(
            lambda nodes: {
                "feat":
                torch.FloatTensor(
                    normalize_feature(sp.lil_matrix(nodes.data["feat"])))
            })
        self.to(device)

        sampler = dgl.dataloading.MultiLayerFullNeighborSampler(self.n_layers)
        data_loader = dgl.dataloading.DataLoader(
            graph,
            graph.nodes(),
            sampler,
            batch_size=self.batch_size,
            shuffle=False,
            drop_last=False,
            num_workers=4 if device == torch.device("cpu") else 0,
            device=device,
        )
        embedding = []
        for _, (_, _, block) in tqdm(
                enumerate(data_loader),
                desc="Inference:",
                total=len(data_loader),
        ):
            with torch.no_grad():
                h = self.forward_instance(block).cpu().detach()
            embedding.extend(h)
        return torch.Tensor(embedding)

    def get_memberships(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> np.ndarray:
        """Get memberships

        Returns:
            np.ndarray: memberships
        """
        self, _, _, _ = load_model(self.model_filename, self, self.optimizer)
        graph.apply_nodes(
            lambda nodes: {
                "feat":
                torch.FloatTensor(
                    normalize_feature(sp.lil_matrix(nodes.data["feat"])))
            })
        sampler = dgl.dataloading.MultiLayerFullNeighborSampler(self.n_layers)
        data_loader = dgl.dataloading.DataLoader(
            graph,
            graph.nodes(),
            sampler,
            batch_size=self.batch_size,
            shuffle=False,
            drop_last=False,
            num_workers=4 if device == torch.device("cpu") else 0,
            device=device,
        )
        clusters = []
        self.to(device)
        for _, (_, _, block) in tqdm(
                enumerate(data_loader),
                desc="Inference:",
                total=len(data_loader),
        ):
            with torch.no_grad():
                c = self.forward_cluster(block).cpu().detach().numpy()
            clusters.extend(c)
        return np.array(clusters).flatten()


# # for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import set_device
#     from utils import set_seed

#     import scipy.sparse as sp
#     import time

#     set_seed(4096)
#     device = set_device('2')

#     graph, label, n_clusters = load_data(
#         dataset_name='Cora',
#         directory='./data',
#     )
#     features = graph.ndata["feat"]
#     adj_csr = graph.adj_external(scipy_fmt='csr')
#     edges = graph.edges()
#     features_lil = sp.lil_matrix(features)

#     start_time = time.time()
#     model = ContrastiveClustering(
#         in_feats=features.shape[1],
#         out_feats_list=[512],
#         n_clusters=n_clusters,
#         aggregator_type='gcn',
#         bias=True,
#         batch_size=1024,
#         instance_temperature=1.0,
#         cluster_temperature=0.5,
#         aug_types=[RandomMask(p=0.3), RandomMask(p=0.4)],
#         n_epochs=1000,
#         lr=0.001,
#         l2_coef=0.0,
#         early_stopping_epoch=20,
#         model_filename='cc_test',
#     )
#     model.fit(graph=graph, device=device)
#     res = model.get_memberships(graph, device)
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
