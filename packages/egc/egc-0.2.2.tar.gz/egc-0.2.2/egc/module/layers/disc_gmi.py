"""
Discriminator Layer
Adapted from: https://github.com/PetarV-/DGI & https://github.com/zpeng27/GMI
"""
import torch
from torch import nn

from ...utils import init_weights


class DiscGMI(nn.Module):
    """Discriminator Layer

    Args:
        in1_features (int): size of each first input sample.
        in2_features (int): size of each second input sample.
        out_features (int): size of each output sample. Defaults to 1.
        activation (str): activation of xWy. Defaults to sigmoid.
        bias (bool): whether to apply bias to xWy. Defaults to False.
    """

    def __init__(
        self,
        in1_features: int,
        in2_features: int,
        out_features: int = 1,
        activation: str = "sigmoid",
        bias: bool = True,
    ) -> None:
        super().__init__()
        self.f_k = nn.Bilinear(in1_features, in2_features, out_features, bias)

        if activation == "sigmoid":
            self.activation = nn.Sigmoid()
        else:
            self.activation = nn.ReLU()

        for module in self.modules():
            init_weights(module)

    def forward(
        self,
        in1_features: torch.Tensor,
        in2_features: torch.Tensor,
        neg_sample_list: int = None,
    ):
        """Forward Propagation

        Args:
            in1_features (torch.Tensor): first input sample in shape of [1, xx, xx].
            in2_features (torch.Tensor): second input sample in shape of [1, xx, xx].
            neg_sample_list (List, optional):
                list of neg sampling nodes index of first input. Defaults to None.

        Returns:
            s_c, s_c_neg (torch.Tensor): output of discriminator.
        """
        s_c = self.activation(
            torch.squeeze(self.f_k(in1_features, in2_features), 2))
        if neg_sample_list is not None:
            s_c_neg = self._neg_sample_forward(in1_features, in2_features,
                                               neg_sample_list)
        else:
            s_c_neg = None

        return s_c, s_c_neg

    def _neg_sample_forward(self, in1_features, in2_features, neg_sample_list):
        """Pointwise Forward Propagation

        Args:
            in1_features (torch.Tensor): first input sample in shape of [1, xx, xx].
            in2_features (torch.Tensor): second input sample in shape of [1, xx, xx].
            neg_sample_list (List): list of negative sampling nodes index of first input.

        Returns:
            s_c_neg (torch.Tensor): output of discriminator for negative sampling list .
        """
        s_c_list = []
        list_len = len(neg_sample_list)

        for i in range(list_len):
            h_mi = torch.unsqueeze(in1_features[0][neg_sample_list[i]], 0)
            s_c_iter = torch.squeeze(self.f_k(h_mi, in2_features), 2)
            s_c_list.append(s_c_iter)

        sc_stack = torch.squeeze(torch.stack(s_c_list, 1), 0)

        return self.activation(sc_stack)
