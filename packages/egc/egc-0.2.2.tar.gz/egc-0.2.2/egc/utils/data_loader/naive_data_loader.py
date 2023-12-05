"""Naive Graph Batch Data Loader
"""
from typing import List

import dgl
import torch

from ..graph_augmentation import ComposeAug
from ..graph_augmentation import get_augments


class NaiveDataLoader:
    """Naive DataLoader using full neighbor sampler

    Args:
        graph (dgl.DGLGraph): graph.
        batch_size (int, optional): batch size. Defaults to 1024.
        n_layers (int, optional): GNN layers. Defaults to 1.
        fanout (List[int] or int, optional): List of neighbors to sample for each GNN layer,
            with the i-th element being the fanout for the i-th GNN layer.Defaults to -1.

            - If only a single integer is provided, DGL assumes that every layer will
              have the same fanout.

            - If -1 is provided on one layer, then all inbound edges will be included.
        aug_types (List, optional): augmentation types list. Defaults to ["none"].
        drop_last (bool, optional): set to True to drop the last incomplete batch.
            Defaults to False.

    Raises:
        ValueError: raise if exists any augmentation type not supported
    """

    def __init__(
        self,
        graph: dgl.DGLGraph,
        batch_size: int = 1024,
        n_layers: int = 1,
        fanouts: List[int] or int = -1,
        aug_types: List = None,
        device: torch.device = torch.device("cpu"),
        drop_last: bool = False,
    ) -> None:
        aug_types = ["none"] if aug_types is None else aug_types
        aug_list = get_augments(aug_types)
        transform = ComposeAug(aug_list, cross=False)

        self.aug_graphs = transform(graph)

        sampler = dgl.dataloading.NeighborSampler(
            fanouts=[fanouts] *
            n_layers if isinstance(fanouts, int) else fanouts)
        self.data_loaders = [
            dgl.dataloading.DataLoader(
                g,
                g.nodes(),
                sampler,
                batch_size=batch_size,
                shuffle=False,
                drop_last=drop_last,
                num_workers=0 if torch.cuda.is_available() else 12,
                device=device,
            ) for g in self.aug_graphs
        ]
        self.device = device

    def get_aug_graphs(self) -> List[dgl.DGLGraph]:
        """Get the augmented graphs.

        Returns:
            List[dgl.DGLGraph]: list of graphs augmented.
        """
        return self.aug_graphs

    def __iter__(self):
        """Return the iterator of the data loader."""
        return _DataLoaderIter(self)

    def __len__(self):
        """Return the number of batches of the data loader."""
        return len(self.data_loaders[0])


class _DataLoaderIter:

    def __init__(self, data_loaders):
        self.device = data_loaders.device
        self.data_loaders = data_loaders.data_loaders
        self.iters_ = [iter(data_loader) for data_loader in self.data_loaders]

    # Make this an iterator for PyTorch Lightning compatibility
    def __iter__(self):
        return self

    def __next__(self):
        # [(input_nodes, output_nodes, blocks),...]
        return [(_to_device(data, self.device) for data in next(iter_))
                for iter_ in self.iters_]


def _to_device(data, device):
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = v.to(device)
    elif isinstance(data, list):
        data = [item.to(device) for item in data]
    else:
        data = data.to(device)
    return data


# def iter_data_loader(data_loaders: List) -> Generator:
#     iter_dls = [iter(dl) for dl in data_loaders]
#     for _ in range(len(data_loaders[0])):
#         try:
#             yield [(next(dl)) for dl in iter_dls]
#         except StopIteration:
#             return

# for test only
# if __name__ == '__main__':
#     from utils import load_data
#     from utils import augment_graph
#     import torch
#     graph, _, _ = load_data('Cora')
#     from module.data_loader.NaiveDataLoader import NaiveDataLoader
#     dl = NaiveDataLoader(graph)
#     for i,j in dl:
#         print(torch.all(i[2][0].dstdata['feat'][0]==j[2][0].dstdata['feat'][0]))

#     for i,j in dl:
#         print(i[2][0].srcdata['feat'].shape,j[2][0].srcdata['feat'].shape)
