"""Multilayer DNN"""
from collections import OrderedDict
from typing import List

from torch import nn

from ...utils import act_map
from ...utils import init_weights


class MultiLayerDNN(nn.Module):
    """MultiLayer Deep Nueral Networks.

    Args:
        in_feats (int): Input feature dimension.
        out_feats_list (List[int]): List of hidden units dimensions.
        bias (List[bool], optional): Whether to apply bias at each layer. Defaults to True.
        activation (List[str], optional): Activation func list to apply at each layer. \
            Defaults to ReLU.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        bias: List[bool] = None,
        activation: List[str] = None,
    ) -> None:
        super().__init__()
        pre_layer = in_feats
        layer_list = []
        for idx, hidden_units in enumerate(out_feats_list):
            layer_list.append((
                f"linear{idx}",
                nn.Linear(
                    pre_layer,
                    hidden_units,
                    bias=True if bias is None else bias[idx],
                ),
            ))
            layer_list.append((
                f"act{idx}",
                nn.ReLU() if activation is None else act_map[activation[idx]],
            ))
            pre_layer = hidden_units
        self.model = nn.Sequential(OrderedDict(layer_list))

        for module in self.modules():
            init_weights(module)

    def forward(self, x):
        h = self.model(x)
        return h
