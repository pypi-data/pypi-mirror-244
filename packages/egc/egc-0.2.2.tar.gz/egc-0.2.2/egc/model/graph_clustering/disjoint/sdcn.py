"""
SDCN implement
"""
import dgl
import dgl.nn.pytorch as dglnn
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.cluster import KMeans
from torch import nn
from torch.nn.parameter import Parameter
from torch.optim import Adam
from torch.utils.data import DataLoader

from ....utils.evaluation import evaluation
from ....utils.load_data import AE_LoadDataset
from ...node_embedding.ae import AE

# from torch.nn import Linear
# from utils.load_data import load_data
# import utils.construct_DGLgraph as GetGraph
# from tensorboardX import SummaryWriter
# writer = SummaryWriter(r'D:\pyprogram\view\sdcn\cite\example4')


class SDCN(nn.Module):
    """
    SDCN
    """

    # pylint: disable=unused-argument
    def __init__(
        self,
        graph: dgl.DGLGraph,
        X: torch.FloatTensor,
        labels: torch.IntTensor,
        n_input,
        n_clusters,
        hidden1: int = 500,
        hidden2: int = 500,
        hidden3: int = 200,
        lr: float = 0.0001,
        epochs: int = 200,
        pretrain_lr: float = 0.0005,
        pretrain_epochs: int = 100,
        n_z: int = 10,
        v: int = 1,
        gpu: int = 0,
    ):  # v:degrees of freedom of the student t-distribution
        super().__init__()
        # autoencoder for intra information

        self.ae = AE(
            n_input=n_input,
            n_clusters=n_clusters,
            hidden1=hidden1,
            hidden2=hidden2,
            hidden3=hidden3,
            hidden4=hidden3,
            hidden5=hidden2,
            hidden6=hidden1,
            lr=pretrain_lr,
            epochs=pretrain_epochs,
            n_z=n_z,
            activation="relu",
            early_stop=10,
            if_eva=False,
            if_early_stop=False,
        )
        X[(X - 0.0) > 0.001] = 1.0
        dataset = AE_LoadDataset(X)
        train_loader = DataLoader(dataset,
                                  drop_last=False,
                                  batch_size=1024,
                                  shuffle=True)
        self.ae.fit(X, train_loader, labels)

        # self.ae.load_state_dict(torch.load('ae.pkl'))
        self.dropout = nn.Dropout(p=0.5)

        self.gcn_1 = dglnn.GraphConv(n_input,
                                     hidden1,
                                     activation=F.relu,
                                     bias=False)  # Z1
        self.gcn_2 = dglnn.GraphConv(hidden1,
                                     hidden2,
                                     activation=F.relu,
                                     bias=False)  # Z2
        self.gcn_3 = dglnn.GraphConv(hidden2,
                                     hidden3,
                                     activation=F.relu,
                                     bias=False)  # Z3
        self.gcn_4 = dglnn.GraphConv(hidden3,
                                     n_z,
                                     activation=F.relu,
                                     bias=False)  # Z4
        self.gcn_5 = dglnn.GraphConv(
            n_z, n_clusters, bias=False
        )  # the fifth is used for classification,Z = softmax(D^-0.5A'D^-0.5Z(L)W(L))

        # cluster layer
        self.cluster_layer = Parameter(torch.Tensor(n_clusters, n_z))
        torch.nn.init.xavier_normal_(self.cluster_layer.data)

        # degree
        self.v = v  # q分布自由度

        self.n_clusters = n_clusters
        self.lr = lr
        self.epochs = epochs
        self.labels = labels

        self.features = X
        self.graph = graph
        self.gpu = gpu
        self.best_feature = None

    def forward(self, graph, x):
        """Calculate the distribution of p,q and z

        Args:
            graph (dgl.DGLgraph): graph
            x (torch.FloatTensor): node features

        Returns:
            x_bar (torch.FloatTensor): node features after AE reconstruction
            q (torch.FloatTensor): q-distribution
            predict (torch.FloatTensor): z-distribution, label predict
            p (torch.FloatTensor): p-distribution
        """
        x_bar, z, tra1, tra2, tra3 = self.ae.forward(x)  # x_bar,h1,h2,h3 z为h4

        sigma = 0.5

        # GCN Module
        h = self.gcn_1(graph, x)  # Z1
        h = self.dropout(h)
        h = self.gcn_2(graph, (1 - sigma) * h + sigma * tra1)  # Z2
        h = self.dropout(h)
        h = self.gcn_3(graph, (1 - sigma) * h + sigma * tra2)  # Z3
        h = self.dropout(h)
        h = self.gcn_4(graph, (1 - sigma) * h + sigma * tra3)  # Z4
        h = self.dropout(h)
        h = self.gcn_5(graph, (1 - sigma) * h +
                       sigma * z)  # Z = softmax(D^-0.5A'D^-0.5Z(L)W(L))，分类结果
        predict = F.softmax(h, dim=1)

        # Dual Self-supervised Module
        q = 1.0 / (1.0 + torch.sum(
            torch.pow(z.unsqueeze(1) - self.cluster_layer, 2), 2) / self.v
                   )  # qij = 1/(1 + ||hi - uj||.pow(2)/v)
        q = q.pow((self.v + 1.0) /
                  2.0)  # qij = (1  + ||hi - uj||.pow(2)/v).pow((v+1)/2)
        q = (q.t() / torch.sum(q, 1)).t(
        )  # Get q-distribution，equal to q = q / torch.sum(q,1).unsqueeze(-1)

        q_data = q.data
        weight = q_data**2 / q_data.sum(
            0)  # qij^2/fj calculate the numerator of p-distribution
        p = (weight.t() / weight.sum(1)).t(
        )  # calculate p-distribution，equal to weight = weight / torch.sum(weight,1).unsequeeze(-1)

        return x_bar, q, predict, p
        # return x_bar(Features after AE reconstruction),
        #       q-distribution, z-distribution, p-distribution

    def init_cluster_layer_parameter(self, features, n_init):
        """Initialize the cluster center

        Args:
            features (torch.FloatTensor): node feature
            n_init (int): Number of kmeans iterations


        """
        with torch.no_grad():
            self.ae.eval()
            _, z, _, _, _ = self.ae.forward(features)
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=n_init)
        kmeans.fit_predict(
            z.data.cpu().numpy()
        )  # µj is initialized by K-means on representations （learned by pre-train autoencoder）

        self.cluster_layer.data = torch.Tensor(kmeans.cluster_centers_)
        if torch.cuda.is_available():
            self.cluster_layer.data = self.cluster_layer.data.cuda()

    def fit(self):
        """Train model

        Returns:
            label_predict (ndarray): the result of model predict
        """
        print(
            "------------------------------------Train SDCN------------------------------------"
        )
        # Process data
        features = self.features.to(torch.float32)
        if torch.cuda.is_available():
            self.cuda()
            features = features.cuda()
        labels = np.array(self.labels.to(torch.int32))
        # graph = GetGraph.construct_DGLgraph_for_graph(self.features,labels,self.graph.edges())

        # add self loop
        self.graph = dgl.remove_self_loop(self.graph)
        self.graph = dgl.add_self_loop(self.graph)
        self.graph.ndata["feat"] = self.features

        # Initialize parameters of classification layer
        self.init_cluster_layer_parameter(features, 20)

        # Train model
        optimizer = Adam(self.parameters(), lr=self.lr)
        for epoch in range(self.epochs):
            self.train(mode=True)
            x_bar, q, pred, p = self.forward(
                self.graph.to("cuda:" + str(self.gpu))
                if torch.cuda.is_available() else self.graph,
                features,
            )

            q_pred = q.data.cpu().numpy().argmax(
                1)  # Get cluster result by Q-distribution
            z_pred = pred.data.cpu().numpy().argmax(
                1)  # Get cluster result by Z-distribution
            p_pred = p.data.cpu().numpy().argmax(
                1)  # Get cluster result by P-distribution

            _, _, Q_ACC, _, _ = evaluation(labels, q_pred)
            (
                Z_ARI_score,
                Z_NMI_score,
                Z_ACC_score,
                Z_Micro_F1_score,
                Z_Macro_F2_score,
            ) = evaluation(labels, z_pred)
            _, _, P_ACC, _, _ = evaluation(labels, p_pred)

            kl_loss = F.kl_div(q.log(), p, reduction="batchmean")
            ce_loss = F.kl_div(pred.log(), p, reduction="batchmean")
            re_loss = F.mse_loss(x_bar, features)
            loss = 0.1 * kl_loss + 0.01 * ce_loss + re_loss

            print(f"epoch:{epoch} "
                  f"loss:{loss.item():.4f} "
                  f"ARI:{Z_ARI_score:.4f} "
                  f"NMI:{Z_NMI_score:.4f} "
                  f"ACC:{Z_ACC_score:.4f} "
                  f"Micro F1:{Z_Micro_F1_score:.4f} "
                  f"Macro F2:{Z_Macro_F2_score:.4f} "
                  f"P_ACC:{P_ACC:.4f} "
                  f"Q_ACC:{Q_ACC:.4f}")
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        self.best_feature = features

    def get_memberships(self):
        """Get predicted label

        Args:
            graph (dgl.DGLGraph): graph
            features (torch.FloatTensor): node features

        Returns:

        """
        z = self.get_embedding()
        label_pred = z.data.cpu().numpy().argmax(1)
        return label_pred

    def get_embedding(self):
        """
        Get Embedding
        Returns:
            torch.Tensor
        """
        g = self.graph.to(
            "cuda:" +
            str(self.gpu)) if torch.cuda.is_available() else self.graph
        _, _, z, _ = self.forward(g, self.best_feature)
        return z.detach().cpu()
