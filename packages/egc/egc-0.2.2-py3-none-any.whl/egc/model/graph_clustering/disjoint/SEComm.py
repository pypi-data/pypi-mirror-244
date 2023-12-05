"""
SEComm implement
"""
# pylint:disable=W0201,R0912,E0012,W0223,R0915,E1102
import gc
import math
import random
from copy import deepcopy
from time import perf_counter as t

import torch
import torch.nn.functional as F
from dgl import DropEdge
from dgl.nn.pytorch.conv import GraphConv
from sklearn.preprocessing import normalize
from torch import nn
from tqdm import tqdm

from ....module import SECommClusterModel as ClusterModel
from ....module import SECommEncoder as Encoder
from ....module import SECommGraceModel as GraceModel
from ....module import SECommSelfExpr as SelfExpr
from ....utils.SEComm_utils import drop_feature
from ....utils.SEComm_utils import dropout_adj0
from ....utils.SEComm_utils import enhance_sim_matrix
from ....utils.SEComm_utils import label_classification
from ..base import Base


class SEComm(Base, nn.Module):
    """SEComm model

    Args:
        see `utils/argparser.py` _SEComm_subparser function
    """

    def __init__(
        self,
        n_clusters: int,
        n_nodes: int,
        num_features: int,
        activation: str,
        base_model: str,
        batch_size: int,
        num_hidden: int,
        num_layers: int,
        num_proj_hidden: int,
        tau: float,
        num_cl_hidden: int,
        dropout: float,
        pretrain_epochs: int,
        learning_rate: float,
        weight_decay: float,
        drop_edge_rate_1: float,
        drop_edge_rate_2: float,
        drop_feature_rate_1: float,
        drop_feature_rate_2: float,
        x_norm: bool,
        iterations: int,
        threshold: float,
        se_epochs: int,
        se_alpha: float,
        se_patience: int,
        se_lr: float,
        cluster_epochs: int,
        cluster_alpha: float,
        final_beta: float,
        cluster_patience: int,
    ):
        Base.__init__(self)
        nn.Module.__init__(self)
        self.n_clusters = n_clusters
        self.n_nodes = n_nodes
        self.num_features = num_features
        self.activation = ({"relu": F.relu, "prelu": nn.PReLU()})[activation]
        self.base_model = ({"GCNConv": GraphConv})[base_model]
        self.batch_size = n_nodes if batch_size == 0 else batch_size
        self.num_hidden = num_hidden
        self.num_layers = num_layers
        self.num_proj_hidden = num_proj_hidden
        self.tau = tau
        self.num_cl_hidden = num_cl_hidden
        self.dropout = dropout
        self.pretrain_epochs = pretrain_epochs
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.drop_edge_rate_1 = drop_edge_rate_1
        self.drop_edge_rate_2 = drop_edge_rate_2
        self.drop_feature_rate_1 = drop_feature_rate_1
        self.drop_feature_rate_2 = drop_feature_rate_2
        self.x_norm = x_norm
        self.iterations = iterations
        self.threshold = threshold
        self.se_epochs = se_epochs
        self.se_alpha = se_alpha
        self.se_patience = se_patience
        self.se_lr = se_lr
        self.cluster_epochs = cluster_epochs
        self.cluster_alpha = cluster_alpha
        self.final_beta = final_beta
        self.cluster_patience = cluster_patience
        self.graph = None
        self.features = None
        self.best_gracemodel = None

        self.encoder = Encoder(
            self.num_features,
            self.num_hidden,
            self.activation,
            self.base_model,
            k=self.num_layers,
        )
        self.gracemodel = GraceModel(
            self.encoder,
            self.num_hidden,
            self.num_proj_hidden,
            self.tau,
        )
        self.semodel = SelfExpr(self.batch_size)
        self.clustermodel = ClusterModel(
            self.num_hidden,
            self.num_cl_hidden,
            self.n_clusters,
            self.dropout,
        )

    def forward(self):
        pass

    def fit(self, graph, features, label):
        """Fitting a SEComm model

        Args:
            graph (dgl.DGLGraph): data graph.
            features (torch.Tensor): features.
            label (torch.Tensor): label of node's cluster
        """
        self.graph = graph

        # TRICK here
        features[features > 0.0] = 1

        self.features = features
        self.label = label

        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            print(f"GPU available: SEComm Using {self.device}")
            self.to(self.device)
            self.graph = self.graph.to(self.device)
            self.features = self.features.to(self.device)
            self.encoder = self.encoder.to(self.device)
            self.gracemodel = self.gracemodel.to(self.device)
            self.semodel = self.semodel.to(self.device)
            self.clustermodel = self.clustermodel.to(self.device)
            self.label = self.label.to(self.device)
        else:
            self.device = torch.device("cpu")

        # ============== Pre-training Module ================#
        # TODO 拆分GRACE为独立embedding模型
        print(
            "Pre-training GRACE model to get baseline embedding for Self Expressive Layer"
        )

        grace_time = 0
        graceoptimizer = torch.optim.Adam(
            self.gracemodel.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        start = t()
        prev = start
        for epoch in range(1, self.pretrain_epochs + 1):
            # if epoch==10:break
            self.gracemodel.train()
            graceoptimizer.zero_grad()
            # transform1 = DropEdge(self.drop_edge_rate_1)
            # graph_index_1 = transform1(self.graph)
            # transform2 = DropEdge(self.drop_edge_rate_2)
            # graph_index_2 = transform2(self.graph)
            graph_index_1 = dropout_adj0(
                self.graph,
                self.features.shape[0],
                p=self.drop_edge_rate_1,
            )
            graph_index_2 = dropout_adj0(
                self.graph,
                self.features.shape[0],
                p=self.drop_edge_rate_2,
            )
            x_1 = drop_feature(self.features, self.drop_feature_rate_1)
            x_2 = drop_feature(self.features, self.drop_feature_rate_2)

            z1 = self.gracemodel(
                graph_index_1.to(self.device),
                x_1.to(self.device),
            )
            z2 = self.gracemodel(
                graph_index_2.to(self.device),
                x_2.to(self.device),
            )

            loss = self.gracemodel.loss(z1, z2, batch_size=self.batch_size)
            loss.backward()
            graceoptimizer.step()

            now = t()
            print(
                f"(T) | Epoch={epoch:03d}, loss={loss.item():.4f}, "
                f"this epoch time {now - prev:.4f}, total time {now - start:.4f}",
            )
            prev = now

        grace_time = t() - start
        print("Saving pre-trained GRACE Model")
        self.best_gracemodel = deepcopy(self.gracemodel)
        del self.gracemodel
        torch.cuda.empty_cache()
        gc.collect()

        # ============== Self-Expressive Layer training Module ================#
        print("Loading pre-trained GRACE model")
        se_time = 0

        print(
            "=== Supervised Accuracy test for GRACE Embeddings Generated ===")
        self.best_gracemodel.eval()
        z = self.best_gracemodel(self.graph, self.features)
        label_classification(z, self.label, ratio=0.1)

        X = self.best_gracemodel(self.graph, self.features).detach()

        if self.x_norm:
            print(
                "Normalizing embeddings before Self Expressive layer training",
            )
            X = normalize(X.cpu().numpy())
            X = torch.tensor(X).to(self.device)

        from_list = []
        to_list = []
        val_list = []
        seoptimizer = torch.optim.Adam(
            self.semodel.parameters(),
            lr=self.se_lr,
            weight_decay=self.weight_decay,
        )

        start_se = t()
        for _ in tqdm(range(self.iterations), desc="self expressive training"):
            train_labels = random.sample(
                list(range(self.n_nodes)),
                self.batch_size,
            )
            x_train = X[train_labels]

            x1 = x_train
            best_loss = 1e9
            bad_count = 0
            for epoch in range(self.se_epochs + 1):
                self.semodel.train()
                seoptimizer.zero_grad()

                c, x2 = self.semodel(x1)

                se_loss = torch.norm(x1 - x2)
                reg_loss = torch.norm(c)
                loss = se_loss + self.se_alpha * reg_loss
                loss.backward()
                seoptimizer.step()

                print(
                    f"se_loss: {se_loss.item():.9f}",
                    f"reg_loss: {reg_loss.item():.9f}",
                    f"full_loss: {loss.item():.9f}",
                )

                if loss.item() < best_loss:
                    if torch.cuda.is_available():
                        best_c = c.cpu()
                    else:
                        best_c = c
                    bad_count = 0
                    best_loss = loss.item()
                else:
                    bad_count += 1
                    if bad_count == self.se_patience:
                        break

            C = best_c
            C = C.cpu().detach().numpy()
            S = enhance_sim_matrix(C, self.n_clusters, 4, 1)

            print("Retriving similarity values for point pairs")
            count = 0
            # RFE: Optimize this for faster runtime
            threshold = self.threshold
            for i in range(self.batch_size):
                for j in range(self.batch_size):
                    if i == j:
                        continue
                    if S[i, j] >= (1 - threshold) or (S[i, j] <= threshold
                                                      and S[i, j] >= 0):
                        from_list.append(train_labels[i])
                        to_list.append(train_labels[j])
                        val_list.append(S[i, j])
                        count += 1
            print(
                f"Included values for {count} points out of {self.batch_size * self.batch_size}"
            )

        se_time = t() - start_se
        print(f"Self Expressive Layer training done. time:{se_time}")

        # ============== Final full training Module ================#
        print("\n\n\nStarting final full training module")

        start_cluster = t()
        fulloptimizer = torch.optim.Adam(
            (list(self.best_gracemodel.parameters()) +
             list(self.clustermodel.parameters())),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        best_loss = 1e9
        bad_count = 0

        for epoch in range(self.cluster_epochs + 1):
            self.best_gracemodel.train()
            self.clustermodel.train()
            fulloptimizer.zero_grad()
            # transform1 = DropEdge(self.drop_edge_rate_1)
            # graph_index_1 = transform1(self.graph)
            # transform2 = DropEdge(self.drop_edge_rate_2)
            # graph_index_2 = transform2(self.graph)

            graph_index_1 = dropout_adj0(self.graph,
                                         self.features.shape[0],
                                         p=self.drop_edge_rate_1)
            graph_index_2 = dropout_adj0(self.graph,
                                         self.features.shape[0],
                                         p=self.drop_edge_rate_2)
            x_1 = drop_feature(self.features, self.drop_feature_rate_1)
            x_2 = drop_feature(self.features, self.drop_feature_rate_2)

            z1 = self.best_gracemodel(graph_index_1.to(self.device),
                                      x_1.to(self.device))
            z2 = self.best_gracemodel(graph_index_2.to(self.device),
                                      x_2.to(self.device))
            grace_loss = self.best_gracemodel.loss(z1, z2, batch_size=4000)

            z_full = self.clustermodel(
                self.best_gracemodel(self.graph, self.features))
            z_from = z_full[from_list]
            z_to = z_full[to_list]
            pred_similarity = torch.sum(z_from * z_to, dim=1)

            numer2 = torch.mm(z_full.T, z_full)
            denom2 = torch.norm(numer2)
            identity_mat = torch.eye(self.n_clusters)
            if torch.cuda.is_available():
                identity_mat = identity_mat.to(self.device)

            B = identity_mat / math.sqrt(self.n_clusters)
            C = numer2 / denom2
            loss1 = F.mse_loss(pred_similarity,
                               torch.FloatTensor(val_list).to(self.device))
            loss2 = torch.norm(B - C)

            loss = self.final_beta * grace_loss + loss1 + self.cluster_alpha * loss2
            loss.backward()
            fulloptimizer.step()
            print(
                f"Epoch: {epoch} ",
                f"full_loss: {loss.item():.5f} "
                f"grace_loss: {grace_loss.item():.5f} "
                f"loss1: {loss1.item():.5f} "
                f"loss2: {loss2.item():.5f} "
                f"time: {t() - start_cluster}",
            )

            if loss2.item() < best_loss:
                bad_count = 0
                best_loss = loss2.item()
            else:
                bad_count += 1
                print(
                    f"Model not improved for {bad_count} consecutive epochs.")
                if bad_count == self.cluster_patience:
                    print("Early stopping Cluster Train...")
                    break

        convergence_loss = best_loss
        cluster_time = t() - start_cluster
        print(f"Final model training done.. time:{cluster_time}"
              f"Total training time:{cluster_time+se_time+grace_time}"
              f"Convergence Loss:{convergence_loss}")

    def get_embedding(self):
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding.
        """
        z = self.best_gracemodel(self.graph, self.features)
        return z.cpu().detach()

    def get_memberships(self):
        """Get the memberships (graph or node level).

        Returns:
            (numpy.ndarray): memberships.
        """
        z = self.clustermodel(self.best_gracemodel(self.graph, self.features))

        return torch.argmax(z, dim=1).cpu().detach().numpy()
