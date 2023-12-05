"""
    AGE Model
"""
import copy
import time

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn.functional as F
from sklearn.preprocessing import normalize
from torch import nn
from torch import optim


class AGE(nn.Module):
    """AGE paper:Adaptive Graph Encoder for Attributed Graph Embedding

    Args:
        dims (list,optional): Number of units in hidden layer 1.
        feat_dim (int,optional): input feature dimension.
        gnnlayers_num (int): Number of gnn layers
        linlayers_num (int, optional): Number of hidden layers
        lr (float, optional): learning rate.. Defaults to 0.001.
        upth_st (float, optional): Upper Threshold start.
        upth_ed (float, optional): Upper Threshold end.
        lowth_st (float, optional): Lower Threshold start.
        lowth_ed (float, optional): Lower Threshold end.
        upd (float, optional): Update epoch.
        bs (int,optional):Batchsize
        epochs (int,optional):Number of epochs to train.
        norm (str,optional):normalize mode of Laplacian matrix
        renorm (bool,optional):If with the renormalization trick
        estop_steps (int,optional):Number of early_stop steps.
    """

    def __init__(
        self,
        dims: list = None,
        feat_dim: int = None,
        gnnlayers_num: int = 3,
        linlayers_num: int = 1,
        lr: float = 0.001,
        upth_st: float = 0.0015,
        upth_ed: float = 0.001,
        lowth_st: float = 0.1,
        lowth_ed: float = 0.5,
        upd: float = 10,
        bs: int = 10000,
        epochs: int = 400,
        norm: str = "sym",
        renorm: bool = True,
        estop_steps: int = 5,
    ) -> None:
        super().__init__()
        # ------------- Parameters ----------------
        self.dims = [feat_dim] + dims
        self.gnnlayers_num = gnnlayers_num
        self.layers_num = linlayers_num
        self.lr = lr
        self.upth_st = upth_st
        self.upth_ed = upth_ed
        self.lowth_st = lowth_st
        self.lowth_ed = lowth_ed
        self.upd = upd
        self.bs = bs
        self.epochs = epochs
        self.norm = norm
        self.renorm = renorm
        self.estop_steps = estop_steps
        self.device = None
        self.sm_fea_s = None
        self.adj_label = None
        self.best_model = None

        # ---------------- Layer -------------------
        self.lintran = LinTrans(linlayers_num, self.dims)
        self.decoder = SampleDecoder(act=lambda x: x)

    def forward(self, x, y):
        """Forward Propagation

        Args:
            x (torch.Tensor):Sample node embedding for x-axis
            y (torch.Tensor): Sample node embedding for y-axis

        Returns:
            batch_pred (torch.Tensor):prediction of adj
        """
        zx = self.lintran(x)
        zy = self.lintran(y)
        batch_pred = self.decoder(zx, zy)

        return batch_pred

    def fit(self, adj: sp.csr_matrix, features: torch.Tensor) -> None:
        """Fitting a AGE model

        Args:
            adj (sp.csr_matrix): 2D sparse adj.
            features (torch.Tensor): features.
        """
        n_nodes, _ = features.shape

        adj = adj - sp.dia_matrix(
            (adj.diagonal()[np.newaxis, :], [0]), shape=adj.shape)
        adj.eliminate_zeros()

        n = adj.shape[0]

        adj_norm_s = preprocess_graph(adj,
                                      self.gnnlayers_num,
                                      norm=self.norm,
                                      renorm=self.renorm)
        sm_fea_s = sp.csr_matrix(features).toarray()

        print("Laplacian Smoothing...")
        for a in adj_norm_s:
            sm_fea_s = a.dot(sm_fea_s)
        adj_1st = (adj + sp.eye(n)).toarray()
        self.sm_fea_s = torch.FloatTensor(sm_fea_s)

        self.adj_label = torch.FloatTensor(adj_1st).reshape([
            -1,
        ])

        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            print(f"GPU available: AGE Embedding Using {self.device}")
            self.cuda()
            self.sm_fea_s = self.sm_fea_s.cuda()
            self.adj_label = self.adj_label.cuda()

        else:
            self.device = torch.device("cpu")

        pos_num = len(adj.indices)
        neg_num = n_nodes * n_nodes - pos_num

        up_eta = (self.upth_ed - self.upth_st) / (self.epochs / self.upd)
        low_eta = (self.lowth_ed - self.lowth_st) / (self.epochs / self.upd)

        pos_inds, neg_inds = update_similarity(
            normalize(self.sm_fea_s.data.cpu().numpy()),
            self.upth_st,
            self.lowth_st,
            pos_num,
            neg_num,
        )
        upth, lowth = update_threshold(self.upth_st, self.lowth_st, up_eta,
                                       low_eta)

        bs = min(self.bs, len(pos_inds))
        # length = len(pos_inds)
        pos_inds_cuda = torch.LongTensor(pos_inds).to(self.device)

        best_loss = 1e9
        cnt = 0
        best_epoch = 0
        optimizer = optim.Adam(self.parameters(), lr=self.lr)

        print("Start Training...")
        for epoch in range(self.epochs):
            st, ed = 0, bs
            batch_num = 0
            self.train()
            length = len(pos_inds)

            while ed <= length:
                sampled_neg = torch.LongTensor(
                    np.random.choice(neg_inds, size=ed - st)).to(self.device)
                sampled_inds = torch.cat((pos_inds_cuda[st:ed], sampled_neg),
                                         0)
                t = time.time()
                optimizer.zero_grad()
                xind = sampled_inds // n_nodes
                yind = sampled_inds % n_nodes
                x = torch.index_select(self.sm_fea_s, 0, xind)
                y = torch.index_select(self.sm_fea_s, 0, yind)

                batch_label = torch.cat(
                    (torch.ones(ed - st), torch.zeros(ed - st))).cuda()
                batch_pred = self.forward(x, y)
                loss = loss_function(adj_preds=batch_pred,
                                     adj_labels=batch_label)

                loss.backward()
                cur_loss = loss.item()
                optimizer.step()

                st = ed
                batch_num += 1
                if ed < length <= ed + bs:
                    ed += length - ed
                else:
                    ed += bs

            if (epoch + 1) % self.upd == 0:
                self.eval()
                mu = self.lintran(self.sm_fea_s)
                hidden_emb = mu.cpu().data.numpy()
                upth, lowth = update_threshold(upth, lowth, up_eta, low_eta)
                pos_inds, neg_inds = update_similarity(hidden_emb, upth, lowth,
                                                       pos_num, neg_num)
                bs = min(self.bs, len(pos_inds))
                pos_inds_cuda = torch.LongTensor(pos_inds).cuda()

            print(
                f"Epoch: {epoch}, train_loss_gae={cur_loss:.5f}, time={time.time() - t:.5f}"
            )

            if cur_loss < best_loss:
                cnt = 0
                best_epoch = epoch
                best_loss = cur_loss
                del self.best_model
                self.best_model = copy.deepcopy(self.to(self.device))
                # self.embedding = mu.data.cpu().numpy()
                # self.memberships = kmeans.labels_
            else:
                cnt += 1
                print(f"loss increase count:{cnt}")
                if cnt >= self.estop_steps:
                    print(f"early stopping,best epoch:{best_epoch}")
                    break

        print("Optimization Finished!")

    def get_embedding(self):
        """Get cluster embedding.

        Returns:tensor.Tensor
        """
        mu = self.best_model.lintran(self.sm_fea_s)
        return mu.detach()


class LinTrans(nn.Module):
    """Linear Transform Model

    Args:
        layers (int):number of linear layers.
        dims (list):Number of units in hidden layers.
    """

    def __init__(self, layers, dims):
        super().__init__()
        self.layers = nn.ModuleList()
        # print('layers',layers)
        for i in range(layers):
            self.layers.append(nn.Linear(dims[i], dims[i + 1]))

    def forward(self, x):
        """Forward Propagation

        Args:
            x (torch.Tensor):feature embedding

        Returns:
            out (torch.Tensor):hiddin embedding
        """
        out = x
        for layer in self.layers:
            out = layer(out)
        out = scale(out)
        out = F.normalize(out)
        return out


class SampleDecoder(nn.Module):
    """Decoder Model , inner dot

    Args:
        activation (object, optional): activation of Decoder.
    """

    def __init__(self, act=torch.sigmoid):
        super().__init__()
        self.act = act

    def forward(self, zx, zy):
        """Forward Propagation

        Args:
            zx (torch.Tensor):Sample node embedding for x-axis
            zy (torch.Tensor): Sample node embedding for y-axis

        Returns:
            sim (torch.Tensor):prediction of adj
        """
        sim = (zx * zy).sum(1)
        sim = self.act(sim)

        return sim


def loss_function(adj_preds, adj_labels):
    """compute loss

    Args:
        adj_preds (torch.Tensor):reconstructed adj

    Returns:
        torch.Tensor: loss
    """

    cost = 0.0
    cost += F.binary_cross_entropy_with_logits(adj_preds, adj_labels)

    return cost


def update_similarity(z, upper_threshold, lower_treshold, pos_num, neg_num):
    """update similarity

    Args:
        z (numpy.ndarray):hidden embedding
        upper_threshold (float): upper threshold
        lower_treshold (float):lower treshold
        pos_num (int):number of positive samples
        neg_num (int):number of negative samples

    Returns:
        numpy.ndarray: list of positive indexs
        numpy.ndarray: list of negative indexs
    """
    f_adj = np.matmul(z, np.transpose(z))
    cosine = f_adj
    cosine = cosine.reshape([
        -1,
    ])
    pos_num = round(upper_threshold * len(cosine))
    neg_num = round((1 - lower_treshold) * len(cosine))

    pos_inds = np.argpartition(-cosine, pos_num)[:pos_num]
    neg_inds = np.argpartition(cosine, neg_num)[:neg_num]

    return np.array(pos_inds), np.array(neg_inds)


def update_threshold(upper_threshold, lower_treshold, up_eta, low_eta):
    """update threshold

    Args:
        upper_threshold (float): upper threshold
        lower_treshold (float):lower treshold
        up_eta (float):update step size of upper threshold
        low_eta (float):update step size of lower threshold

    Returns:
        upth (float): updated upth
        lowth (float): updated lowth
    """
    upth = upper_threshold + up_eta
    lowth = lower_treshold + low_eta
    return upth, lowth


def preprocess_graph(adj: sp.csr_matrix,
                     layer: int,
                     norm: str = "sym",
                     renorm: bool = True) -> torch.Tensor:
    """Generalized Laplacian Smoothing Filter

    Args:
        adj (sp.csr_matrix): 2D sparse adj.
        layer (int):numbers of linear layers
        norm (str):normalize mode of Laplacian matrix
        renorm (bool): If with the renormalization trick

    Returns:
        adjs (sp.csr_matrix):Laplacian Smoothing Filter
    """
    adj = sp.coo_matrix(adj)
    ident = sp.eye(adj.shape[0])
    if renorm:
        adj_ = adj + ident
    else:
        adj_ = adj

    rowsum = np.array(adj_.sum(1))

    if norm == "sym":
        degree_mat_inv_sqrt = sp.diags(np.power(rowsum, -0.5).flatten())
        adj_normalized = (adj_.dot(degree_mat_inv_sqrt).transpose().dot(
            degree_mat_inv_sqrt).tocoo())
        laplacian = ident - adj_normalized
    elif norm == "left":
        degree_mat_inv_sqrt = sp.diags(np.power(rowsum, -1.0).flatten())
        adj_normalized = degree_mat_inv_sqrt.dot(adj_).tocoo()
        laplacian = ident - adj_normalized

    reg = [2 / 3] * (layer)

    adjs = []
    for i in reg:
        adjs.append(ident - (i * laplacian))
    return adjs


def scale(z):
    """Feature Scale
    Args:
        z (torch.Tensor):hidden embedding

    Returns:
        z_scaled (torch.Tensor):scaled embedding
    """
    zmax = z.max(dim=1, keepdim=True)[0]
    zmin = z.min(dim=1, keepdim=True)[0]
    z_std = (z - zmin) / (zmax - zmin)
    z_scaled = z_std

    return z_scaled
