"""
Load dataset with DGL for Graph Clustering
Author: Sheng Zhou
"""
import os
import ssl
import sys
from typing import Tuple

import dgl
import numpy as np
import scipy.io as sio
import torch
import wget
from ogb.nodeproppred import DglNodePropPredDataset
from torch.utils.data import Dataset

ogb_datasets = ["products", "arxiv", "mag", "proteins"]
dgl_datasets = ["Cora", "Citeseer", "Pubmed", "CoraFull", "Reddit"]
other_datasets = ["BlogCatalog", "Flickr", "ACM", "DBLP"]

DEFAULT_DATA_DIR = "./data"

BASE_CoLA_LAB = "https://github.com/GRAND-Lab/CoLA/blob/main"
BLOGCATALOG_URL = f"{BASE_CoLA_LAB}/raw_dataset/BlogCatalog/BlogCatalog.mat?raw=true"
FLICKR_URL = f"{BASE_CoLA_LAB}/raw_dataset/Flickr/Flickr.mat?raw=true"
SDCN_URL = "https://github.com/bdy9527/SDCN/blob/da6bb007b7/"


def load_data(
    dataset_name: str,
    directory=DEFAULT_DATA_DIR,
) -> Tuple[dgl.DGLGraph, torch.Tensor, int]:
    """Load datasets.

    Args:
        dataset_name (str): Name of the dataset. Check README.md for supported datasets.
        directory (str, optional): path for the dataset to save. Defaults to './data'.

    Raises:
        NotImplementedError: dataset not supported

    Returns:
        Tuple[dgl.DGLGraph, torch.Tensor, int]: graph, label, n_clusters
    """

    if dataset_name in ogb_datasets:
        graph, label, n_clusters = load_ogb_data(dataset_name, directory)
    elif dataset_name in dgl_datasets:
        graph, label, n_clusters = load_dgl_data(dataset_name, directory)
    elif dataset_name in other_datasets:
        # pylint: disable=protected-access
        ssl._create_default_https_context = ssl._create_unverified_context
        # `python -m` may fail to download datasets in other_datasets_map
        graph, label, n_clusters = other_datasets_map[dataset_name](directory)
    else:
        raise NotImplementedError
    return graph, label, n_clusters


def load_ogb_data(dataset_name, directory=DEFAULT_DATA_DIR):
    """
    graph:DGL graph ob+ject
    label: torch tensor of shape (num_nodes,num_tasks)
    """
    dataset = DglNodePropPredDataset(
        name="ogbn-" + dataset_name,
        root=directory,
    )
    graph, label = dataset[0]

    print(f"\n  NumNodes: {graph.num_nodes()}\n"
          f"  NumEdges: {graph.num_edges()}\n"
          f"  NumFeats: {graph.ndata['feat'].shape[1]}\n"
          f"  NumClasses: {dataset.num_classes}\n")

    return graph, label, dataset.num_classes


def load_dgl_data(dataset_name, directory=DEFAULT_DATA_DIR):
    """
    graph:DGL graph object
    label: form graph.ndata['label']
    """
    print("\n")
    if dataset_name not in ("Reddit", "CoraFull"):
        dataset = getattr(
            dgl.data,
            dataset_name + "GraphDataset",
        )(raw_dir=directory)
    else:
        dataset = getattr(
            dgl.data,
            dataset_name + "Dataset",
        )(raw_dir=directory)

        print(f"  NumNodes: {dataset[0].num_nodes()}\n"
              f"  NumEdges: {dataset[0].num_edges()}\n"
              f"  NumFeats: {dataset[0].ndata['feat'].shape[1]}\n"
              f"  NumClasses: {dataset.num_classes}")

    print("\n")

    graph = dataset[0]
    label = graph.ndata["label"]
    return graph, label, dataset.num_classes


def allclose(
    a: torch.Tensor,
    b: torch.Tensor,
    rtol: float = 1e-4,
    atol: float = 1e-4,
) -> bool:
    """This function checks if a and b satisfy the condition:
    \|a - b\| <= atol + rtol * \|b\|

    Args:
        a (torch.Tensor): first tensor to compare
        b (torch.Tensor): second tensor to compare
        rtol (float, optional): relative tolerance. Defaults to 1e-4.
        atol (float, optional): absolute tolerance. Defaults to 1e-4.

    Returns:
        bool: True for close, False for not
    """
    return torch.allclose(
        a.float().cpu(),
        b.float().cpu(),
        rtol=rtol,
        atol=atol,
    )


def is_bidirected(g: dgl.DGLGraph) -> bool:
    """Return whether the graph is a bidirected graph.
    A graph is bidirected if for any edge :math:`(u, v)` in :math:`G` with weight :math:`w`,
    there exists an edge :math:`(v, u)` in :math:`G` with the same weight.

    Args:
        g (dgl.DGLGraph): dgl.DGLGraph

    Returns:
        bool: True for bidirected, False for not
    """
    src, dst = g.edges()
    num_nodes = g.num_nodes()

    # Sort first by src then dst
    idx_src_dst = src * num_nodes + dst
    perm_src_dst = torch.argsort(idx_src_dst, dim=0, descending=False)
    src1, dst1 = src[perm_src_dst], dst[perm_src_dst]

    # Sort first by dst then src
    idx_dst_src = dst * num_nodes + src
    perm_dst_src = torch.argsort(idx_dst_src, dim=0, descending=False)
    src2, dst2 = src[perm_dst_src], dst[perm_dst_src]

    return allclose(src1, dst2) and allclose(src2, dst1)


class AE_LoadDataset(Dataset):
    """AE_LoadDataset"""

    def __init__(self, data):
        super().__init__()
        self.x = data

    def __len__(self):
        return self.x.shape[0]

    def __getitem__(self, idx):
        return torch.from_numpy(np.array(
            self.x[idx])).float(), torch.from_numpy(np.array(idx))


def load_mat_data2dgl(data_path, verbose=True):
    """
    load data from .mat file

    Args:
        data_path (str): the file to read in
        verbose (bool, optional): print info, by default True

    Returns:
        graph (DGL.graph): the graph read from data_path
        (torch.Tensor): label of node classes
        num_classes (int): number of node classes
    """
    mat_path = data_path
    data_mat = sio.loadmat(mat_path)
    adj = data_mat["Network"]
    feat = data_mat["Attributes"]
    # feat = preprocessing.normalize(feat, axis=0)
    labels = data_mat["Label"]
    labels = labels.flatten()
    graph = dgl.from_scipy(adj)
    graph.ndata["feat"] = torch.from_numpy(feat.toarray()).to(torch.float32)
    graph.ndata["label"] = torch.from_numpy(labels).to(torch.int64)
    num_classes = len(np.unique(labels))

    if verbose:
        print()
        print("  DGL dataset")
        print(f"  NumNodes: {graph.number_of_nodes()}")
        print(f"  NumEdges: {graph.number_of_edges()}")
        print(f"  NumFeats: {graph.ndata['feat'].shape[1]}")
        print(f"  NumClasses: {num_classes}")

    return graph, graph.ndata["label"], num_classes


def bar_progress(current, total, _):
    """create this bar_progress method which is invoked automatically from wget"""
    progress_message = f"Downloading: {current / total * 100}% [{current} / {total}] bytes"
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def load_BlogCatalog(raw_dir=DEFAULT_DATA_DIR):
    """
    load BlogCatalog dgl graph

    Args:
        raw_dir (str): Data path. Supports user customization.

    Returns:
        graph (DGL.graph): the graph read from data_path
        (torch.Tensor): label of node classes
        num_classes (int): number of node classes

    Examples:
        >>> graph, label, n_clusters = load_BlogCatalog()
    """

    data_file = os.path.join(raw_dir, "BlogCatalog.mat")
    if not os.path.exists(data_file):
        url = BLOGCATALOG_URL
        wget.download(url, out=data_file, bar=bar_progress)

    return load_mat_data2dgl(data_path=data_file)


def load_Flickr(raw_dir=DEFAULT_DATA_DIR):
    """
    load Flickr dgl graph

    Args:
        raw_dir (str): Data path. Supports user customization.

    Returns:
        graph (DGL.graph): the graph read from data_path
        (torch.Tensor): label of node classes
        num_classes (int): number of node classes

    Examples:
        >>> graph, label, n_clusters = load_Flickr()
    """
    data_file = os.path.join(raw_dir, "Flickr.mat")
    if not os.path.exists(data_file):
        url = FLICKR_URL
        wget.download(url, out=data_file, bar=bar_progress)

    return load_mat_data2dgl(data_path=data_file)


def load_ACM(raw_dir=DEFAULT_DATA_DIR, verbose=True):
    """
    load ACM dgl graph

    Args:
        raw_dir (str): Data path. Supports user customization.
        verbose (bool, optional): print info, by default True

    Returns:
        graph (DGL.graph): the graph read from data_path
        (torch.Tensor): label of node classes
        num_classes (int): number of node classes

    Examples:
        >>> graph, label, n_clusters = load_ACM()
    """
    if not os.path.exists(os.path.join(raw_dir, "acm")):
        os.mkdir(os.path.join(raw_dir, "acm"))

    adj_data_file = os.path.join(raw_dir, "acm", "adj.txt")
    if not os.path.exists(adj_data_file):
        url = SDCN_URL + "graph/acm_graph.txt?raw=true"
        wget.download(url, out=adj_data_file, bar=bar_progress)

    feat_data_file = os.path.join(raw_dir, "acm", "feat.txt")
    if not os.path.exists(feat_data_file):
        url = SDCN_URL + "data/acm.txt?raw=true"
        wget.download(url, out=feat_data_file, bar=bar_progress)

    label_data_file = os.path.join(raw_dir, "acm", "label.txt")
    if not os.path.exists(label_data_file):
        url = SDCN_URL + "data/acm_label.txt?raw=true"
        wget.download(url, out=label_data_file, bar=bar_progress)

    edges_unordered = np.genfromtxt(adj_data_file, dtype=np.int32)
    graph = dgl.graph((edges_unordered[:, 0], edges_unordered[:, 1]))
    feat = np.loadtxt(feat_data_file, dtype=float)
    labels = np.loadtxt(label_data_file, dtype=int)
    graph.ndata["feat"] = torch.from_numpy(feat).to(torch.float32)
    graph.ndata["label"] = torch.from_numpy(labels).to(torch.int64)
    num_classes = len(np.unique(labels))

    if verbose:
        print()
        print("  DGL dataset")
        print(f"  NumNodes: {graph.number_of_nodes()}")
        print(f"  NumEdges: {graph.number_of_edges()}")
        print(f"  NumFeats: {graph.ndata['feat'].shape[1]}")
        print(f"  NumClasses: {num_classes}")

    return graph, graph.ndata["label"], num_classes


def load_DBLP(raw_dir=DEFAULT_DATA_DIR, verbose=True):
    """
    load DBLP dgl graph

    Args:
        raw_dir (str): Data path. Supports user customization.
        verbose (bool, optional): print info, by default True

    Returns:
        graph (DGL.graph): the graph read from data_path
        (torch.Tensor): label of node classes
        num_classes (int): number of node classes

    Examples:
        >>> graph, label, n_clusters = load_DBLP()
    """
    if not os.path.exists(os.path.join(raw_dir, "dblp")):
        os.mkdir(os.path.join(raw_dir, "dblp"))

    adj_data_file = os.path.join(raw_dir, "dblp", "adj.txt")
    if not os.path.exists(adj_data_file):
        url = SDCN_URL + "graph/dblp_graph.txt?raw=true"
        wget.download(url, out=adj_data_file, bar=bar_progress)

    feat_data_file = os.path.join(raw_dir, "dblp", "feat.txt")
    if not os.path.exists(feat_data_file):
        url = SDCN_URL + "data/dblp.txt?raw=true"
        wget.download(url, out=feat_data_file, bar=bar_progress)

    label_data_file = os.path.join(raw_dir, "dblp", "label.txt")
    if not os.path.exists(label_data_file):
        url = SDCN_URL + "data/dblp_label.txt?raw=true"
        wget.download(url, out=label_data_file, bar=bar_progress)

    edges_unordered = np.genfromtxt(adj_data_file, dtype=np.int32)
    graph = dgl.graph((edges_unordered[:, 0], edges_unordered[:, 1]))
    print(graph)
    feat = np.loadtxt(feat_data_file, dtype=float)
    labels = np.loadtxt(label_data_file, dtype=int)
    graph.ndata["feat"] = torch.from_numpy(feat).to(torch.float32)
    graph.ndata["label"] = torch.from_numpy(labels).to(torch.int64)
    num_classes = len(np.unique(labels))

    if verbose:
        print()
        print("  DGL dataset")
        print(f"  NumNodes: {graph.number_of_nodes()}")
        print(f"  NumEdges: {graph.number_of_edges()}")
        print(f"  NumFeats: {graph.ndata['feat'].shape[1]}")
        print(f"  NumClasses: {num_classes}")

    return graph, graph.ndata["label"], num_classes


other_datasets_map = {
    "ACM": load_ACM,
    "Flickr": load_Flickr,
    "BlogCatalog": load_BlogCatalog,
    "DBLP": load_DBLP,
}

# # for test
# if __name__ == "__main__":
#     import pandas as pd
#     import scipy.sparse as sp
#     dataset_list = [
#         'Cora', 'Citeseer', 'Pubmed', 'BlogCatalog', 'Flickr', 'ACM'
#     ]

#     n_nodes_list, n_edges_list, n_attr_list, n_class_list = [], [], [], []
#     for data_name in dataset_list:
#         print('-' * 10, data_name, '-' * 10)
#         graph, label, n_clusters = load_data(data_name)

#         print(is_bidirected(graph))

#         print(label)
#         n_nodes_list.append(graph.number_of_nodes())
#         n_edges_list.append(graph.number_of_edges())
#         n_attr_list.append(graph.ndata['feat'].shape[1])
#         n_class_list.append(n_clusters)

#     df_dataset = pd.DataFrame({
#         'Datasets': dataset_list,
#         'Nodes': n_nodes_list,
#         'Edges': n_edges_list,
#         'Attributes': n_attr_list,
#         'Classes': n_class_list
#     })
#     print(df_dataset)
