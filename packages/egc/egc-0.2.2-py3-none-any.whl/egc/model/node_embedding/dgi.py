"""Embedding By DGI

Adapted from: https://github.com/PetarV-/DGI
"""
import copy
from typing import List

import dgl
import numpy as np
import scipy.sparse as sp
import torch
from torch import nn
from tqdm import tqdm

from ...module import DiscDGI
from ...module import MultiLayerGNN
from ...utils import init_weights
from ...utils import load_model
from ...utils import NaiveDataLoader
from ...utils import normalize_feature
from ...utils import save_model

# pylint:disable=self-cls-assignment


def avg_readout(h: torch.Tensor, mask: torch.Tensor = None):
    """Average readout of whole graph

    Args:
        h (torch.Tensor): embeddings of all nodes in graph.
        mask (torch.Tensor, optional): node mask. Defaults to None.

    Returns:
        (torch.Tensor): Average readout of whole graph.
    """
    if mask is None:
        return torch.mean(h, 1)
    mask = torch.unsqueeze(mask, -1)
    return torch.sum(h * mask, 1) / torch.sum(mask)


class DGIEmbed(nn.Module):
    """DGI Embedding

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
        activation (str, optional): activation of gcn layer. Defaults to prelu.
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
    ):
        super().__init__()
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.n_layers = len(out_feats_list)
        self.out_feats_list = out_feats_list
        self.neighbor_sampler_fanouts = neighbor_sampler_fanouts
        self.device = torch.device("cpu")

        self.encoder = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            activation=[activation] * len(out_feats_list),
            bias=True,
            aggregator_type="gcn",
        )
        self.disc = DiscDGI(out_feats_list[-1], out_feats_list[-1])
        self.sigmoid = nn.Sigmoid()

        self.calc_loss = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def forward(
        self,
        block,
        input_feats,
    ) -> torch.Tensor:
        h = self.encoder(block, input_feats)
        return h

    def fit(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        """Fit for Specific Graph

        Args:
            graph (dgl.DGLGraph): dgl graph.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.device = device
        graph.apply_nodes(
            lambda nodes: {
                "feat":
                torch.FloatTensor(
                    normalize_feature(sp.lil_matrix(nodes.data["feat"])))
            })

        train_loader = NaiveDataLoader(
            graph=graph,
            batch_size=self.batch_size,
            fanouts=self.neighbor_sampler_fanouts,
            n_layers=self.n_layers,
            aug_types=["none"],
            device=device,
            drop_last=True,
        )
        lbl = torch.cat(
            (
                torch.ones(1, self.batch_size),
                torch.zeros(1, self.batch_size),
            ),
            1,
        ).to(device)

        self.to(device)

        cnt_wait = 0
        best = 1e9
        g_avg = None
        for epoch in range(self.n_epochs + 1):
            self.train()
            loss_epoch = 0
            g_avg_iter = torch.zeros((1, self.out_feats_list[-1])).to(device)

            train_loader_iter = iter(train_loader)
            if g_avg is None:
                with torch.no_grad():
                    for _, [(_, _, blocks)] in tqdm(
                            enumerate(train_loader),
                            desc="Initialize the average graph embedding: ",
                            total=len(train_loader),
                    ):
                        input_feats = blocks[0].srcdata["feat"]
                        h = self.forward(blocks, input_feats)
                        g_avg_iter = g_avg_iter + h
                # NOTE: intermediate results should be detached,
                # otherwise loss calculated by it will not be able to backward propagate
                # in the second iteration as intermediate results will be deleted
                g_avg = self.sigmoid(
                    g_avg_iter.unsqueeze(0) /
                    (self.batch_size * len(train_loader))).detach()
                continue

            g_shf = copy.deepcopy(graph)
            g_shf.apply_nodes(
                lambda nodes: {
                    "feat":
                    nodes.data["feat"][np.random.permutation(
                        list(range(nodes.data["feat"].shape[0])))]
                })
            shf_loader = NaiveDataLoader(
                graph=g_shf,
                batch_size=self.batch_size,
                fanouts=self.neighbor_sampler_fanouts,
                n_layers=self.n_layers,
                aug_types=["none"],
                device=device,
                drop_last=True,
            )
            shf_loader_iter = iter(shf_loader)

            for _ in tqdm(range(len(train_loader)), desc="Iteration: "):
                self.optimizer.zero_grad()
                [(_, _, train_blocks)] = next(train_loader_iter)
                [(_, _, shf_blocks)] = next(shf_loader_iter)

                embed = self.forward(train_blocks,
                                     train_blocks[0].srcdata["feat"])
                embed_shf = self.forward(shf_blocks,
                                         shf_blocks[0].srcdata["feat"])

                mi = self.disc(
                    g_avg,
                    embed.unsqueeze(0),
                    embed_shf.unsqueeze(0),
                )
                loss = self.calc_loss(mi, lbl)
                loss.backward()
                self.optimizer.step()

                loss_epoch = loss_epoch + loss.item()
                g_avg_iter = g_avg_iter + h

            g_avg = self.sigmoid(
                g_avg_iter.unsqueeze(0) /
                (self.batch_size * len(train_loader))).detach()

            print(
                f"Epoch:{epoch}  Average Loss:{loss_epoch / len(train_loader)}"
            )

            if loss_epoch < best:
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
        self, _, _, _ = load_model(
            model_filename
            if model_filename is not None else self.model_filename,
            self,
            self.optimizer,
        )
        graph.apply_nodes(
            lambda nodes: {
                "feat":
                torch.FloatTensor(
                    normalize_feature(sp.lil_matrix(nodes.data["feat"])))
            })

        train_loader = NaiveDataLoader(
            graph=graph,
            batch_size=self.batch_size,
            n_layers=self.n_layers,
            aug_types=["none"],
            device=device,
            drop_last=False,
        )
        embedding = torch.FloatTensor([]).to(device)
        with torch.no_grad():
            for _, [(_, _, blocks)] in tqdm(
                    enumerate(train_loader),
                    desc="Inference: ",
                    total=len(train_loader),
            ):
                input_feats = blocks[0].srcdata["feat"]
                embedding = torch.cat(
                    (
                        embedding,
                        self.forward(blocks, input_feats),
                    ),
                    dim=0,
                )

        return embedding


# for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import set_device
#     from utils import set_seed
#     from utils import sk_clustering
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
#     model = DGIEmbed(
#         in_feats=features.shape[1],
#         out_feats_list=[64],
#         n_epochs=10000,
#         early_stopping_epoch=20,
#         neighbor_sampler_fanouts=[3],
#         batch_size=1024,
#         lr=0.001,
#         l2_coef=0.0,
#         activation='prelu',
#         model_filename='dgi_test',
#     )
#     model.fit(graph=graph, device=device)
#     embedding = model.get_embedding(graph, device)
#     res = sk_clustering(
#         torch.squeeze(embedding, 0).cpu(),
#         n_clusters,
#         name='kmeans',
#     )
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
