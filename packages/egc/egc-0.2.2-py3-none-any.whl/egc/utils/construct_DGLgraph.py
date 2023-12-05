"""
construct_DGLgraph
"""
import collections

import dgl
import numpy as np
import torch
from sklearn.metrics import pairwise_distances as pair


def construct_DGLgraph_for_non_graph(x, labels, k=3, method="euclidean"):
    if method == "heat":
        return construct_DGLgraph_for_non_graph_by_heat(x, labels, k)
    if torch.is_tensor(x) is False:
        x = torch.Tensor(x)
    if torch.is_tensor(labels) is False:
        labels = torch.Tensor(labels)
    knn_g = dgl.knn_graph(x, k, dist=method)
    edges = knn_g.edges()
    edges = np.array(process_edges_info(edges))
    return build_graph(x, edges, x.shape[0], labels)


def construct_DGLgraph_for_non_graph_by_heat(x, labels, k=3):
    if torch.is_tensor(x) is False:
        x = torch.Tensor(x)
    if torch.is_tensor(labels) is False:
        labels = torch.Tensor(labels)
    dist = None

    dist = -0.5 * pair(x)**2  # 时间参数t默认为2？？？？？,计算任意两个节点之间的距离，并返回一个矩阵
    dist = np.exp(dist)  # 得到相似度矩阵
    inds = []
    for i in range(dist.shape[0]):
        ind = np.argpartition(dist[i, :], -(k + 1))[-(k + 1):]  # 获取k个最相似的节点的下标
        inds.append(ind)
    src = []
    dst = []
    counter = 0
    for i, v in enumerate(inds):
        for vv in v:
            if vv == i:
                pass
            else:
                if labels[vv] != labels[i]:
                    counter += 1
                src.append(i)
                dst.append(vv)
    edges = torch.stack((torch.Tensor(src), torch.Tensor(dst)), dim=1)
    edges = np.array(process_edges_info(edges))
    return build_graph(x, edges, x.shape[0], labels)


def construct_DGLgraph_for_graph(x, labels, edges):
    if torch.is_tensor(x) is False:
        x = torch.Tensor(x)
    if torch.is_tensor(labels) is False:
        labels = torch.Tensor(labels)
    edges = np.array(process_edges_info(edges))
    return build_graph(x, edges, x.shape[0], labels)


def process_edges_info(
        edges):  # 由于DGL图会将重复的边也算进边的总数内，所有要去除重复的边和自环，到后面统一添加自环,并且DGL
    edge_dict = collections.defaultdict(bool)
    pair_list = []
    u = edges[0]
    v = edges[1]
    length = len(edges[0])
    for i in range(length):
        if (edge_dict[(u[i].item(), v[i].item())] is False
                and u[i].item() != v[i].item()):
            edge_dict[(u[i].item(), v[i].item())] = True
            edge_dict[(v[i].item(), u[i].item())] = True
            pair_list.append((u[i].item(), v[i].item()))
            pair_list.append((v[i].item(), u[i].item()))
    return pair_list


def build_graph(features, edges, num_nodes, labels):  # 构图，减少代码重复
    graph = dgl.graph((edges[0], edges[1]), num_nodes=num_nodes)
    graph.ndata["feat"] = features
    graph.ndata["label"] = labels
    graph = dgl.add_self_loop(graph)
    return graph
