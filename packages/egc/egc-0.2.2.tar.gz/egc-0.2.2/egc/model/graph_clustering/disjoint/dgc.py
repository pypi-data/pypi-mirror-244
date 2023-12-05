"""Deep Graph Clustering"""
from typing import List

import dgl
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from tqdm import tqdm

from ....module import InnerProductDecoder
from ....module import MultiLayerGNN
from ....utils import init_weights
from ....utils import load_model
from ....utils import NaiveDataLoader
from ....utils import save_model
from ..base import Base

# from module import MultiLayerDNN


class DGC(Base, nn.Module):
    """Deep Graph Clustering"""

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_clusters: int,
        # classifier_hidden_list: List[int] = None,
        aggregator_type: str = "gcn",
        bias: bool = True,
        encoder_act: List[str] = None,
        # classifier_act: List[str] = None,
        dropout: float = 0.0,
        batch_size: int = 1024,
        n_epochs: int = 1000,
        lr: float = 0.01,
        l2_coef: float = 0.0,
        early_stopping_epoch: int = 20,
        model_filename: str = "dgc",
    ):
        super().__init__()
        nn.Module.__init__(self)
        self.n_clusters = n_clusters
        self.n_epochs = n_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.batch_size = batch_size
        self.n_layers = len(out_feats_list)
        self.norm = None
        self.pos_weight = None
        self.device = None

        self.encoder = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            aggregator_type=aggregator_type,
            bias=bias,
            activation=encoder_act,
            dropout=dropout,
        )
        self.decoder = InnerProductDecoder()
        # self.classifier = MultiLayerDNN(
        #     in_feats=out_feats_list[-1],
        #     out_feats_list=[n_clusters]
        #     if classifier_hidden_list is None else classifier_hidden_list,
        #     activation=['softmax']
        #     if classifier_act is None else classifier_act,
        # )

        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def forward(self, blocks):
        z = self.encoder(blocks, blocks[0].srcdata["feat"])
        preds = z
        adj_hat = self.decoder(preds)
        return preds, adj_hat

    def loss(self, adj_hat: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        return self.norm * F.binary_cross_entropy_with_logits(
            adj_hat.view(-1),
            adj.view(-1),
            pos_weight=self.pos_weight,
        )

    def fit(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        self.device = device
        adj_csr = graph.adj_external(scipy_fmt="csr")

        # (|V|**2 - |E|) / |E|
        self.pos_weight = torch.FloatTensor([
            float(adj_csr.shape[0] * adj_csr.shape[0] - adj_csr.sum()) /
            adj_csr.sum()
        ])
        # |V|**2 / (2 * ((|V|**2 - |E|)))
        self.norm = (adj_csr.shape[0] * adj_csr.shape[0] / float(
            (adj_csr.shape[0] * adj_csr.shape[0] - adj_csr.sum()) * 2))

        data_loader = NaiveDataLoader(
            graph=graph,
            batch_size=self.batch_size,
            n_layers=self.n_layers,
            device=device,
        )
        self.to(device)
        adj = torch.Tensor(adj_csr.todense()).to(device)
        self.pos_weight = self.pos_weight.to(device)

        cnt_wait = 0
        best = 1e9
        for epoch in range(self.n_epochs):
            self.train()

            loss_epoch = 0
            for _, ((_, _, blocks), ) in enumerate(data_loader):
                self.optimizer.zero_grad()

                _, adj_hat = self.forward(blocks)

                loss = self.loss(adj_hat, adj)

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
        self.to(device)

        data_loader = NaiveDataLoader(
            graph=graph,
            batch_size=self.batch_size,
            n_layers=self.n_layers,
            device=device,
        )

        embedding = []
        for _, ((_, _, blocks), ) in tqdm(
                enumerate(data_loader),
                desc="Inference:",
                total=len(data_loader),
        ):
            with torch.no_grad():
                preds, _ = self.forward(blocks)
            embedding.extend(preds.cpu().detach().numpy())
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
        return self.get_embedding(graph, device).argmax(dim=1).cpu().numpy()


# # for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import set_device
#     from utils import set_seed

#     import scipy.sparse as sp
#     import time

#     device = set_device('0')
#     set_seed(4096)

#     # datasets = ['Cora', 'Citeseer', 'Pubmed', 'ACM', 'BlogCatalog', 'Flickr']
#     datasets = ['Pubmed', 'ACM', 'BlogCatalog', 'Flickr']

#     for ds in datasets:
#         graph, label, n_clusters = load_data(dataset_name=ds)
#         features = graph.ndata["feat"]
#         adj_csr = graph.adj_external(scipy_fmt='csr')
#         edges = graph.edges()
#         features_lil = sp.lil_matrix(features)
#         for out_feats, en_act in zip(
#             [
#                 [500, n_clusters],
#                 [500, n_clusters],
#                 [500, 256, n_clusters],
#                 [500, 256, n_clusters],
#             ],
#             [
#                 ['relu', 'softmax'],
#                 ['relu', 'none'],
#                 ['relu', 'relu', 'softmax'],
#                 ['relu', 'relu', 'none'],
#             ],
#         ):
#             for l in [0.01, 0.001]:
#                 for agg in ['gcn', 'mean']:
#                     print(f'\n\n\t{ds} \t{out_feats} \t{en_act} \t{l} \t{agg} \t4096\n\n')
#                     start_time = time.time()
#                     model = DGC(
#                         in_feats=features.shape[1],
#                         out_feats_list=out_feats,
#                         encoder_act=en_act,
#                         classifier_hidden_list=[n_clusters],
#                         classifier_act=['linear'],
#                         n_clusters=n_clusters,
#                         aggregator_type=agg,
#                         bias=True,
#                         batch_size=graph.num_nodes(),
#                         n_epochs=800,
#                         lr=l,
#                         l2_coef=0.0,
#                         early_stopping_epoch=20,
#                         model_filename='dgc',
#                     )
#                     model.fit(graph=graph, device=device)
#                     res = model.get_memberships(graph, device)
#                     elapsed_time = time.time() - start_time
#                     (
#                         ARI_score,
#                         NMI_score,
#                         ACC_score,
#                         Micro_F1_score,
#                         Macro_F1_score,
#                     ) = evaluation(label, res)
#                     print("\n"
#                         f"Elapsed Time:{elapsed_time:.2f}s\n"
#                         f"ARI:{ARI_score}\n"
#                         f"NMI:{ NMI_score}\n"
#                         f"ACC:{ACC_score}\n"
#                         f"Micro F1:{Micro_F1_score}\n"
#                         f"Macro F1:{Macro_F1_score}\n")
