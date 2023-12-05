"""
Graph Debiased Contrastive Learning with Joint Representation Clustering
https://www.ijcai.org/proceedings/2021/0473.pdf
"""
import random

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from torch import nn
from torch.nn.parameter import Parameter

from ....utils import compute_ppr
from ....utils import get_checkpoint_path
from ....utils import normalize_feature
from ....utils import save_model
from ....utils import sparse_mx_to_torch_sparse_tensor
from ....utils import symmetrically_normalize_adj
from ....utils.evaluation import evaluation
from ...node_embedding.mvgrl import MVGRL

# pylint:disable=too-many-branches,too-many-statements


# Borrowed from https://github.com/PetarV-/DGI
class Readout(nn.Module):
    """read out"""

    @staticmethod
    def forward(seq, msk):
        """Forward Propagation

        Args:
            seq (torch.Tensor): features tensor.
            msk (torch.Tensor): node mask.

        Returns:
            (torch.Tensor):  graph-level representation
        """
        if msk is None:
            return torch.mean(seq, 1)
        msk = torch.unsqueeze(msk, -1)
        return torch.mean(seq * msk, 1) / torch.sum(msk)


class GDCL(nn.Module):
    """GDCL: Graph Debiased Contrastive Learning with Joint Representation Clustering

    Args:
        in_feats (int): Input feature size.
        n_clusters (int): Num of clusters.
        n_h (int): hidden units dimension. Defaults to 512.
        nb_epochs: epoch number of GDCL . Defaults to 1500.
        lr: learning rate of GDCL. Defaults to 0.00005.
        alpha: alpha parameter of distribution. Defaults to 0.0001.
        mask_num: mask number. Defaults to 100.
        batch_size: batch size of GDCL. Defaults to 4.
        update_interval: update interval of GDCL. Defaults to 10.
        model_filename: model filename of GDCL. Defaults to 'gdcl'.
        beta: balance factor. Defaults to 10e-4.
        weight_decay: weight decay of GDCL. Defaults to 0.0.
        pt_n_h:hidden units dimension of pretrained MVGRL. Defaults to 512.
        pt_model_filename: model filename of pretrained MVGRL. Defaults to 'mvgrl'.
        pt_nb_epochs: epoch number of pretrained MVGRL. Defaults to 3000.
        pt_patience: patience of pretrained MVGRL. Defaults to 20.
        pt_lr: learning rate of pretrained MVGRL. Defaults to 0.001.
        pt_weight_decay: weight decay of pretrained MVGRL. Defaults to 0.0.
        pt_sample_size: sample size of pretrained MVGRL. Defaults to 2000.
        pt_batch_size: batch size of pretrained MVGRL. Defaults to 4.
        sparse: if sparse. Defaults to False.
        dataset: dataset name. Defaults to 'Citeseer'.
        device: device. Defaults to torch.device('cpu').
    """

    def __init__(
            self,
            in_feats,
            n_clusters,
            n_h: int = 512,
            nb_epochs: int = 1500,
            lr: float = 0.00005,
            alpha=0.0001,
            mask_num: int = 100,
            batch_size: int = 4,
            update_interval: int = 10,
            model_filename: str = "gdcl",
            beta: float = 10e-4,
            weight_decay: float = 0.0,
            pt_n_h: int = 512,
            pt_model_filename: str = "mvgrl",
            pt_nb_epochs: int = 3000,
            pt_patience: int = 20,
            pt_lr: float = 0.001,
            pt_weight_decay: float = 0.0,
            pt_sample_size: int = 2000,
            pt_batch_size: int = 4,
            sparse: bool = False,
            dataset: str = "Citeseer",
            device: torch.device = torch.device("cpu"),
    ):
        super().__init__()
        self.n_clusters = n_clusters
        self.nb_epochs = nb_epochs
        self.lr = lr
        self.sparse = sparse
        self.alpha = alpha
        self.pretrain_path = get_checkpoint_path(pt_model_filename)
        self.mask_num = mask_num
        self.dataset = dataset
        self.nb_epochs = nb_epochs
        self.batch_size = batch_size
        self.update_interval = update_interval
        self.model_filename = model_filename
        self.beta = beta
        self.weight_decay = weight_decay
        self.device = device
        self.adj = None
        self.diff = None
        self.features = None
        self.optimizer = None

        self.mvg = MVGRL(
            in_feats=in_feats,
            n_clusters=n_clusters,
            n_h=pt_n_h,
            model_filename=pt_model_filename,
            sparse=sparse,
            nb_epochs=pt_nb_epochs,
            patience=pt_patience,
            lr=pt_lr,
            weight_decay=pt_weight_decay,
            sample_size=pt_sample_size,
            batch_size=pt_batch_size,
            dataset=dataset,
        )
        # cluster layer
        self.cluster_layer = Parameter(torch.Tensor(n_clusters, n_h))
        torch.nn.init.xavier_normal_(self.cluster_layer.data)

    def pretrain(self, graph):
        """Fitting

        Args:
            graph (dgl.DGLGraph): graph.
        """
        print("pretrained MVGRL starting...")
        self.mvg.fit(adj_csr=graph.adj_external(scipy_fmt="csr"),
                     features=graph.ndata["feat"])
        print("pretrained MVGRL ending...")

    def embed(self, seq, adj, diff, sparse):
        """Embed.

        Args:
            seq (tensor.Tensor): features of raw graph
            adj (tensor.Tensor): adj matrix of raw graph
            diff (tensor.Tensor): ppr matrix of diffuse graph
            sparse (bool): if sparse

        Returns:
            (tensor.Tensor): node embedding
        """
        h_1 = self.mvg.gcn1(seq, adj, sparse)
        h = self.mvg.gcn2(seq, diff, sparse)
        return ((h + h_1)).detach()

    def forward(self, bf, mask_fts, bd, sparse):
        """Forward Propagation

        Args:
            bf (tensor.Tensor): features of raw graph
            mask_fts (tensor.Tensor): mask features
            bd (tensor.Tensor): ppr matrix of diffuse graph
            sparse (bool): if sparse

        Returns:
            h_mask (tensor.Tensor): node embedding of mask features graph
            h (tensor.Tensor): node embedding of raw graph
            q (tensor.Tensor): soft assignment
        """
        h_mask = self.mvg.gcn2(mask_fts, bd, sparse)[0].unsqueeze(0)
        h = self.mvg.gcn2(bf, bd, sparse)[0].unsqueeze(0)
        # cluster
        q = 1.0 / (
            1.0 + torch.sum(
                torch.pow(
                    h.reshape(-1, h.shape[2]).unsqueeze(1) -
                    self.cluster_layer, 2),
                2,
            ) / self.alpha
        )  # h.reshape(-1,h.shape[2]).unsqueeze(1)-self.cluster_layer
        q = q.pow((self.alpha + 1.0) / 2.0)
        q = (q.t() / torch.sum(q, 1)).t()
        return h_mask, h, q

    def fit(self, graph, labels):
        """Fitting

        Args:
            graph (dgl.DGLGraph): graph.
            labels (tensor.Tensor): labels of each node
        """
        adj_csr = graph.adj_external(scipy_fmt="csr")
        self.adj = adj_csr.toarray()
        self.diff = compute_ppr(self.adj, 0.2)
        self.features = graph.ndata["feat"].numpy()

        if self.dataset == "Citeseer":
            self.features = sp.lil_matrix(self.features)
            self.features = normalize_feature(self.features)

            epsilons = [1e-5, 1e-4, 1e-3, 1e-2]
            avg_degree = np.sum(self.adj) / self.adj.shape[0]
            epsilon = epsilons[np.argmin([
                abs(avg_degree -
                    np.argwhere(self.diff >= e).shape[0] / self.diff.shape[0])
                for e in epsilons
            ])]

            self.diff[self.diff < epsilon] = 0.0
            scaler = MinMaxScaler()
            scaler.fit(self.diff)
            self.diff = scaler.transform(self.diff)

        self.adj = symmetrically_normalize_adj(
            self.adj + sp.eye(self.adj.shape[0])).todense()

        ft_size = self.features.shape[1]
        sample_size = self.features.shape[0]

        labels = torch.LongTensor(labels)

        self.optimizer = torch.optim.Adam(self.parameters(),
                                          lr=self.lr,
                                          weight_decay=self.weight_decay)

        self.pretrain(graph)

        if self.sparse:
            self.adj = sparse_mx_to_torch_sparse_tensor(sp.coo_matrix(
                self.adj))
            self.diff = sparse_mx_to_torch_sparse_tensor(
                sp.coo_matrix(self.diff))

        features_array = self.features
        diff_array = self.diff

        self.features = torch.FloatTensor(self.features[np.newaxis])
        self.adj = torch.FloatTensor(self.adj[np.newaxis])
        self.diff = torch.FloatTensor(self.diff[np.newaxis])

        self.features = self.features.to(self.device)
        self.adj = self.adj.to(self.device)
        self.diff = self.diff.to(self.device)

        # obtain features of positive samples
        features_mask = self.features  # [1,n,d]

        for i in range(features_mask.shape[1]):
            idx = random.sample(range(1, features_mask.shape[2]),
                                self.mask_num)
            features_mask[0][i][idx] = 0  # feature random mask 0
        features_mask_array = np.array(features_mask.squeeze(0).cpu())

        # cluster parameter initiate
        h2 = self.mvg.gcn2(self.features, self.diff, self.sparse)
        kmeans = KMeans(n_clusters=self.n_clusters)
        y_pred = kmeans.fit_predict(h2.data.squeeze().cpu().numpy())
        self.cluster_layer.data = torch.tensor(kmeans.cluster_centers_).to(
            self.device)

        self.train()
        acc_clu = 0
        kl_loss = 0
        loss = 0

        for epoch in range(self.nb_epochs):
            idx = np.random.randint(0, self.adj.shape[-1] - sample_size + 1,
                                    self.batch_size)
            bd, bf, bf_mask = [], [], []
            for i in idx:
                bd.append(diff_array[i:i + sample_size, i:i + sample_size])
                bf.append(features_array[i:i + sample_size])
                bf_mask.append(features_mask_array[i:i + sample_size])
            bd = np.array(bd).reshape(self.batch_size, sample_size,
                                      sample_size)
            bf = np.array(bf).reshape(self.batch_size, sample_size, ft_size)
            bf_mask = np.array(bf_mask).reshape(self.batch_size, sample_size,
                                                ft_size)
            if self.sparse:
                bd = sparse_mx_to_torch_sparse_tensor(sp.coo_matrix(bd))
            else:
                bd = torch.FloatTensor(bd)
                bf = torch.FloatTensor(bf)
                bf_mask = torch.FloatTensor(bf_mask)

            bf = bf.to(self.device)
            bd = bd.to(self.device)
            bf_mask = bf_mask.to(self.device)

            if epoch % self.update_interval == 0:
                _, _, tmp_q = self.forward(bf, bf_mask, bd, self.sparse)
                # update target distribution p
                tmp_q = tmp_q.data
                p = target_distribution(tmp_q)

                # evaluate clustering performance
                y_pred = self.get_memberships()
                (
                    ARI_score,
                    NMI_score,
                    ACC_score,
                    _,
                    _,
                ) = evaluation(np.array(labels.cpu()), y_pred)
                print("ACC_score:", ACC_score)

            if ACC_score > acc_clu:
                acc_clu = ACC_score
                _ = NMI_score
                _ = ARI_score

                save_model(
                    self.model_filename,
                    self,
                    self.optimizer,
                    epoch,
                    loss.item() if loss != 0 else 0,
                )

            h_mask, h_2_sour, q = self.forward(bf, bf_mask, bd, self.sparse)

            kl_loss = F.kl_div(q.log(), p)

            temperature = 0.5
            y_sam = torch.LongTensor(y_pred)
            # --------------- compute pos sample results ---------------
            neg_size = 1000
            class_sam = []
            for m in range(np.max(y_pred) + 1):
                class_del = torch.ones(int(sample_size), dtype=bool)
                class_del[np.where(y_sam.cpu() == m)] = 0
                class_neg = torch.arange(sample_size).masked_select(class_del)
                # FIXME: Sample larger than population
                neg_sam_id = random.sample(
                    range(0, class_neg.shape[0]),
                    int(neg_size),
                )
                class_sam.append(class_neg[neg_sam_id])  # [n_class,neg_size]

            out = (h_2_sour).squeeze()  # shape: [sample_size,d]
            neg = torch.exp(torch.mm(out,
                                     out.t().contiguous()) /
                            temperature)  # shape: [sample_size,sample_size]
            neg_samp = torch.zeros(
                neg.shape[0], int(neg_size))  # shape: [sample_size,neg_size]
            for n in range(np.max(y_pred) + 1):
                neg_samp[np.where(y_sam.cpu() == n)] = neg.cpu().index_select(
                    1, class_sam[n])[np.where(y_sam.cpu() == n)]
            neg_samp = neg_samp.cuda()
            Ng = neg_samp.sum(dim=-1)

            # ---------------- compute pos sample results --------------
            pos_size = 10
            class_sam_pos = []
            for m in range(np.max(y_pred) + 1):
                class_del = torch.ones(int(sample_size), dtype=bool)
                class_del[np.where(y_sam.cpu() != m)] = 0
                class_pos = torch.arange(sample_size).masked_select(class_del)
                pos_sam_id = random.sample(
                    range(0, class_pos.shape[0]),
                    int(pos_size))  # BUG number of pos samples < pos_size
                class_sam_pos.append(
                    class_neg[pos_sam_id]
                )  # BUG why class_neg .... class_sam_pos shape:[pos_size,d]

            out = h_2_sour.squeeze()
            pos = torch.exp(torch.mm(out, out.t().contiguous()))
            pos_samp = torch.zeros(
                pos.shape[0], int(pos_size))  # shape:[sample_size,pos_size]
            for n in range(np.max(y_pred) + 1):
                pos_samp[np.where(y_sam.cpu() == n)] = pos.cpu().index_select(
                    1, class_sam_pos[n])[np.where(y_sam.cpu() == n)]

            pos_samp = pos_samp.cuda()
            pos = pos_samp.sum(dim=-1) + torch.diag(
                torch.exp(torch.mm(out, (h_mask.squeeze()).t().contiguous())))
            node_contra_loss_2 = (-torch.log(pos / (pos + Ng))).mean()

            loss = node_contra_loss_2 + self.beta * kl_loss
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def get_embedding(self):
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding of each node.
            (torch.Tensor): embedding of graph representations
        """
        h_2 = self.mvg.gcn2(self.features, self.diff, self.sparse)

        return h_2.detach()

    def get_memberships(self):
        """Get memberships

        Returns:
            np.ndarray: memberships
        """
        h = self.get_embedding()
        # cluster
        q = 1.0 / (
            1.0 + torch.sum(
                torch.pow(
                    h.reshape(-1, h.shape[2]).unsqueeze(1) -
                    self.cluster_layer, 2),
                2,
            ) / self.alpha
        )  # h.reshape(-1,h.shape[2]).unsqueeze(1)-self.cluster_layer
        q = q.pow((self.alpha + 1.0) / 2.0)
        q = (q.t() / torch.sum(q, 1)).t()
        y_pred = q.detach().cpu().numpy().argmax(1)
        return y_pred


def target_distribution(q):
    """get target distribution P

    Args:
        q (torch.Tensor): Soft assignments

    Returns:
        torch.Tensor: target distribution P
    """
    weight = q**2 / q.sum(0)
    return (weight.t() / weight.sum(1)).t()


# # for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils.evaluation import evaluation
#     from utils import set_device
#     from utils import set_seed
#     import scipy.sparse as sp
#     import time

#     set_seed(4096)
#     device = set_device('4')

#     graph, label, n_clusters = load_data(
#         dataset_name='Citeseer',
#         directory='./data',
#     )
#     print(graph)
#     features = graph.ndata["feat"]

#     start_time = time.time()
#     model = GDCL(
#         in_feats=features.shape[1],
#         n_clusters=n_clusters,
#         device=device
#     )
#     model.fit(graph=graph,labels=label)
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
