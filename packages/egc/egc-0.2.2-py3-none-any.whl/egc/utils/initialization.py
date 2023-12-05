"""
Initialization

"""
from torch import nn


def init_weights(module: nn.Module) -> None:
    """Init Module Weights

    .. code-block:: python

        from utils import init_weights
        # inside your module, do:
        for module in self.modules():
            init_weights(module)

    Args:
        module (nn.Module)
    """
    if isinstance(module, nn.Linear):
        # TODO: different initialization
        nn.init.xavier_uniform_(module.weight.data)
        if module.bias is not None:
            module.bias.data.fill_(0.0)
    elif isinstance(module, nn.Bilinear):
        nn.init.xavier_uniform_(module.weight.data)
        if module.bias is not None:
            module.bias.data.fill_(0.0)
