"""ClusterNet
Paper: https://proceedings.neurips.cc/paper/2019/file/8bd39eae38511daad6152e84545e504d-Paper.pdf
Source Code: https://github.com/bwilder0/clusternet
"""
from typing import List
from typing import Tuple

import dgl
import numpy as np
import torch
from torch import nn

from ....module import MultiLayerGNN
from ....utils import get_modularity_matrix
from ....utils import get_modularity_value
from ....utils import init_weights
from ....utils import load_model
from ....utils import NaiveDataLoader
from ....utils import save_model
from ....utils import soft_kmeans_clustering

# pylint:disable=self-cls-assignment


class ClusterNet(nn.Module):
    """GCN ClusterNet.
    The ClusterNet architecture. The first step is a 2-layer GCN to generate embeddings.
    The output is the cluster means mu and soft assignments r, along with the
    embeddings and the the node similarities (just output for debugging purposes).

    The forward pass inputs are x, a feature matrix for the nodes, and adj, a sparse
    adjacency matrix. The optional parameter num_iter determines how many steps to
    run the k-means updates for.

    Args:
        in_feats (int): Input feature size.
        out_feats_list (List[int]): List of hidden units dimensions.
        n_clusters (int): Num of clusters.
        cluster_temp (float, optional): softmax temperature. Defaults to 30.
        aggregator_type (str, optional): Aggregator type to use \
            (``mean``, ``gcn``, ``pool``, ``lstm``). Defaults to 'gcn'.
        bias (bool, optional): If True, adds a learnable bias to the output. Defaults to True.
        dropout (float, optional): Percentage for dropping in GCN. Defaults to 0.5.
        n_epochs (int, optional): Maximum training epochs. Defaults to 1000.
        lr (float, optional): Learning Rate. Defaults to 0.01.
        l2_coef (float, optional): Weight decay. Defaults to 0.5.
        early_stopping_epoch (int, optional): Early stopping threshold. Defaults to 20.
        model_filename (str, optional): Path to store model parameters. Defaults to 'clusternet'.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_clusters: int,
        cluster_temp: float = 30,
        aggregator_type: str = "gcn",
        bias: bool = True,
        dropout: float = 0.5,
        n_epochs: int = 1000,
        lr: float = 0.01,
        l2_coef: float = 1e-5,
        early_stopping_epoch: int = 20,
        model_filename: str = "clusternet",
    ):
        super().__init__()

        self.n_layers = len(out_feats_list)
        self.n_clusters = n_clusters
        self.cluster_temp = cluster_temp
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.encoder = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=[*out_feats_list],
            aggregator_type=aggregator_type,
            bias=bias,
            dropout=dropout,
            activation=["relu"] * (len(out_feats_list) - 1) + ["none"],
        )
        self.init = nn.Parameter(
            torch.rand(self.n_clusters, out_feats_list[-1]),
            requires_grad=True,
        )
        nn.init.xavier_uniform_(self.init.data)

        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def forward(self, blocks) -> Tuple[torch.Tensor]:
        input_feat = blocks[0].srcdata["feat"]
        x_en = self.encoder(blocks, input_feat)
        return x_en

    def fit(
            self,
            graph: dgl.DGLGraph,
            num_iter: int = 10,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        """fit

        Args:
            graph (dgl.DGLGraph): graph.
            num_iter (int, optional): clustering iteration. Defaults to 10.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.to(device)
        g = graph.to(device)
        adj_csr = g.adj_external(scipy_fmt="csr")
        adj_nodia = torch.FloatTensor(
            adj_csr.todense() - np.diag(np.diag(adj_csr.todense()))).to(device)

        data_loader = NaiveDataLoader(
            graph=g,
            aug_types=["none"],
            batch_size=g.num_nodes(),
            n_layers=self.n_layers,
            device=device,
            drop_last=True,
        )

        cnt_wait = 0
        best = 1e9
        for epoch in range(self.n_epochs):
            self.train()

            loss_epoch = 0
            for _, [(_, _, block)] in enumerate(data_loader):
                self.optimizer.zero_grad()
                x_en = self.forward(block)

                _, r, _ = soft_kmeans_clustering(
                    data=x_en,
                    num_iter=num_iter,
                    miu=self.init,
                    cluster_temp=self.cluster_temp,
                    dist_type="cosine_similarity",
                )
                loss = -get_modularity_value(
                    adj_nodia,
                    r,
                    get_modularity_matrix(adj_nodia),
                )

                loss.backward()
                self.optimizer.step()
                loss_epoch += loss.item()

            # increase iterations after 100 updates to fine-tune
            # if epoch % 100 == 0:
            #     num_iter += 5

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

            print(
                f"Epoch: {epoch+1:04d}\tEpoch Loss:{loss_epoch / len(data_loader) :.8f}"
            )

    def get_embedding(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        g = graph.to(device)
        sampler = dgl.dataloading.MultiLayerFullNeighborSampler(self.n_layers)
        data_loader = dgl.dataloading.DataLoader(
            g,
            g.nodes(),
            sampler,
            batch_size=g.num_nodes(),
            shuffle=False,
            drop_last=False,
            num_workers=4 if device == torch.device("cpu") else 0,
            device=device,
        )
        embedding = []
        self.to(device)
        for _, (_, _, block) in enumerate(data_loader):
            with torch.no_grad():
                h = self.forward(block)
                h = h.cpu().detach().numpy()
            embedding.extend(h)
        return torch.Tensor(embedding)

    def get_memberships(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> torch.Tensor:
        """Get the memberships.

        Args:
            graph (dgl.DGLGraph): dgl graph.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
            model_filename (str, optional): Model file to load. Defaults to None.

        Returns:
            torch.Tensor: Embeddings.
        """
        self, _, _, _ = load_model(self.model_filename, self, self.optimizer)
        x_en = self.get_embedding(
            graph,
            device,
        )
        _, r, _ = soft_kmeans_clustering(
            data=x_en.to(device),
            num_iter=1,
            miu=self.init,
            cluster_temp=self.cluster_temp,
            dist_type="cosine_similarity",
        )
        return r.argmax(dim=1).cpu().numpy()


# if __name__ == '__main__':
#     from utils import load_data
#     from utils import set_device
#     import torch
#     from utils import set_seed
#     set_seed(4096)
#     device = set_device('5')
#     graph, label, n_clusters = load_data(
#         dataset_name='Cora',
#         directory='./data',
#     )
#     features = graph.ndata["feat"]
#     # features = sp.lil_matrix(features)
#     # features = normalize_feature(features)
#     # features = torch.FloatTensor(features)
#     # features[features != 0] = 1
#     # graph.apply_nodes(lambda nodes: {'feat': features})
#     model = ClusterNet(
#         in_feats=features.shape[1],
#         out_feats_list=[50, 10],
#         n_clusters=n_clusters,
#         n_epochs=1001,
#         early_stopping_epoch=50,
#     )
#     model.fit(graph=graph, device=device)

#     res = model.get_memberships(graph, device)
#     from utils.evaluation import evaluation
#     (
#         ARI_score,
#         NMI_score,
#         ACC_score,
#         Micro_F1_score,
#         Macro_F1_score,
#     ) = evaluation(label, res)
#     print("\nclusternet\n"
#           f"ARI:{ARI_score}\n"
#           f"NMI:{ NMI_score}\n"
#           f"ACC:{ACC_score}\n"
#           f"Micro F1:{Micro_F1_score}\n"
#           f"Macro F1:{Macro_F1_score}\n")
