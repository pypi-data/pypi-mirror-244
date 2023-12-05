"""
Contrastive Multi-View Representation Learning on Graphs
https://arxiv.org/abs/2006.05582
"""
import numpy as np
import scipy.sparse as sp
import torch
from sklearn.preprocessing import MinMaxScaler
from torch import nn

from ...module import BATCH_GCN
from ...module import DiscMVGRL
from ...utils import compute_ppr
from ...utils import normalize_feature
from ...utils import save_model
from ...utils import sk_clustering
from ...utils import sparse_mx_to_torch_sparse_tensor
from ...utils import symmetrically_normalize_adj

# from utils import load_model


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


class MVGRL(nn.Module):
    """MVGRL:Contrastive Multi-View Representation Learning on Graphs

    Args:
        in_feats (int): Input feature size.
        n_clusters (int): Num of clusters.
        n_h (int,optional): hidden units dimension. Defaults to 256.
        model_filename (str,optional): Path to store model parameters. Defaults to 'mvgrl'.
        sparse (bool,optional): Use sparse tensor. Defaults to False.
        nb_epochs (int,optional): Maximum training epochs. Defaults to 3000.
        patience (int,optional): Early stopping patience. Defaults to 20.
        lr (float,optional): Learning rate. Defaults to 0.001.
        weight_decay (float,optional): Weight decay. Defaults to 0.0.
        sample_size (int,optional): Sample size. Defaults to 2000.
        batch_size (int,optional): Batch size. Defaults to 4.
        dataset (str,optional): Dataset. Defaults to 'Citeseer'.
    """

    def __init__(
        self,
        in_feats: int,
        n_clusters: int,
        n_h: int = 512,
        model_filename: str = "mvgrl",
        sparse: bool = False,
        nb_epochs: int = 3000,
        patience: int = 20,
        lr: float = 0.001,
        weight_decay: float = 0.0,
        sample_size: int = 2000,
        batch_size: int = 4,
        dataset: str = "Citeseer",
    ):
        super().__init__()
        self.n_clusters = n_clusters
        self.model_filename = model_filename
        self.sparse = sparse
        self.nb_epochs = nb_epochs
        self.patience = patience
        self.lr = lr
        self.weight_decay = weight_decay
        self.sample_size = sample_size
        self.batch_size = batch_size
        self.dataset = dataset
        self.adj = None
        self.diff = None
        self.features = None
        self.optimizer = None
        self.msk = None

        self.gcn1 = BATCH_GCN(in_feats, n_h)
        self.gcn2 = BATCH_GCN(in_feats, n_h)
        self.read = Readout()
        self.sigm = nn.Sigmoid()
        self.disc = DiscMVGRL(n_h)

    def forward(self, seq1, seq2, adj, diff, sparse, msk):
        """Forward Propagation

        Args:
            seq1 (torch.Tensor): features of raw graph
            seq2 (torch.Tensor): shuffle features of diffuse graph
            adj (torch.Tensor): adj matrix of raw graph
            diff (torch.Tensor): ppr matrix of diffuse graph
            sparse (bool): if sparse
            msk (torch.Tensor): mask node

        Returns:
            ret (torch.Tensor): probability of positive or negtive node
            h_1 (torch.Tensor): node embedding of raw graph by one gcn layer
            h_2 (torch.Tensor): node embedding of diffuse graph by one gcn layer
        """

        h_1 = self.gcn1(seq1, adj, sparse)
        c_1 = self.read(h_1, msk)
        c_1 = self.sigm(c_1)

        h_2 = self.gcn2(seq1, diff, sparse)
        c_2 = self.read(h_2, msk)
        c_2 = self.sigm(c_2)

        h_3 = self.gcn1(seq2, adj, sparse)
        h_4 = self.gcn2(seq2, diff, sparse)

        ret = self.disc(c_1, c_2, h_1, h_2, h_3, h_4)

        return ret, h_1, h_2

    def fit(self, adj_csr, features):
        """Fitting

        Args:
            adj_csr (sp.lil_matrix): adj sparse matrix.
            features (torch.Tensor): features.
        """
        # adj_csr = graph.adj_external(scipy_fmt='csr')
        self.adj = adj_csr.toarray()
        self.diff = compute_ppr(self.adj, 0.2)
        # self.features = graph.ndata["feat"].numpy()
        self.features = features.numpy()
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

        lbl_1 = torch.ones(self.batch_size, self.sample_size * 2)
        lbl_2 = torch.zeros(self.batch_size, self.sample_size * 2)
        lbl = torch.cat((lbl_1, lbl_2), 1)

        self.optimizer = torch.optim.Adam(self.parameters(),
                                          lr=self.lr,
                                          weight_decay=self.weight_decay)

        if torch.cuda.is_available():
            self.cuda()
            lbl = lbl.cuda()

        b_xent = nn.BCEWithLogitsLoss()
        cnt_wait = 0
        best = 1e9

        for epoch in range(self.nb_epochs):
            idx = np.random.randint(0,
                                    self.adj.shape[-1] - self.sample_size + 1,
                                    self.batch_size)
            ba, bd, bf = [], [], []
            for i in idx:
                ba.append(self.adj[i:i + self.sample_size,
                                   i:i + self.sample_size])
                bd.append(self.diff[i:i + self.sample_size,
                                    i:i + self.sample_size])
                bf.append(self.features[i:i + self.sample_size])

            ba = np.array(ba).reshape(self.batch_size, self.sample_size,
                                      self.sample_size)
            bd = np.array(bd).reshape(self.batch_size, self.sample_size,
                                      self.sample_size)
            bf = np.array(bf).reshape(self.batch_size, self.sample_size,
                                      ft_size)

            if self.sparse:
                ba = sparse_mx_to_torch_sparse_tensor(sp.coo_matrix(ba))
                bd = sparse_mx_to_torch_sparse_tensor(sp.coo_matrix(bd))
            else:
                ba = torch.FloatTensor(ba)
                bd = torch.FloatTensor(bd)

            bf = torch.FloatTensor(bf)
            idx = np.random.permutation(self.sample_size)
            shuf_fts = bf[:, idx, :]

            if torch.cuda.is_available():
                bf = bf.cuda()
                ba = ba.cuda()
                bd = bd.cuda()
                shuf_fts = shuf_fts.cuda()

            self.train()
            self.optimizer.zero_grad()

            logits, __, __ = self.forward(bf, shuf_fts, ba, bd, self.sparse,
                                          None)

            loss = b_xent(logits, lbl)

            loss.backward()
            self.optimizer.step()

            print(f"Epoch: {epoch}, Loss: {loss.item()}")

            if loss < best:
                best = loss
                cnt_wait = 0
                save_model(self.model_filename, self, self.optimizer, epoch,
                           loss.item())
                # torch.save(self.state_dict(), 'model.pkl')
            else:
                cnt_wait += 1

            if cnt_wait == self.patience:
                print("Early stopping!")
                break

    def get_embedding(self):
        """Get the embeddings (graph or node level).

        Returns:
            (torch.Tensor): embedding of each node.
            (torch.Tensor): embedding of graph representations
        """
        # model, _, _, _ = load_model(self.model_filename, self, self.optimizer)
        adj = torch.FloatTensor(self.adj[np.newaxis])
        diff = torch.FloatTensor(self.diff[np.newaxis])
        features = torch.FloatTensor(self.features[np.newaxis])
        adj = adj.cuda()
        diff = diff.cuda()
        features = features.cuda()
        h_1 = self.gcn1(features, adj, self.sparse)
        c = self.read(h_1, self.msk)
        h_2 = self.gcn2(features, diff, self.sparse)
        return (h_1 + h_2).detach(), c.detach()

    def get_memberships(self, ):
        """Get memberships

        Returns:
            np.ndarray: memberships
        """
        pred, _ = self.get_embedding()
        return sk_clustering(torch.squeeze(pred, 0).cpu(),
                             self.n_clusters,
                             name="kmeans")


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

#     dataset = 'ACM'
#     graph, label, n_clusters = load_data(
#         dataset_name=dataset,
#         directory='./data',
#     )
#     print(graph)
#     features = graph.ndata["feat"]

#     start_time = time.time()
#     model = MVGRL(in_feats=features.shape[1],
#                   n_clusters=n_clusters,
#                   n_h=512,
#                   lr=0.001,
#                   dataset=dataset)
#     model.fit(graph=graph)
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
#     labels_true, labels_pred = best_mapping(label.cpu().numpy(), res)
#     df_res = pd.DataFrame({'label':labels_true,'pred':labels_pred})
#     df_res.to_pickle(f'./tmp/MVGRL_{dataset}_pred.pkl')
#     print('write to',f'./tmp/MVGRL_{dataset}_pred.pkl')
