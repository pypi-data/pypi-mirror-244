"""AGM Pretrain
C++ Pretrain source code is copied from: https://github.com/SamJia/CommunityGAN
"""
import os
import subprocess
from ast import literal_eval
from typing import Dict
from typing import Tuple

import numpy as np


def agm_pretrain(
    edges: Tuple,
    n_clusters: int,
    n_threads: int = 20,
    n_epochs: int = 200,
    rest_args: Dict = None,
    dataset_name: str = "Cora",
    overlapping: bool = True,
) -> np.ndarray:
    """AGM Pretrain

    Args:
        edges (Tuple): edges.
        n_clusters (int): num of clusters.
        n_threads (int, optional): num of threads. Defaults to 20.
        n_epochs (int, optional): num of pretrain epochs. Defaults to 200.
        rest_args (Dict, optional): other args for agm pretrain. Defaults to {}.
        dataset_name (str, optional): dataset name. Defaults to 'Cora'.
        overlapping (bool, optional): whether dataset is overlapping. Defaults to True.

    Returns:
        np.ndarray: node embedding pretrained by AGM
    """
    cwd_path = os.path.abspath(
        f"{os.path.dirname(os.path.realpath(__file__))}/agm_pretrain")
    subprocess.call("rm -rf cache", shell=True, cwd=cwd_path)
    subprocess.call("mkdir cache", shell=True, cwd=cwd_path)

    with open(f"{cwd_path}/cache/{dataset_name}_edges.txt",
              "w",
              encoding="utf-8") as f:
        for u, v in zip(edges[0], edges[1]):
            f.writelines(f"{u}\t{v}\n")

    rest_args = (" ".join([
        f"-{key} {value}" for key, value in rest_args.items()
    ]) if rest_args is not None else "")

    subprocess.call("make", shell=True, cwd=cwd_path)
    subprocess.call(
        f"./magic -i {cwd_path}/cache/{dataset_name}_edges.txt  -o cache/{dataset_name}_\
             -nt {n_threads} -c {n_clusters} -mi {n_epochs} {rest_args}",
        shell=True,
        cwd=cwd_path,
    )
    # Args of ./magic
    # -i:Input edgelist file name.
    # -o:Output Graph data prefix. Defaults to 'cache/{dataset_name}_'.
    # -nt:Number of threads for parallelization(default: 56). Defaults to n_threads, i.e., 20.
    # -mi:Maximum number of update iteration(default: 500). Defaults to n_epochs, i.e., 200.
    # -l:Input file name for node dates (Node ID, Node date) (default: none)
    # -t:Input file name for node' text (Node ID, Node texts), \
    #     'none' means do not load text (default: none)
    # -c:The number of communities to detect (-1 detect automatically).
    # -mc:Minimum number of communities to try(default: 5)
    # -xc:Maximum number of communities to try(default: 500)
    # -nc:How many trials for the number of communities(default: 10)
    # -sa:Alpha for backtracking line search(default: 0.05)
    # -sb:Beta for backtracking line search(default: 0.1)
    # -st:Allow reference between two same time node or not (0: don't allow, 1: allow)(default: 0)
    # -woe:Disable Eta or not (0: enable eta, 1: disable eta, 2: symmetric eta)(default: 1)
    # -se:same Eta or not (0: different eta, 1: same eta)(default: 1)
    # -si:How many iterations for once save(default: 5000)
    # -rsi:How many iterations for once negative sampling(default: 10)
    # -sa:Zero Threshold for F and eta(default: 0.0001)
    # -lnf:Remain only largest how many elements for F(default: 0)

    with open(f"{cwd_path}/cache/{dataset_name}_final.f.txt",
              "r",
              encoding="utf-8") as f:
        n_nodes, _ = f.readline().split()
        emb = np.zeros((int(n_nodes), n_clusters))
        for line in f:
            line_tuple = line.split()
            node = int(line_tuple[0].replace("d", ""))
            cluster_tuple = literal_eval(line_tuple[1].replace(")(", "),("))
            if len(cluster_tuple) > 0:
                val = np.zeros((n_clusters, ))
                idx, value = zip(*cluster_tuple)
                if overlapping:
                    val.put(idx, value)
                else:
                    idx = np.argmax(value)
                    val.put([idx], value[idx])
                emb[node] = val

    return emb
