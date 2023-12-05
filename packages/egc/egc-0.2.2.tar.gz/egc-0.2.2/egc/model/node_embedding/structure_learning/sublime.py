"""
Towards Unsupervised Deep Graph Structure Learning
https://shiruipan.github.io/publication/www-22-liu/www-22-liu.pdf
"""
import copy

import numpy as np
import torch
from sklearn.cluster import KMeans
from torch import nn

from ....module import ATT_learner
from ....module import FGP_learner
from ....module import GCL_SUBLIME
from ....module import GNN_learner
from ....module import MLP_learner
from ....utils import dgl_graph_to_torch_sparse
from ....utils import normalize_sublime
from ....utils import sparse_mx_to_torch_sparse_tensor
from ....utils import torch_sparse_to_dgl_graph
from ....utils.sublime_utils import get_feat_mask
from ....utils.sublime_utils import split_batch
from ....utils.sublime_utils import symmetrize

# from utils import sk_clustering
# from utils.sublime_utils import clustering_metrics

# pylint: disable=too-many-branches


class SUBLIME(nn.Module):
    """SUBLIME:Towards Unsupervised Deep Graph Structure Learning

    Args:

    """

    def __init__(
        self,
        nfeats,
        n_clusters,
        sparse: int = 0,
        type_learner: str = "fgp",
        k: int = 20,
        sim_function: str = "cosine",
        activation_learner: str = "relu",
        nlayers: int = 2,
        hidden_dim: int = 512,
        rep_dim: int = 256,
        proj_dim: int = 256,
        dropout: float = 0.5,
        dropedge_rate: float = 0.5,
        lr: float = 0.001,
        w_decay: float = 0.0,
        epochs: int = 2500,
        maskfeat_rate_anchor: float = 0.8,
        maskfeat_rate_learner: float = 0.1,
        contrast_batch_size: int = 0,
        tau: float = 0.9999,
        c: int = 0,
        eval_freq: int = 100,
        n_clu_trials: int = 10,
    ):
        super().__init__()
        self.n_clusters = n_clusters
        self.sparse = sparse
        self.type_learner = type_learner
        self.k = k
        self.sim_function = sim_function
        self.activation_learner = activation_learner
        self.lr = lr
        self.w_decay = w_decay
        self.epochs = epochs
        self.maskfeat_rate_anchor = maskfeat_rate_anchor
        self.maskfeat_rate_learner = maskfeat_rate_learner
        self.contrast_batch_size = contrast_batch_size
        self.tau = tau
        self.c = c
        self.eval_freq = eval_freq
        self.n_clu_trials = n_clu_trials
        self.features = None
        self.Adj = None

        if self.type_learner == "fgp":
            self.graph_learner = FGP_learner
        elif self.type_learner == "mlp":
            self.graph_learner = MLP_learner
        elif self.type_learner == "att":
            self.graph_learner = ATT_learner
        elif self.type_learner == "gnn":
            self.graph_learner = GNN_learner

        self.gcl = GCL_SUBLIME(
            nlayers=nlayers,
            in_dim=nfeats,
            hidden_dim=hidden_dim,
            emb_dim=rep_dim,
            proj_dim=proj_dim,
            dropout=dropout,
            dropout_adj=dropedge_rate,
            sparse=sparse,
        )

    def forward(self, features, anchor_adj):
        """Forward Propagation"""
        # view 1: anchor graph
        if self.maskfeat_rate_anchor:
            mask_v1, _ = get_feat_mask(features, self.maskfeat_rate_anchor)
            features_v1 = features * (1 - mask_v1)
        else:
            features_v1 = copy.deepcopy(features)

        z1, _ = self.gcl(features_v1, anchor_adj, "anchor")

        # view 2: learned graph
        if self.maskfeat_rate_learner:
            mask, _ = get_feat_mask(features, self.maskfeat_rate_learner)
            features_v2 = features * (1 - mask)
        else:
            features_v2 = copy.deepcopy(features)

        learned_adj = self.graph_learner(features)
        if not self.sparse:
            learned_adj = symmetrize(learned_adj)
            learned_adj = normalize_sublime(learned_adj, "sym", self.sparse)

        z2, _ = self.gcl(features_v2, learned_adj, "learner")

        # compute loss
        if self.contrast_batch_size:
            node_idxs = list(range(features.shape[0]))
            # random.shuffle(node_idxs)
            batches = split_batch(node_idxs, self.contrast_batch_size)
            loss = 0
            for batch in batches:
                weight = len(batch) / features.shape[0]
                loss += self.gcl.calc_loss(z1[batch], z2[batch]) * weight
        else:
            loss = self.gcl.calc_loss(z1, z2)

        return loss, learned_adj

    def fit(self, adj_csr, features):
        """Fitting

        Args:
            adj_csr (sp.lil_matrix): adj sparse matrix.
            features (torch.Tensor): features.
        """
        # prepare data
        if not self.sparse:
            adj_original = np.array(adj_csr.todense(), dtype="float32")
            anchor_adj_raw = torch.from_numpy(adj_original)
        else:
            adj_original = sparse_mx_to_torch_sparse_tensor(adj_csr)
            anchor_adj_raw = adj_original

        anchor_adj = normalize_sublime(anchor_adj_raw, "sym", self.sparse)
        if self.sparse:
            anchor_adj_torch_sparse = copy.deepcopy(anchor_adj)
            anchor_adj = torch_sparse_to_dgl_graph(anchor_adj)

        # init graph learner
        if self.type_learner == "fgp":
            self.graph_learner = self.graph_learner(features.cpu(), self.k,
                                                    self.sim_function, 6,
                                                    self.sparse)
        elif self.type_learner == "mlp":
            self.graph_learner = self.graph_learner(
                2,
                features.shape[1],
                self.k,
                self.sim_function,
                6,
                self.sparse,
                self.activation_learner,
            )
        elif self.type_learner == "att":
            self.graph_learner = self.graph_learner(
                2,
                features.shape[1],
                self.k,
                self.sim_function,
                6,
                self.sparse,
                self.activation_learner,
            )
        elif self.type_learner == "gnn":
            self.graph_learner = self.graph_learner(
                2,
                features.shape[1],
                self.k,
                self.sim_function,
                6,
                self.sparse,
                self.activation_learner,
                anchor_adj,
            )

        optimizer_cl = torch.optim.Adam(self.gcl.parameters(),
                                        lr=self.lr,
                                        weight_decay=self.w_decay)
        optimizer_learner = torch.optim.Adam(self.graph_learner.parameters(),
                                             lr=self.lr,
                                             weight_decay=self.w_decay)

        if torch.cuda.is_available():
            self.gcl = self.gcl.cuda()
            self.graph_learner = self.graph_learner.cuda()
            features = features.cuda()
            if not self.sparse:
                anchor_adj = anchor_adj.cuda()

        for epoch in range(1, self.epochs + 1):
            self.gcl.train()
            self.graph_learner.train()

            loss, Adj = self.forward(features, anchor_adj)

            optimizer_cl.zero_grad()
            optimizer_learner.zero_grad()
            loss.backward()
            optimizer_cl.step()
            optimizer_learner.step()

            # Structure Bootstrapping
            if (1 - self.tau) and (self.c == 0 or epoch % self.c == 0):
                if self.sparse:
                    learned_adj_torch_sparse = dgl_graph_to_torch_sparse(Adj)
                    anchor_adj_torch_sparse = (
                        anchor_adj_torch_sparse * self.tau +
                        learned_adj_torch_sparse * (1 - self.tau))
                    anchor_adj = torch_sparse_to_dgl_graph(
                        anchor_adj_torch_sparse)
                else:
                    anchor_adj = anchor_adj * self.tau + Adj.detach() * (
                        1 - self.tau)

            print(f"Epoch {epoch:05d} | CL Loss {loss.item():.4f}")

        self.features = features
        self.Adj = Adj

        #     if epoch % self.eval_freq == 0:
        #         self.gcl.eval()
        #         self.graph_learner.eval()
        #         self.features = features
        #         self.Adj = Adj

        #         # _, embedding = self.gcl(features, Adj)
        #         # embedding = embedding.cpu().detach().numpy()
        #         embedding = self.get_embedding()

        #         acc_mr, nmi_mr, f1_mr, ari_mr = [], [], [], []
        #         for clu_trial in range(self.n_clu_trials):
        #             kmeans = KMeans(n_clusters=self.n_clusters,
        #                             random_state=clu_trial).fit(embedding)
        #             predict_labels = kmeans.predict(embedding)
        #             cm_all = clustering_metrics(label.cpu().numpy(), predict_labels)
        #             acc_, nmi_, f1_, ari_ = cm_all.evaluationClusterModelFromLabel(
        #                                             print_results=False)
        #             # predict_labels = self.get_memberships(clu_trial)
        #             # ari_,nmi_,acc_,_, f1_ = evaluation(label, predict_labels)

        #             acc_mr.append(acc_)
        #             nmi_mr.append(nmi_)
        #             f1_mr.append(f1_)
        #             ari_mr.append(ari_)

        #             print(" ACC: ", acc_)
        #             print(" NMI: ", nmi_)
        #             print(" F-score: ", f1_)
        #             print(" ARI: ", ari_)

        #         acc, nmi, f1, ari = np.mean(acc_mr), np.mean(nmi_mr), \
        #                             np.mean(f1_mr), np.mean(ari_mr)

        # print("Final ACC: ", acc)
        # print("Final NMI: ", nmi)
        # print("Final F-score: ", f1)
        # print("Final ARI: ", ari)

    def get_embedding(self):
        """Get the embeddings."""
        _, embedding = self.gcl(self.features, self.Adj)
        embedding = embedding.cpu().detach()
        return embedding

    def get_memberships(self):
        """Get memberships

        Returns:
            np.ndarray: memberships
        """
        embedding = self.get_embedding()
        kmeans = KMeans(n_clusters=self.n_clusters).fit(embedding)
        predict_labels = kmeans.predict(embedding)
        return predict_labels
        # return sk_clustering(torch.squeeze(pred, 0).cpu(),
        #                      self.n_clusters,
        #                      name='kmeans')


# # for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation,best_mapping
#     from utils import set_device
#     from utils import set_seed
#     import scipy.sparse as sp
#     import time
#     import pandas as pd

#     set_seed(4096)
#     device = set_device('1')

#     dataset = 'Citeseer'
#     graph, label, n_clusters = load_data(
#         dataset_name=dataset,
#         directory='./data',
#     )
#     print(graph)
#     adj_csr = graph.adj_external(scipy_fmt='csr')
#     features = graph.ndata["feat"]

#     start_time = time.time()
#     model = SUBLIME(nfeats=features.shape[1],
#                   n_clusters=n_clusters)
#     model.fit(adj_csr,features)
#     res = model.get_memberships(1)
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
#     # labels_true, labels_pred = best_mapping(label.cpu().numpy(), res)
#     # df_res = pd.DataFrame({'label':labels_true,'pred':labels_pred})
#     # df_res.to_pickle(f'./tmp/MVGRL_{dataset}_pred.pkl')
#     # print('write to',f'./tmp/MVGRL_{dataset}_pred.pkl')
