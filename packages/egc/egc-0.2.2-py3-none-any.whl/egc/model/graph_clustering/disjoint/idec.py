"""DEC / IDEC

- Paper: Unsupervised Deep Embedding for Clustering Analysis
- Code of the paper author: https://github.com/piiswrong/dec
- Code for reference: https://github.com/XifengGuo/IDEC
"""
from typing import List
from typing import Tuple

import dgl
import numpy as np
import torch
from sklearn.cluster import MiniBatchKMeans
from torch import nn

from ....module import MultiLayerDNN
from ....module import MultiLayerGNN
from ....utils import init_weights
from ....utils import load_model
from ....utils import NaiveDataLoader
from ....utils import save_model
from ..base import Base

# pylint:disable=self-cls-assignment


class IDEC(Base, nn.Module):
    """DEC / IDEC. Set beta to 0.0 for DEC or to nonzero for IDEC.

    Args:
        in_feats (int): Input feature size.
        out_feats_list (List[int]):  List of hidden units dimensions.
        n_clusters (int): Num of clusters.
        aggregator_type (str, optional): Aggregator type to use \
            (``mean``, ``gcn``, ``pool``, ``lstm``). Defaults to 'gcn'.
        bias (bool, optional): If True, adds a learnable bias to the output. Defaults to True.
        batch_size (int, optional): Batch size. Defaults to 1024.
        alpha (float, optional): Alpha of student-T distribution. Defaults to 1.0.
        beta (float, optional): Coeffecient of reconstruction loss. 0.0 for DEC while nonzero \
            for IDEC. Defaults to 10.0.
        n_epochs (int, optional): Maximum training epochs. Defaults to 1000.
        n_pretrain_epochs (int, optional): Maximum pretraining epochs. Defaults to 400.
        lr (float, optional): Learning Rate. Defaults to 0.001.
        l2_coef (float, optional): Weight decay. Defaults to 0.0.
        early_stopping_epoch (int, optional): Early stopping threshold. Defaults to 20.
        model_filename (str, optional): Path to store model parameters. Defaults to 'dec'.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        n_clusters: int,
        aggregator_type: str = "gcn",
        bias: bool = True,
        batch_size: int = 1024,
        alpha: float = 1.0,
        beta: float = 10.0,
        n_epochs: int = 1000,
        n_pretrain_epochs: int = 400,
        lr: float = 0.001,
        l2_coef: float = 0.0,
        early_stopping_epoch: int = 20,
        model_filename: str = "dec",
    ) -> None:
        super().__init__()
        nn.Module.__init__(self)
        self.batch_size = batch_size
        self.n_clusters = n_clusters
        self.n_epochs = n_epochs
        self.n_pretrain_epochs = n_pretrain_epochs
        self.alpha = alpha
        self.beta = beta
        self.early_stopping_epoch = early_stopping_epoch
        self.model_filename = model_filename
        self.n_layers = len(out_feats_list)

        self.encoder = MultiLayerGNN(
            in_feats=in_feats,
            out_feats_list=out_feats_list,
            aggregator_type=aggregator_type,
            bias=bias,
            activation=["relu"] * (self.n_layers - 1) + ["none"],
        )

        self.decoder = MultiLayerDNN(
            in_feats=out_feats_list[-1],
            out_feats_list=out_feats_list[::-1][1:] + [in_feats],
        )

        self.cluster_centers = nn.Parameter(
            torch.Tensor(n_clusters, out_feats_list[-1]))
        self.mbk = MiniBatchKMeans(
            n_clusters=self.n_clusters,
            n_init=20,
            batch_size=batch_size,
        )

        self.mse = nn.MSELoss()
        self.kld = nn.KLDivLoss()
        self.optimizer = torch.optim.Adam(
            self.parameters(),
            lr=lr,
            weight_decay=l2_coef,
        )

        for module in self.modules():
            init_weights(module)

    def clustering(
            self,
            h: torch.Tensor,
            device: torch.device = torch.device("cpu"),
    ) -> None:
        """Clustering by miniBatchKmeans.

        Args:
            h (torch.Tensor): features.
            device (torch.device, optional): torch device. Defaults to torch.device('cpu').
        """
        self.mbk.partial_fit(h.detach().cpu().numpy())
        self.cluster_centers.data = torch.Tensor(
            self.mbk.cluster_centers_).to(device)

    def get_distance(
        self,
        h: torch.Tensor,
    ) -> torch.Tensor:
        """Get the distance sum of all the point to each center.

        Args:
            h (torch.Tensor): features.

        Returns:
            distance (torch.Tensor): distance sum of all the point to each center.
        """
        x_miu = torch.unsqueeze(h, 1) - self.cluster_centers
        distance = torch.sum(torch.mul(x_miu, x_miu), 2)
        return distance

    def get_t_distribution(
        self,
        h: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Student t-distribution, as same as used in t-SNE algorithm.
        q_ij = 1/(1+dist(x_i, u_j)^2), then normalize it.

        Args:
            h (torch.Tensor): features.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: (distance, q)
        """
        d = self.get_distance(h)
        q = 1.0 / (1.0 + (d / self.alpha))
        q = q**(self.alpha + 1.0) / 2.0
        q = (q.t() / torch.sum(q, 1)).t()
        return q, d

    @staticmethod
    def target_distribution(q: torch.Tensor) -> torch.Tensor:
        weight = q**2 / q.sum(0)
        return (weight.T / weight.sum(1)).T

    def pretrain(
        self,
        train_loader: NaiveDataLoader,
        features: torch.Tensor,
    ) -> None:
        cnt_wait = 0
        best = 1e9
        for epoch in range(self.n_pretrain_epochs):
            self.optimizer.zero_grad()
            self.train()
            running_loss = 0.0
            for step, [(_, output_x, block)] in enumerate(train_loader):
                x = features[output_x]
                _, x_de = self.forward(block)
                loss = self.mse(x_de, x)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
                print(f"[{epoch + 1}, {step + 1}] loss: {running_loss:.7f}")

            if round(running_loss, 8) < best:
                best = running_loss
                cnt_wait = 0
                save_model(
                    self.model_filename,
                    self,
                    self.optimizer,
                    epoch,
                    running_loss,
                )
            else:
                cnt_wait += 1

            if cnt_wait == self.early_stopping_epoch:
                print("Early stopping!")
                break

    def forward(self, blocks) -> Tuple[torch.Tensor, torch.Tensor]:
        input_feat = blocks[0].srcdata["feat"]
        x_en = self.encoder(blocks, input_feat)
        x_de = self.decoder(x_en)
        return x_en, x_de

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
        self.to(device)

        g = graph.to(device)

        data_loader = NaiveDataLoader(
            graph=g,
            aug_types=["none"],
            batch_size=self.batch_size,
            n_layers=self.n_layers,
            device=device,
            drop_last=True,
        )

        cnt_wait = 0
        best = 1e9

        got_cluster_center = False
        features = g.ndata["feat"]

        self.pretrain(data_loader, features)

        self, _, _, _ = load_model(self.model_filename, self, self.optimizer)

        for epoch in range(self.n_epochs):
            loss_epoch = 0
            for step, [(_, output_x, block)] in enumerate(data_loader):
                self.optimizer.zero_grad()

                if not got_cluster_center:
                    x_en, _ = self.forward(block)
                    self.clustering(x_en, device)
                    if step == len(data_loader) - 1:
                        got_cluster_center = True
                else:
                    # TODO: add idec update interval
                    self.train()
                    x = features[output_x]
                    x_en, x_de = self.forward(block)
                    q, _ = self.get_t_distribution(x_en)
                    p = self.target_distribution(q)

                    re_loss = self.mse(x_de, x)
                    kld_loss = self.kld(q.log(), p)
                    loss = kld_loss + self.beta * re_loss

                    if step % 50 == 0:
                        print(f"Step:{step+1:04d}\tLoss:{loss:.8f}")

                    loss.backward()
                    self.optimizer.step()
                    loss_epoch += loss.item()
            if loss_epoch != 0:
                print(
                    f"Epoch: {epoch+1:04d}\tEpoch Loss:{loss_epoch / len(data_loader) :.10f}"
                )

                if round(loss_epoch, 10) < best:
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
        g = graph.to(device)
        sampler = dgl.dataloading.MultiLayerFullNeighborSampler(self.n_layers)
        data_loader = dgl.dataloading.DataLoader(
            g,
            g.nodes(),
            sampler,
            batch_size=self.batch_size,
            shuffle=False,
            drop_last=False,
            num_workers=4 if device == torch.device("cpu") else 0,
            device=device,
        )
        embedding = []
        self.to(device)
        for _, (_, _, block) in enumerate(data_loader):
            with torch.no_grad():
                h, _ = self.forward(block)
                h = h.cpu().detach().numpy()
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
        q, _ = self.get_t_distribution(
            self.get_embedding(graph, device).to(device))
        return q.data.cpu().numpy().argmax(1)


# # for test only
# if __name__ == "__main__":
#     from utils import load_data
#     from utils import augment_graph
#     from utils import set_device
#     from utils import print_model_parameters
#     import scipy.sparse as sp
#     import torch
#     from utils import normalize_feature
#     from utils import set_seed
#     set_seed(4096)
#     device = set_device(6)
#     graph, label, n_clusters = load_data(
#         dataset_name='Cora',
#         directory='./data',
#     )
#     features = graph.ndata["feat"]
#     features = sp.lil_matrix(features)
#     features = normalize_feature(features)
#     features = torch.FloatTensor(features)
#     # features[features != 0] = 1
#     graph.apply_nodes(lambda nodes: {'feat': features})
#     model = IDEC(
#         in_feats=features.shape[1],
#         out_feats_list=[512, 128],
#         n_clusters=n_clusters,
#         batch_size=2708,
#         n_pretrain_epochs=400,
#         n_epochs=1000,
#         beta=10.0,
#         early_stopping_epoch=20,
#     )
#     # print_model_parameters(model)
#     model.fit(graph, device)

#     # q = model.get_memberships(graph, device)
#     from utils.evaluation import evaluation
#     (
#         ARI_score,
#         NMI_score,
#         ACC_score,
#         Micro_F1_score,
#         Macro_F1_score,
#     ) = evaluation(label, q)
#     print("\ndec\n"
#           f"ARI:{ARI_score}\n"
#           f"NMI:{ NMI_score}\n"
#           f"ACC:{ACC_score}\n"
#           f"Micro F1:{Micro_F1_score}\n"
#           f"Macro F1:{Macro_F1_score}\n")
#     from utils import sk_clustering
#     res = sk_clustering(
#         torch.squeeze(
#             model.get_embedding(graph, device),
#             0,
#         ).cpu(),
#         n_clusters,
#         name='kmeans',
#     )
#     from utils.evaluation import evaluation
#     (
#         ARI_score,
#         NMI_score,
#         ACC_score,
#         Micro_F1_score,
#         Macro_F1_score,
#     ) = evaluation(label, res)
#     print("\nkmeans\n"
#           f"ARI:{ARI_score}\n"
#           f"NMI:{ NMI_score}\n"
#           f"ACC:{ACC_score}\n"
#           f"Micro F1:{Micro_F1_score}\n"
#           f"Macro F1:{Macro_F1_score}\n")
