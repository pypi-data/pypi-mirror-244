"""Deep Graph Clustering"""
from typing import List

import dgl
import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from torch import nn
from tqdm import tqdm

from ....model.graph_clustering.base import Base
from ....module import InnerProductDecoder
from ....module import MultiLayerDNN
from ....module import MultiLayerGNN
from ....utils import init_weights
from ....utils import load_model
from ....utils import NaiveDataLoader
from ....utils import save_model
from ....utils import sparse_mx_to_torch_sparse_tensor
from ....utils import torch_sparse_to_dgl_graph


class DGC(Base, nn.Module):
    """Deep Graph Clustering"""

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_clusters: int,
        classifier_hidden_list: List[int] = None,
        aggregator_type: str = "gcn",
        bias: bool = True,
        k: int = 20,
        tau: float = 0.9999,
        encoder_act: List[str] = None,
        classifier_act: List[str] = None,
        dropout: float = 0.0,
        n_epochs: int = 1000,
        n_pretrain_epochs: int = 800,
        lr: float = 0.01,
        l2_coef: float = 0.0,
        early_stopping_epoch: int = 20,
        model_filename: str = "dgc_mlp_gsl",
    ):
        super().__init__()
        nn.Module.__init__(self)
        self.n_clusters = n_clusters
        self.n_epochs = n_epochs
        self.n_pretrain_epochs = n_pretrain_epochs
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.n_layers = len(out_feats_list)
        self.k = k
        self.tau = tau
        self.norm = None
        self.pos_weight = None
        self.device = None
        self.batch_size = None

        self.encoder = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            aggregator_type=aggregator_type,
            bias=bias,
            activation=encoder_act,
            dropout=dropout,
        )
        self.decoder = InnerProductDecoder()
        self.classifier = MultiLayerDNN(
            in_feats=out_feats_list[-1],
            out_feats_list=[n_clusters]
            if classifier_hidden_list is None else classifier_hidden_list,
            activation=["softmax"]
            if classifier_act is None else classifier_act,
        )

        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def load_best_model(self, device: torch.device) -> None:
        self, _, _, _ = load_model(self.model_filename, self, self.optimizer)
        self.to(device)

    def forward(self, blocks):
        z = self.encoder(blocks, blocks[0].srcdata["feat"])
        preds = self.classifier(z)
        adj_hat = self.decoder(preds)
        return preds, adj_hat

    def loss(self, adj_hat: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        return self.norm * F.binary_cross_entropy_with_logits(
            adj_hat.view(-1),
            adj.view(-1),
            pos_weight=self.pos_weight,
        )

    def pretrain(
        self,
        data_loader: NaiveDataLoader,
        adj_label: torch.Tensor,
    ) -> None:
        cnt_wait = 0
        best = 1e9
        print("Train Encoder Start.")
        for epoch in range(self.n_pretrain_epochs):
            self.train()

            loss_epoch = 0
            for _, ((_, _, blocks), ) in enumerate(data_loader):
                self.optimizer.zero_grad()

                _, adj_hat = self.forward(blocks)

                loss = self.loss(adj_hat, adj_label)

                loss.backward()
                self.optimizer.step()
                loss_epoch += loss.item()

            if epoch % 50 == 0:
                print(
                    f"Pretrain Epoch: {epoch+1:04d}\t Loss:{loss_epoch / len(data_loader) :.8f}"
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
                print("Pretrain Encoder Done.")
                break

        self.load_best_model(self.device)

    def learn_structure(self, preds: torch.Tensor) -> torch.Tensor:
        q = torch.mm(preds, preds.t())
        _, indices = q.topk(k=self.k, dim=-1)
        mask = torch.zeros(q.shape).to(self.device)
        mask[torch.arange(q.shape[0]).view(-1, 1), indices] = 1
        adj_new = F.relu(mask * q)
        return adj_new

    def fit(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        self.device = device
        self.batch_size = graph.num_nodes()
        adj_raw = graph.adj().to(device)
        adj = adj_raw.to_dense()

        for _ in range(self.n_epochs):
            adj_sum = adj.sum()
            # (|V|**2 - |E|) / |E|
            self.pos_weight = torch.FloatTensor([
                float(adj.shape[0] * adj.shape[0] - adj_sum) / adj_sum
            ]).to(device)
            # |V|**2 / (2 * ((|V|**2 - |E|)))
            self.norm = (adj.shape[0] * adj.shape[0] / float(
                (adj.shape[0] * adj.shape[0] - adj_sum) * 2))

            data_loader = NaiveDataLoader(
                graph=graph,
                batch_size=self.batch_size,
                n_layers=self.n_layers,
                device=device,
            )
            self.to(device)

            self.pretrain(data_loader=data_loader, adj_label=adj)

            preds = self.get_embedding(graph, device)
            # res = preds.argmax(dim=1).cpu().numpy()
            # (
            #     ARI_score,
            #     NMI_score,
            #     ACC_score,
            #     Micro_F1_score,
            #     Macro_F1_score,
            # ) = evaluation(label, res)
            # print("\n"
            #     f"ARI:{ARI_score}\n"
            #     f"NMI:{ NMI_score}\n"
            #     f"ACC:{ACC_score}\n"
            #     f"Micro F1:{Micro_F1_score}\n"
            #     f"Macro F1:{Macro_F1_score}\n")
            adj = self.tau * adj + (1 - self.tau) * self.learn_structure(preds)
            graph_new = torch_sparse_to_dgl_graph(
                sparse_mx_to_torch_sparse_tensor(
                    sp.csr_matrix(adj.cpu().numpy())))
            graph_new.ndata["feat"] = graph.ndata["feat"].to(device)
            graph = graph_new

    def get_embedding(
            self,
            graph: dgl.DGLGraph,
            device: torch.device = torch.device("cpu"),
    ) -> torch.Tensor:
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        self.load_best_model(device=device)

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
            embedding.extend(preds.cpu().numpy())
        return torch.Tensor(embedding).to(device)

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

#     graph, label, n_clusters = load_data(dataset_name='Cora')
#     features = graph.ndata["feat"]
#     adj_csr = graph.adj_external(scipy_fmt='csr')
#     edges = graph.edges()
#     features_lil = sp.lil_matrix(features)

#     model = DGC(
#         in_feats=features.shape[1],
#         out_feats_list=[500],
#         classifier_hidden_list=[7],
#         aggregator_type='mean',
#         n_clusters=n_clusters,
#         bias=True,
#         k=20,
#         tau=0.9999,
#         encoder_act=['relu'],
#         classifier_act=['softmax'],
#         dropout=0.0,
#         n_epochs=1000,
#         n_pretrain_epochs=800,
#         lr=0.001,
#         l2_coef=0.0,
#         early_stopping_epoch=20,
#         model_filename='dgc_mlp_gsl',
#     )
#     model.fit(graph=graph, device=device)
#     res = model.get_memberships(graph, device)
#     (
#         ARI_score,
#         NMI_score,
#         ACC_score,
#         Micro_F1_score,
#         Macro_F1_score,
#     ) = evaluation(label, res)
#     print("\n"
#           f"ARI:{ARI_score}\n"
#           f"NMI:{ NMI_score}\n"
#           f"ACC:{ACC_score}\n"
#           f"Micro F1:{Micro_F1_score}\n"
#           f"Macro F1:{Macro_F1_score}\n")
