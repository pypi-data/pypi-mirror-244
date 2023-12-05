"""MultiLayer GraphSAGE"""
from typing import List

from dgl.nn.pytorch.conv import SAGEConv
from torch import nn

from ...utils import act_map


class MultiLayerGNN(nn.Module):
    """MultiLayer GraphSAGE with different types of aggregator_type.

    Args:
        in_feats (int): Input feature dimension.
        out_feats_list (List[int]): List of hidden units dimensions.
        aggregator_type (str, optional): Aggregate type of sage. Defaults to 'gcn'.
        bias (bool, optional): Whether to apply bias. Defaults to True.
    """

    def __init__(
        self,
        in_feats: int,
        out_feats_list: List[int],
        aggregator_type: str = "gcn",
        bias: bool = True,
        activation: List[str] = None,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        pre_layer = in_feats
        for idx, hidden_units in enumerate(out_feats_list):
            setattr(
                self,
                f"conv{idx}",
                SAGEConv(
                    in_feats=pre_layer,
                    out_feats=hidden_units,
                    aggregator_type=aggregator_type,
                    bias=bias,
                    feat_drop=dropout,
                    activation=nn.ReLU()
                    if activation is None else act_map[activation[idx]],
                ),
            )
            pre_layer = hidden_units

    def forward(self, blocks, x, edge_weight=None):
        for idx, block in enumerate(blocks):
            conv = getattr(self, f"conv{idx}")
            x = conv(block, x, edge_weight)
        return x
