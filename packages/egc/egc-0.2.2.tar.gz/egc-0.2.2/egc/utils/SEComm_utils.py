"""
SEComm utils
"""
import functools

import dgl
import numpy as np
import torch
from scipy.sparse.linalg import svds
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import normalize
from sklearn.preprocessing import OneHotEncoder


def enhance_sim_matrix(
    C: np.ndarray,
    K: int,
    d: int,
    alpha: float,
) -> np.ndarray:
    """Enhance similarity matrix.

    Args:
        C (np.ndarray): coefficient matrix.
        K (int): number of clusters.
        d (int): dimension of each subspace.
        alpha (float): coefficient.

    Returns:
        np.ndarray: enhanced similarity matrix
    """
    C = 0.5 * (C + C.T)
    r = min(d * K + 1, C.shape[0] - 1)
    U, S, _ = svds(C, r, v0=np.ones(C.shape[0]))
    U = U[:, ::-1]
    S = np.sqrt(S[::-1])
    S = np.diag(S)
    U = U.dot(S)
    U = normalize(U, norm="l2", axis=1)
    Z = U.dot(U.T)
    Z = Z * (Z > 0)
    L = np.abs(Z**alpha)
    L = 0.5 * (L + L.T)
    L = L / L.max()
    return L


def drop_feature(x, drop_prob):
    drop_mask = (torch.empty((x.size(1), ),
                             dtype=torch.float32,
                             device=x.device).uniform_(0, 1) < drop_prob)
    x = x.clone()
    x[:, drop_mask] = 0

    return x


def dropout_adj0(g, num_nodes, p=0.5):
    if p < 0.0 or p > 1.0:
        raise ValueError(f"Dropout probability has to be between 0 and 1 "
                         f"(got {p}")
    edge_index = torch.stack(g.edges(), dim=1)
    mask = edge_index.new_full((edge_index.size(0), ),
                               1 - p,
                               dtype=torch.float)
    mask = torch.bernoulli(mask).to(torch.bool)
    u = edge_index[mask, 0]
    v = edge_index[mask, 1]

    return dgl.graph((u, v), num_nodes=num_nodes)


def repeat(n_times):

    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            results = [f(*args, **kwargs) for _ in range(n_times)]
            statistics = {}
            for key in results[0].keys():
                values = [r[key] for r in results]
                statistics[key] = {
                    "mean": np.mean(values),
                    "std": np.std(values)
                }
            print_statistics(statistics, f.__name__)
            return statistics

        return wrapper

    return decorator


def prob_to_one_hot(y_pred):
    ret = np.zeros(y_pred.shape, bool)
    indices = np.argmax(y_pred, axis=1)
    for i in range(y_pred.shape[0]):
        ret[i][indices[i]] = True
    return ret


def print_statistics(statistics, function_name):
    print(f"(E) | {function_name}:", end=" ")
    for i, key in enumerate(statistics.keys()):
        mean = statistics[key]["mean"]
        std = statistics[key]["std"]
        print(f"{key}={mean:.4f}+-{std:.4f}", end="")
        if i != len(statistics.keys()) - 1:
            print(",", end=" ")
        else:
            print()


@repeat(3)
def label_classification(embeddings, y, ratio):
    X = embeddings.detach().cpu().numpy()
    Y = y.detach().cpu().numpy()
    Y = Y.reshape(-1, 1)
    onehot_encoder = OneHotEncoder(categories="auto").fit(Y)
    Y = onehot_encoder.transform(Y).toarray().astype(bool)

    X = normalize(X, norm="l2")

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=1 - ratio)

    logreg = LogisticRegression(solver="liblinear")
    c = 2.0**np.arange(-10, 10)

    clf = GridSearchCV(
        estimator=OneVsRestClassifier(logreg),
        param_grid=dict(estimator__C=c),
        n_jobs=8,
        cv=5,
        verbose=0,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict_proba(X_test)
    y_pred = prob_to_one_hot(y_pred)

    micro = f1_score(y_test, y_pred, average="micro")
    macro = f1_score(y_test, y_pred, average="macro")

    return {"F1Mi": micro, "F1Ma": macro}
