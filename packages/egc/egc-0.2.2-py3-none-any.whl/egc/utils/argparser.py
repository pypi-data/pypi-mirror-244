"""Parse All Model Args"""
import argparse
import os
from pathlib import Path
from pathlib import PurePath
from typing import Dict

import yaml

from .common import tab_printer

type_map = {"int": int, "str": str, "float": float, "bool": bool}

#: Info of the models supported.
models: Dict = {
    "pca_kmeans": {
        "name": "PCA",
        "description": "PCA with Kmeans.",
        "paper url": "",
        "source code": "",
    },
    "sgc_kmeans": {
        "name": "SGC",
        "description": "SGC with Kmeans.",
        "paper url": "https://arxiv.org/pdf/1902.07153.pdf",
        "source code": "https://github.com/Tiiiger/SGC",
    },
    "dgi_kmeans": {
        "name": "DGI",
        "description": "DGI with Kmeans",
        "paper url": "https://arxiv.org/abs/1809.10341",
        "source code": "https://github.com/PetarV-/DGI",
    },
    "gmi_kmeans": {
        "name": "GMI",
        "description": "GMI with Kmeans",
        "paper url": "https://arxiv.org/pdf/1809.10341.pdf",
        "source code": "https://github.com/zpeng27/GMI",
    },
    "DANMF": {
        "name": "DANMF",
        "description": "DANMF",
        "paper url": "https://dl.acm.org/doi/pdf/10.1145/3269206.3271697",
        "source code": "https://github.com/benedekrozemberczki/DANMF",
    },
    "MNMF": {
        "name": "MNMF",
        "description": "MNMF",
        "paper url": "https://ojs.aaai.org/index.php/AAAI/article/view/10488",
        "source code": "https://github.com/AnryYang/M-NMF",
    },
    "VGAECD": {
        "name": "VGAECD",
        "description": "VGAECD",
        "paper url":
        "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8594831",
        "source code": "",
    },
    "CommunityGAN": {
        "name": "CommunityGAN",
        "description": "CommunityGAN",
        "paper url": "https://dl.acm.org/doi/pdf/10.1145/3308558.3313564",
        "source code": "https://github.com/SamJia/CommunityGAN",
    },
    "gae_kmeans": {
        "name": "GAE",
        "description": "GAE with Kmeans",
        "paper url": "https://arxiv.org/pdf/1611.07308.pdf",
        "source code": "https://github.com/tkipf/gae",
    },
    "vgae_kmeans": {
        "name": "VGAE",
        "description": "VGAE with Kmeans",
        "paper url": "https://arxiv.org/pdf/1611.07308.pdf",
        "source code": "https://github.com/tkipf/gae",
    },
    "DFCN": {
        "name": "DFCN",
        "description": "DFCN",
        "paper url": "https://arxiv.org/pdf/2012.09600.pdf",
        "source code": "https://github.com/WxTu/DFCN",
    },
    "AGE": {
        "name": "AGE",
        "description": "AGE",
        "paper url": "https://dl.acm.org/doi/pdf/10.1145/3394486.3403140",
        "source code": "https://github.com/thunlp/AGE",
    },
    "DAEGC": {
        "name": "DAEGC",
        "description": "DAEGC",
        "paper url": "https://www.ijcai.org/Proceedings/2019/0509.pdf",
        "source code": "https://github.com/Tiger101010/DAEGC",
    },
    "SEComm": {
        "name": "SEComm",
        "description": "SEComm",
        "paper url":
        "https://proceedings.mlr.press/v161/bandyopadhyay21a/bandyopadhyay21a.pdf",
        "source code": "https://github.com/viz27/SEComm",
    },
    "cc": {
        "name": "CC",
        "description": "Contrastive Clustering",
        "paper url": "https://arxiv.org/pdf/2009.09687.pdf",
        "source code": "https://github.com/Yunfan-Li/Contrastive-Clustering",
    },
    "SDCN": {
        "name": "SDCN",
        "description": "SDCN",
        "paper url": "https://arxiv.org/pdf/2002.01633.pdf",
        "source code": "https://github.com/bdy9527/SDCN",
    },
    "SENet_kmeans": {
        "name": "SENet",
        "description": "SENEet with kmeans",
        "paper url":
        "https://www.sciencedirect.com/science/article/pii/S0893608021002227?via%3Dihub",
        "source code": "",
    },
    "ComE": {
        "name": "ComE",
        "description": "ComE",
        "paper url": "https://dl.acm.org/doi/pdf/10.1145/3132847.3132925",
        "source code": "https://github.com/andompesta/ComE",
    },
    "AGCN": {
        "name": "AGCN",
        "description": "AGCN",
        "paper url": "",
        "source code": "https://github.com/ZhihaoPENG-CityU/MM21---AGCN",
    },
    "AGC": {
        "name": "AGC",
        "description": "AGC",
        "paper url": "https://dl.acm.org/doi/abs/10.1145/3474085.3475276",
        "source code": "https://github.com/karenlatong/AGC-master",
    },
    "GALA": {
        "name": "GALA",
        "description": "GALA",
        "paper url": "https://arxiv.org/pdf/1908.02441v1.pdf",
        "source code": "https://github.com/sseung0703/GALA_TF2.0",
    },
    "idec": {
        "name": "idec",
        "description": "IDEC",
        "paper url": "https://dl.acm.org/doi/10.5555/3045390.3045442",
        "source code": "https://github.com/piiswrong/dec",
    },
    "clusternet": {
        "name": "clusternet",
        "description": "ClusterNet",
        "paper url": "https://arxiv.org/abs/1905.13732",
        "source code": "https://github.com/bwilder0/clusternet",
    },
    "GDCL": {
        "name": "GDCL",
        "description": "GDCL",  # BUG exits
        "paper url": "https://www.ijcai.org/proceedings/2021/0473.pdf",
        "source code": "https://github.com/hzhao98/GDCL",
    },
    "MVGRL": {
        "name": "MVGRL",
        "description": "MVGRL",
        "paper url": "https://arxiv.org/abs/2006.05582",
        "source code": "https://github.com/kavehhassani/mvgrl",
    },
    "SUBLIME": {
        "name": "SUBLIME",
        "description": "SUBLIME",
        "paper url": "https://arxiv.org/pdf/2201.06367.pdf",
        "source code": "https://github.com/GRAND-Lab/SUBLIME",
    },
}


def _read_args(model: str = None) -> Dict:
    basename = os.path.abspath(
        f"{os.path.dirname(os.path.realpath(__file__))}/..", )
    config_path: PurePath = Path(f"{basename}/config/{model}.yaml")
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:
        args = yaml.safe_load(f)
    return args


def _set_subparser(model: str, _parser: argparse.ArgumentParser) -> None:
    args = _read_args(model)
    for key, val in args.items():
        keys = val.keys()
        default_val = val["default"] if "default" in keys else None
        type_val = type_map[val["type"]] if "type" in keys else type(
            val["default"])
        nargs_val = val["nargs"] if "nargs" in keys else None
        _parser.add_argument(
            f"--{key}",
            type=type_val,
            default=default_val,
            help=val["help"],
            nargs=nargs_val,
        )


def parse_all_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="EAGLE Graph Clustering",
        description="Parameters for Graph Clustering",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="Cora",
        help="Dataset used in the experiment",
    )
    parser.add_argument(
        "--gpu",
        type=str,
        default="0",
        help="ID(s) of gpu used by cuda",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="./data",
        help="Path to store the dataset",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=4096,
        help="Random seed. Defaults to 4096.",
    )
    parser.add_argument(
        "--nodes_rate",
        type=float,
        default=0.5,
        help="Random sample nodes rate in same class. Defaults to 0.5.",
    )
    parser.add_argument(
        "--add_edge_rate",
        type=float,
        default=0.5,
        help="Random add edge rate in same class. Defaults to 0.5.",
    )
    parser.add_argument(
        "--not_set_seed",
        dest="seed",
        action="store_false",
        help="Force Not to Use Random Seed.",
    )
    parser.add_argument(
        "--target_path",
        type=str,
        default=None,
        help=
        "Target file path to save the experiment results. Defaults to None.",
    )

    subparsers = parser.add_subparsers(dest="model", help="sub-command help")

    for _model, items in models.items():
        # pylint: disable=invalid-sequence-index
        _help = items["description"]
        _parser = subparsers.add_parser(
            _model,
            help=f"Run Graph Clustering on {_help}",
        )
        _set_subparser(_model, _parser)

    args = parser.parse_args()

    tab_printer(args)

    return args


def get_default_args(model: str) -> Dict:
    """Get default args of any model supported.

    Args:
        model (str): name of the model.

    Returns:
        Dict: the default args of the model.
    """
    _args = _read_args(model)
    args = {}
    for key, val in _args.items():
        keys = val.keys()
        default_val = val["default"] if "default" in keys else None
        args[key] = default_val

    return args
