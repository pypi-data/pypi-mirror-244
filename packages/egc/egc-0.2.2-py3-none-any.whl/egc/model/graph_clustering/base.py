"""Base Model for Graph Clustering
"""
from typing import Any
from typing import Callable


def _unimplemented(self, *fit_input: Any) -> None:
    raise NotImplementedError


class Base:
    """Base class with constructor and public methods for Graph Clustering model."""

    def __init__(self):
        """Creating an estimator."""

    fit: Callable[..., Any] = _unimplemented

    get_embedding: Callable[..., Any] = _unimplemented

    get_memberships: Callable[..., Any] = _unimplemented

    def get_cluster_centers(self):
        """Getting the cluster centers."""
