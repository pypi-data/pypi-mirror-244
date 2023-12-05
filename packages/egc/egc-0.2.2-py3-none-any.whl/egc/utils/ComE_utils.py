"""
Utils for ComE model
"""
import itertools
import logging as log
import math
import os
import random
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from itertools import zip_longest
from multiprocessing import cpu_count
from os import path
from time import time

import numpy as np

log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.INFO,
)


def chunkize_serial(iterable, chunksize, as_numpy=False):
    """
    Return elements from the iterable in `chunksize`-ed lists. The last returned
    element may be smaller (if length of collection is not divisible by `chunksize`).

    >>> print(list(grouper(range(10), 3)))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    """

    it = iter(iterable)
    while True:
        if as_numpy:
            # convert each document to a 2d numpy array (~6x faster when transmitting
            # chunk data over the wire, in Pyro)
            wrapped_chunk = [[
                np.array(doc) for doc in itertools.islice(it, int(chunksize))
            ]]
        else:
            wrapped_chunk = [list(itertools.islice(it, int(chunksize)))]
        if not wrapped_chunk[0]:
            break
        # memory opt: wrap the chunk and then pop(), to avoid leaving behind a dangling reference
        yield wrapped_chunk.pop()


def prepare_sentences(model, paths):
    """
    :param model: current model containing the vocabulary and the index
    :param paths: list of the random walks.
        we have to translate the node to the appropriate index and apply the dropout
    :return: generator of the paths according to the dropout probability and the correct index
    """
    for _path in paths:
        # avoid calling random_sample() where prob >= 1, to speed things up a little:
        sampled = [
            model.vocab[node] for node in _path if node in model.vocab and
            (model.vocab[node].sample_probability >= 1.0 or
             model.vocab[node].sample_probability >= np.random.random_sample())
        ]
        yield sampled


def batch_generator(iterable, batch_size=1):
    """same as chunkize_serial, but without the usage of an infinite while

    :param iterable: list that we want to convert in batches
    :param batch_size: batch size
    """
    args = [iterable] * batch_size
    return itertools.zip_longest(*args, fillvalue=None)


class RepeatCorpusNTimes:
    """Class used to repeat n-times the same corpus of paths

    :param corpus: list of paths that we want to repeat
    :param n: number of times we want to repeat our corpus
    """

    def __init__(self, corpus, n):
        self.corpus = corpus
        self.n = n

    def __iter__(self):
        for _ in range(self.n):
            for document in self.corpus:
                yield document


class Vocab:
    """A single vocabulary item, used internally for
    constructing binary trees (incl. both word leaves and inner nodes)."""

    def __init__(self, **kwargs):
        self.count = 0
        self.__dict__.update(kwargs)

    def __lt__(self, other):  # used for sorting in a priority queue
        return self.count < other.count

    def __str__(self):
        vals = [
            f"{key}:{self.__dict__[key]}" for key in sorted(self.__dict__)
            if not key.startswith("_")
        ]
        return "<" + ", ".join(vals) + ">"


def xavier_normal(size, as_type=np.float32, gain=1):
    assert len(size) == 2
    std = gain * math.sqrt(2.0 / sum(size))
    return np.random.normal(size=size, loc=0, scale=std).astype(as_type)


log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.INFO,
)


def __random_walk__(G, path_length, start, alpha=0, rand=random.Random()):
    """Returns a truncated random walk.

    :param G: networkx graph
    :param path_length: Length of the random walk.
    :param alpha: probability of restarts.
    :param rand: random number generator
    :param start: the start node of the random walk.

    :return:
    """
    _path = [start]

    while len(_path) < path_length:
        cur = _path[-1]
        if len(list(G.neighbors(cur))) > 0:
            if rand.random() >= alpha:
                _path.append(rand.choice(list(G.neighbors(cur))))
            else:
                _path.append(_path[0])
        else:
            break
    return _path


class WriteWalksToDisk:
    """Used for writing rand walks to disk"""

    def __init__(self):
        self.__current_graph = None
        self.__vertex2str = None

    def _write_walks_to_disk(self, args):
        num_paths, path_length, alpha, rand, f = args
        G = self.__current_graph
        t_0 = time()
        with open(f, "w", encoding="utf8") as fout:
            for walk in build_deepwalk_corpus_iter(
                    G=G,
                    num_paths=num_paths,
                    path_length=path_length,
                    alpha=alpha,
                    rand=rand,
            ):
                fout.write(f"{' '.join(self.__vertex2str[v] for v in walk)}\n")
        print(f"Generated new file {f}, it took {time() - t_0} seconds")
        return f

    def write_walks_to_disk(
            self,
            G,
            filebase,
            num_paths,
            path_length,
            alpha=0,
            rand=random.Random(0),
            num_workers=cpu_count(),
    ):
        """save the random walks on files so is not needed to perform
        the walks at each execution

        :param G: graph to walks on
        :param filebase: location where to save the final walks
        :param num_paths: number of walks to do for each node
        :param path_length: lenght of each walks
        :param alpha: restart probability for the random walks
        :param rand: generator of random numbers
        :param num_workers: number of thread used to execute the job

        :return:
        """
        self.__current_graph = G
        self.__vertex2str = {v: str(v) for v in G.nodes()}
        files_list = [f"{filebase}.{str(x)}" for x in range(num_paths)]

        args_list = []
        files = []
        print(f"file_base: {filebase}")
        if num_paths <= num_workers:
            paths_per_worker = [1 for x in range(num_paths)]
        else:
            paths_per_worker = [
                sum([y is not None for y in x]) for x in grouper(
                    int(num_paths / num_workers) + 1, range(1, num_paths + 1))
            ]

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            for _, file_, ppw in zip(executor.map(count_lines, files_list),
                                     files_list, paths_per_worker):
                args_list.append((
                    ppw,
                    path_length,
                    alpha,
                    random.Random(rand.randint(0, 2**31)),
                    file_,
                ))

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            for file_ in executor.map(self._write_walks_to_disk, args_list):
                files.append(file_)

        return files


def combine_files_iter(file_list):
    for file in file_list:
        with open(file, "r", encoding="utf8") as f:
            for line in f:
                yield map(int, line.split())


def count_lines(f):
    if path.isfile(f):
        num_lines = 0
        with open(f, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if line:
                    num_lines = num_lines + 1
                else:
                    break
        return num_lines
    return 0


def build_deepwalk_corpus_iter(G,
                               num_paths,
                               path_length,
                               alpha=0,
                               rand=random.Random(0)):
    nodes = list(G.nodes())
    for _ in range(num_paths):
        rand.shuffle(nodes)
        for node in nodes:
            yield __random_walk__(G,
                                  path_length,
                                  rand=rand,
                                  alpha=alpha,
                                  start=node)


def count_textfiles(files, workers=1):
    c = Counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for c_ in executor.map(count_words, files):
            c.update(c_)
    return c


def count_words(file):
    """Counts the word frequences in a list of sentences.

    Note:
      This is a helper function for parallel execution of `Vocabulary.from_text`
      method.
    """
    c = Counter()
    with open(file, "r", encoding="utf8") as f:
        for l in f:
            words = [int(word) for word in l.strip().split()]
            c.update(words)
    return c


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def judgeExist(utils_dir):
    files = os.listdir(utils_dir)
    for f in files:
        if ".so" in f:
            if f"cpython-{sys.version_info.major}{sys.version_info.minor}" in f:
                return True
            subprocess.run(
                f"rm {utils_dir}/*.c {utils_dir}/*.so {utils_dir}/*.o",
                shell=True,
                cwd=utils_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

    return False


def initComeEnv():
    basename = os.path.abspath(
        f"{os.path.dirname(os.path.realpath(__file__))}/..", )
    utils_dir = f"{basename}/module/pretrain/ComE/SDG_utils"
    if judgeExist(utils_dir=utils_dir):
        return
    build_dir = f"{utils_dir}/build"
    if not os.path.exists(build_dir):
        subprocess.run(
            f"mkdir {build_dir}",
            shell=True,
            cwd=utils_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    subprocess.run(
        f"python {utils_dir}/cython_utils.py build_ext",
        shell=True,
        cwd=utils_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    files = getFile(build_dir)
    for file in files:
        command = "mv " + file + " " + utils_dir
        subprocess.run(
            command,
            shell=True,
            cwd=build_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    subprocess.run(
        f"rm -rf {utils_dir}/build",
        shell=True,
        cwd=utils_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return


def getFile(build_dir):
    res = []
    files = os.listdir(build_dir)
    files = [build_dir + "/" + file for file in files]
    for file in files:
        if os.path.isdir(file):
            res.extend(getFile(file))
        else:
            res.append(file)
    return res
