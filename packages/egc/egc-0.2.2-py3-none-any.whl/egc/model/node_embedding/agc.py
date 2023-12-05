"""
AGC Embedding
"""
import scipy.sparse as sp
import torch
from sklearn.cluster import KMeans
from torch import nn

from ...utils.evaluation import evaluation


class AGCEmbed(nn.Module):
    """
    AGC Embedding
    """

    def __init__(
        self,
        adj: torch.sparse.Tensor,
        feature: torch.Tensor,
        labels: torch.Tensor,
        epochs: int = 60,
        n_clusters: int = 7,
        rep: int = 10,
    ):
        super().__init__()
        self.A = adj
        self.feature = feature
        self.labels = labels
        self.epochs = epochs
        self.D = torch.sum(adj.to_dense(), 1)
        self.n_clusters = n_clusters
        self.rep = rep
        self.best_feature = None

    def forward(self):
        pass

    def fit(self):
        if torch.cuda.is_available():
            self.A = self.A.cuda()
            self.feature = self.feature.cuda()
            self.labels = self.labels.cuda()
            self.D = self.D.cuda()

        tt = 0
        adj_normalized = self.normalize_adj()
        intra_list = [10000]
        feature = self.feature
        while tt <= self.epochs:
            tt = tt + 1
            power = tt
            intraD = torch.zeros(self.rep)

            ac = torch.zeros(self.rep)
            nm = torch.zeros(self.rep)
            f1 = torch.zeros(self.rep)

            feature = torch.mm(adj_normalized, feature)

            u, _, _ = sp.linalg.svds(feature.cpu().numpy(),
                                     k=self.n_clusters,
                                     which="LM")

            for i in range(self.rep):
                kmeans = KMeans(n_clusters=self.n_clusters).fit(u)
                predict_labels = kmeans.predict(u)
                predict_labels_tensor = torch.IntTensor(predict_labels)
                if torch.cuda.is_available():
                    predict_labels_tensor = predict_labels_tensor.cuda()
                intraD[i] = self.square_dist(predict_labels_tensor, feature)
                _, NMI_score, ACC_score, Micro_F1_score, _ = evaluation(
                    self.labels.cpu().numpy(), predict_labels)
                ac[i], nm[i], f1[i] = ACC_score, NMI_score, Micro_F1_score
                print(f"ACC_score: {ACC_score} , NMI_score: {NMI_score}, "
                      f"Micro_F1_score: {Micro_F1_score}")

            intramean = torch.mean(intraD)
            acc_means = torch.mean(ac)
            nmi_means = torch.mean(nm)
            f1_means = torch.mean(f1)

            intra_list.append(intramean)

            print(
                f"power:{power},intra_dist:{intramean}, acc_mean:{acc_means},"
                f"nmi_mean:{nmi_means},f1_mean:{f1_means}")
            if intra_list[tt] > intra_list[tt - 1]:
                print(f"bestpower: {tt - 1}")
                break
            self.best_feature = feature

    def normalize_adj(self):
        In = torch.eye(self.A.shape[0])
        if torch.cuda.is_available():
            In = In.cuda()
        A_prime = In + self.A.to_dense()
        D_prime = self.D + 1
        D_inv = torch.diag(torch.pow(D_prime, -0.5))
        conv_operator = (torch.mm(torch.mm(D_inv, A_prime), D_inv) + In) / 2
        return conv_operator

    def to_onehot(self, prelabel):
        label = torch.zeros([prelabel.shape[0], self.n_clusters])
        for i, v in enumerate(prelabel):
            label[i, v.item()] = 1
        label = label.T
        return label

    def square_dist(self, prelabel, feature):
        onehot = self.to_onehot(prelabel)
        if torch.cuda.is_available():
            onehot = onehot.cuda()
        m, _ = onehot.shape
        count = onehot.sum(1).reshape(m, 1)
        count[count == 0] = 1

        mean = torch.mm(onehot, feature) / count
        a2 = (torch.mm(onehot, feature * feature) / count).sum(1)
        pdist2 = a2 + a2.T - 2 * torch.mm(mean, mean.T)

        intra_dist = torch.trace(pdist2)
        inter_dist = pdist2.sum() - intra_dist
        intra_dist /= m
        inter_dist /= m * (m - 1)
        return intra_dist

    def get_embedding(self):
        u, _, _ = sp.linalg.svds(
            self.best_feature.cpu().numpy(),
            k=self.n_clusters,
            which="LM",
        )
        return torch.FloatTensor(u.copy())
