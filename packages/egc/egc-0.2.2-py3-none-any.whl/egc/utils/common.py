"""
common utils
"""
import csv
import os
import pickle as pkl
import random
import subprocess
from pathlib import Path
from pathlib import PurePath
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

import dgl
import numpy as np
import scipy.sparse as sp
import torch
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from texttable import Texttable
from torch import nn

act_map = {
    "relu": nn.ReLU(),
    "prelu": nn.PReLU(),
    "softmax": nn.Softmax(dim=1),
    "none": nn.Identity(),
    "linear": nn.Identity(),
}

############################################################################
# START: This section of code is adapted from https://github.com/tkipf/gcn #
############################################################################


def sparse_mx_to_torch_sparse_tensor(sparse_mx: sp.spmatrix) -> torch.Tensor:
    """Convert a scipy sparse matrix to a torch sparse tensor

    Args:
        sparse_mx (<class 'scipy.sparse'>): sparse matrix

    Returns:
        (torch.Tensor): torch sparse tensor
    """
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse_coo_tensor(indices, values, shape, dtype=torch.float32)


############################################################################
# END:   This section of code is adapted from https://github.com/tkipf/gcn #
############################################################################


def MF(X, dim, name="PCA"):
    if name == "PCA":
        model = PCA(n_components=dim)
        embedding = model.fit_transform(X)
        return embedding

    if name == "NMF":
        model = NMF(n_components=dim)
        embedding = model.fit(X)
        return embedding

    raise NotImplementedError


def tab_printer(args: Dict, thead: List[str] = None) -> None:
    """Function to print the logs in a nice tabular format.

    Args:
        args (Dict): Parameters used for the model.
    """
    args = vars(args) if hasattr(args, "__dict__") else args
    keys = sorted(args.keys())
    txt = Texttable()
    txt.set_precision(5)
    params = [["Parameter", "Value"] if thead is None else thead]
    params.extend([[
        k.replace("_", " "),
        f"{args[k]}" if isinstance(args[k], bool) else args[k],
    ] for k in keys])
    txt.add_rows(params)
    print(txt.draw())


def make_parent_dirs(target_path: PurePath) -> None:
    """make all the parent dirs of the target path.

    Args:
        target_path (PurePath): target path.
    """
    if not target_path.parent.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)


def refresh_file(target_path: str = None) -> None:
    """clear target path

    Args:
        target_path (str): file path
    """
    if target_path is not None:
        target_path: PurePath = Path(target_path)
        if target_path.exists():
            target_path.unlink()

        make_parent_dirs(target_path)
        target_path.touch()


def csv2file(
    target_path: str,
    thead: Tuple[str] = None,
    tbody: Tuple = None,
    refresh: bool = False,
    is_dict: bool = False,
) -> None:
    """save csv to target_path

    Args:
        target_path (str): target path
        thead (Tuple[str], optional): csv table header, only written into the file when\
            it is not None and file is empty. Defaults to None.
        tbody (Tuple, optional): csv table content. Defaults to None.
        refresh (bool, optional): whether to clean the file first. Defaults to False.
    """
    target_path: PurePath = Path(target_path)
    if refresh:
        refresh_file(target_path)

    make_parent_dirs(target_path)

    with open(target_path, "a+", newline="", encoding="utf-8") as csvfile:
        csv_write = csv.writer(csvfile)
        if os.stat(target_path).st_size == 0 and thead is not None:
            csv_write.writerow(thead)
        if tbody is not None:
            if is_dict:
                dict_writer = csv.DictWriter(csvfile,
                                             fieldnames=tbody[0].keys())
                for elem in tbody:
                    dict_writer.writerow(elem)
            else:
                csv_write.writerow(tbody)


def set_seed(seed: int = 4096) -> None:
    """Set random seed.

    NOTE:!!! conv and neighborSampler of dgl is somehow nondeterministic !!!

    Set according to the pytorch doc: https://pytorch.org/docs/1.9.0/notes/randomness.html
    cudatoolkit doc: https://docs.nvidia.com/cuda/cublas/index.html#cublasApi_reproducibility
    dgl issue: https://github.com/dmlc/dgl/issues/3302

    Args:
        seed (int, optional): random seed. Defaults to 4096.
    """
    if seed is not False:
        os.environ["PYTHONHASHSEED"] = str(seed)
        # required by torch: Deterministic behavior was enabled with either
        # `torch.use_deterministic_algorithms(True)` or
        # `at::Context::setDeterministicAlgorithms(true)`,
        # but this operation is not deterministic because it uses CuBLAS and you have
        # CUDA >= 10.2. To enable deterministic behavior in this case,
        # you must set an environment variable before running your PyTorch application:
        # CUBLAS_WORKSPACE_CONFIG=:4096:8 or CUBLAS_WORKSPACE_CONFIG=:16:8.
        # For more information, go to
        # https://docs.nvidia.com/cuda/cublas/index.html#cublasApi_reproducibility
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        # if you are using multi-GPU.
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        # torch.use_deterministic_algorithms(True)
        # NOTE: dgl.seed will occupy cuda:0 no matter which gpu is set if seed is set before device
        # see the issue：https://github.com/dmlc/dgl/issues/3054
        dgl.seed(seed)


def set_device(gpu: str = "0") -> torch.device:
    """Set torch device.

    Args:
        gpu (str): args.gpu. Defaults to '0'.

    Returns:
        torch.device: torch device. `device(type='cuda: x')` or `device(type='cpu')`.
    """
    max_device = torch.cuda.device_count() - 1
    if gpu == "none":
        print("Use CPU.")
        device = torch.device("cpu")
    elif torch.cuda.is_available():
        if not gpu.isnumeric():
            raise ValueError(
                f"args.gpu:{gpu} is not a single number for gpu setting."
                f"Multiple GPUs parallelism is not supported.")

        if int(gpu) <= max_device:
            print(f"GPU available. Use cuda:{gpu}.")
            device = torch.device(f"cuda:{gpu}")
            torch.cuda.set_device(device)
        else:
            print(
                f"cuda:{gpu} is not in available devices [0, {max_device}]. Use CPU instead."
            )
            device = torch.device("cpu")
    else:
        print("GPU is not available. Use CPU instead.")
        device = torch.device("cpu")
    return device


def print_model_parameters(model: torch.nn.Module) -> None:
    """print model parameters.

    Args:
        model (torch.nn.Module): Torch module.
    """
    print(dict(model.named_parameters()))


def run_subprocess_command(
    cmd: str,
    cwd_path: os.path = None,
) -> None:
    """run shell command in subprocess.

    Args:
        cmd (str): command string.
        cwd_path (os.path, optional): cwd path to run the cmd. Defaults to None.
    """
    if cwd_path is None:
        file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        cwd = os.path.abspath(file_dir)
    else:
        cwd = cwd_path
    subprocess.call(cmd, shell=True, cwd=cwd)


def dump_var(
    filename: str,
    variable: Any,
    relative_path: str = "tmp",
) -> None:
    """dump var using pickle.

    Args:
        filename (str): varname.
        variable (Any): variable to dump.
        relative_path (str, optional): relative path of the dir to save the var. Defaults to 'tmp'.
    """
    var_path: PurePath = Path(f"{relative_path}/{filename}.pkl")
    make_parent_dirs(var_path)
    with open(var_path, "wb") as fw:
        pkl.dump(variable, fw)


def load_var(filename: str, relative_path: str = "tmp") -> Any:
    """load var using pickle.

    Args:
        filename (str): varname.
        relative_path (str, optional): relative path of the dir to save the var. Defaults to 'tmp'.

    Returns:
        Any: variable.
    """
    var_path: PurePath = Path(f"{relative_path}/{filename}.pkl")
    with open(var_path, "rb") as fr:
        variable = pkl.load(fr)
    return variable


def load_or_dump(
    filename: str,
    func: Callable,
    args: Dict,
    relative_path: str = "tmp",
) -> Any:
    """load and return the variable if dumped. Otherwise calculate and dump before return.

    Args:
        filename (str): varname.
        func (Callable): func to calculate the variable.
        args (Dict): parameter dict for the func.
        relative_path (str, optional): relative path of the dir to save the var. Defaults to 'tmp'.

    Returns:
        Any: variable.
    """
    var_path: PurePath = Path(f"{relative_path}/{filename}.pkl")
    if var_path.exists():
        print(f"'{filename}' dumped before. Load from file.")
        return load_var(filename)

    print(f"calculate '{filename}' and dump.")
    var = func(**args)
    dump_var(filename, var)

    return var


def torch_sparse_to_dgl_graph(torch_sparse_mx):
    """Convert a torch sparse tensor matrix to dgl graph

    Args:
        torch_sparse_mx (torch.Tensor): torch sparse tensor

    Returns:
        (dgl.graph): dgl graph
    """
    torch_sparse_mx = torch_sparse_mx.coalesce()
    indices = torch_sparse_mx.indices()
    values = torch_sparse_mx.values()
    rows_, cols_ = indices[0, :], indices[1, :]
    dgl_graph = dgl.graph((rows_, cols_),
                          num_nodes=torch_sparse_mx.shape[0],
                          device="cuda")
    dgl_graph.edata["w"] = values.detach().cuda()
    return dgl_graph


def dgl_graph_to_torch_sparse(dgl_graph):
    values = dgl_graph.edata["w"].cpu().detach()
    rows_, cols_ = dgl_graph.edges()
    indices = torch.cat((torch.unsqueeze(rows_, 0), torch.unsqueeze(cols_, 0)),
                        0).cpu()
    torch_sparse_mx = torch.sparse.FloatTensor(indices, values)
    return torch_sparse_mx
