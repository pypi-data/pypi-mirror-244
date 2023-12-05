"""Model of ComE"""
import logging as log
import os
import random
import timeit
from math import floor
from pathlib import Path

import numpy as np

from ....module.pretrain.ComE.community_embeddings_ComE import Community2Vec
from ....module.pretrain.ComE.context_embeddings_ComE import Context2Vec
from ....module.pretrain.ComE.node_embeddings_ComE import Node2Vec
from ....utils.ComE_utils import combine_files_iter
from ....utils.ComE_utils import count_textfiles
from ....utils.ComE_utils import Vocab
from ....utils.ComE_utils import WriteWalksToDisk
from ....utils.ComE_utils import xavier_normal

log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.DEBUG,
)


class ComE:
    """
    class that keep track of all the parameters used during the learning of the embedding.


    :param nodes_degree: Dict with node_id: degree of node
    :param size: projection space
    :param down_sampling: perform down_sampling of common node
    :param table_size: size of the negative table to generate
    :param path_labels: location of the file containing the ground true (label for each node)
    :param input_file: name of the file containing the ground true (label for each node)
    :return:
    """

    def __init__(
        self,
        graph,
        n_clusters=7,
        size=2,
        down_sampling=0,
        table_size=100000000,
        labels=None,
        batch_size=50,
        num_workers=10,
        negative=5,
        lr=0.025,
        window_size=10,
        num_walks=10,
        walk_length=80,
        num_iter=1,
        output_file="Cora",
        alpha=0.1,
        beta=0.1,
        reg_covar=0.00001,
    ) -> None:
        self.predict = None
        self.down_sampling = down_sampling
        self.table_size = table_size
        if size % 4 != 0:
            log.warning(
                "consider setting layer size to a multiple of 4 for greater performance"
            )
        self.layer1_size = int(size)
        self.G = graph.to_networkx().to_undirected()
        self.num_walks = num_walks
        self.walk_length = walk_length
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.negative = negative
        self.lr = lr
        self.window_size = window_size
        self.num_iter = num_iter
        self.output_file = output_file
        self.alpha = alpha
        self.beta = beta
        self.reg_covar = reg_covar
        self.n_clusters = n_clusters
        self.centroid = None
        self.covariance_mat = None
        self.inv_covariance_mat = None
        self.pi = None
        self.node_embedding = np.array(graph.ndata["feat"])
        self.node_embedding[self.node_embedding - 0.0 > 0.0001] = 1.0
        log.info("\t\tsampling the paths")

        basename = os.path.abspath(
            f"{os.path.dirname(os.path.realpath(__file__))}/..", )
        walks_filebase = os.path.join(
            basename, "tmp", "data",
            self.output_file + "_Walks")  # where read/write the sampled path
        if not os.path.exists(walks_filebase):
            Path(walks_filebase).mkdir(parents=True, exist_ok=True)
        writeWalksToDisk = WriteWalksToDisk()
        self.walk_files = writeWalksToDisk.write_walks_to_disk(
            self.G,
            os.path.join(walks_filebase, f"{self.output_file}.walks"),
            num_paths=self.num_walks,
            path_length=self.walk_length,
            alpha=0,
            rand=random.Random(0),
            num_workers=self.num_workers,
        )

        nodes_degree = count_textfiles(self.walk_files, self.num_workers)

        if nodes_degree is not None:
            self.build_vocab_(nodes_degree)
            self.ground_true = labels
            # inizialize node and context embeddings
            self.make_table()
            self.precalc_sampling()
            self.reset_weights()
        else:
            log.warning("Model not initialized, need the nodes degree")

    def build_vocab_(self, nodes_degree):
        """
        Build vocabulary from a sequence of paths (can be a once-only generator stream).
        Sorted by node id
        """
        # assign a unique index to each word
        self.vocab = {}

        for node_idx, (node, count) in enumerate(
                sorted(nodes_degree.items(), key=lambda x: x[0])):
            v = Vocab()
            v.count = count
            v.index = node_idx
            self.vocab[node] = v
        self.vocab_size = len(self.vocab)
        print(f"total {self.vocab_size} nodes")

    def precalc_sampling(self):
        """
        Peach vocabulary item's threshold for sampling
        """

        if self.down_sampling:
            print(
                f"frequent-node down sampling, threshold {self.down_sampling};"
                f" progress tallies will be approximate")
            total_nodes = sum(v.count for v in self.vocab.values())
            threshold_count = float(self.down_sampling) * total_nodes

        for v in self.vocab.values():
            prob = ((np.sqrt(v.count / threshold_count) + 1) *
                    (threshold_count / v.count) if self.down_sampling else 1.0)
            v.sample_probability = min(prob, 1.0)

    def reset_weights(self):
        """Reset all projection weights to an initial (untrained) state,
        but keep the existing vocabulary."""
        self.context_embedding = xavier_normal(size=(self.vocab_size,
                                                     self.layer1_size),
                                               as_type=np.float32)

        self.centroid = np.zeros((self.n_clusters, self.layer1_size),
                                 dtype=np.float32)
        self.covariance_mat = np.zeros(
            (self.n_clusters, self.layer1_size, self.layer1_size),
            dtype=np.float32)
        self.inv_covariance_mat = np.zeros(
            (self.n_clusters, self.layer1_size, self.layer1_size),
            dtype=np.float32)
        self.pi = np.zeros((self.vocab_size, self.n_clusters),
                           dtype=np.float32)

    def reset_communities_weights(self):
        """Reset all projection weights to an initial (untrained) state,
        but keep the existing vocabulary."""

        self.centroid = np.zeros((self.n_clusters, self.layer1_size),
                                 dtype=np.float32)
        self.covariance_mat = np.zeros(
            (self.n_clusters, self.layer1_size, self.layer1_size),
            dtype=np.float32)
        self.inv_covariance_mat = np.zeros(
            (self.n_clusters, self.layer1_size, self.layer1_size),
            dtype=np.float32)
        self.pi = np.zeros((self.vocab_size, self.n_clusters),
                           dtype=np.float32)
        print(f"reset communities data| k: {self.n_clusters}")

    def make_table(self, power=0.75):
        """
        Create a table using stored vocabulary word counts for drawing random words in the negative
        sampling training routines.

        Called internally from `build_vocab()`.

        """
        print(f"constructing a table with noise distribution "
              f"from {self.vocab_size} words of size {self.table_size}")
        # table (= list of words) of noise distribution for negative sampling
        self.table = np.zeros(self.table_size, dtype=np.uint32)
        sorted_keys = sorted(self.vocab.keys())
        k_idx = 0
        # compute sum of all power (Z in paper)
        train_words_pow = float(
            sum([v.count**power for k, v in self.vocab.items()]))
        # go through the whole table and fill it up with the word indexes proportional
        # to a word's count**power
        node_idx = sorted_keys[k_idx]
        # normalize count^0.75 by Z
        d1 = self.vocab[node_idx].count**power / train_words_pow
        for tidx in range(self.table_size):
            self.table[tidx] = self.vocab[node_idx].index
            if 1.0 * tidx / self.table_size > d1:
                k_idx += 1
                if k_idx > sorted_keys[-1]:
                    k_idx = sorted_keys[-1]
                node_idx = sorted_keys[k_idx]
                d1 += self.vocab[node_idx].count**power / train_words_pow

        print(f"Max value in the negative sampling table: {max(self.table)}")

    def fit(self):
        # Learning algorithm
        node_learner = Node2Vec(workers=self.num_workers,
                                negative=self.negative,
                                lr=self.lr)
        cont_learner = Context2Vec(
            window_size=self.window_size,
            workers=self.num_workers,
            negative=self.negative,
            lr=self.lr,
        )
        com_learner = Community2Vec(lr=self.lr)

        context_total_path = self.G.number_of_nodes(
        ) * self.num_walks * self.walk_length
        edges = np.array(list(self.G.edges()))
        print(f"context_total_path: {context_total_path}")
        print(f"node total edges: {self.G.number_of_edges()}")

        log.info("\n_______________________________________")
        log.info("\t\tPRE-TRAINING\n")
        ###########################
        #   PRE-TRAINING          #
        ###########################
        cont_learner.train(
            self,
            paths=combine_files_iter(self.walk_files),
            total_nodes=context_total_path,
            alpha=1,
            chunksize=self.batch_size,
        )
        ###########################
        #   EMBEDDING LEARNING    #
        ###########################
        iter_node = floor(context_total_path / self.G.number_of_edges() / 100)
        iter_com = floor(context_total_path / (self.G.number_of_edges()) / 100)
        for it in range(self.num_iter):
            alpha = self.alpha
            beta = self.beta
            print("\n_______________________________________\n")
            print(f"\t\tITER-{it}\n")
            print(f"k: {self.n_clusters}")
            self.reset_communities_weights()
            print(
                f"using alpha:{alpha}\tbeta:{beta}\titer_com:{iter_com}\titer_node: {iter_node}"
            )
            start_time = timeit.default_timer()
            com_learner.fit(self, reg_covar=self.reg_covar, n_init=10)

            log.info("Start training node embedding")
            node_learner.train(self,
                               edges=edges,
                               epochs=iter_node,
                               chunksize=self.batch_size)
            log.info("Stop training node embedding")

            log.info("Start training community embedding")
            com_learner.train(self.G.nodes(),
                              self,
                              beta,
                              chunksize=self.batch_size,
                              epochs=iter_com)
            log.info("Stop training community embedding")

            log.info("Start training context embedding")
            cont_learner.train(
                self,
                paths=combine_files_iter(self.walk_files),
                total_nodes=context_total_path,
                alpha=alpha,
                chunksize=self.batch_size,
            )
            log.info("Stop training context embedding")
            print(f"time: {timeit.default_timer() - start_time:.2f}s")
        self.predict = np.argmax(self.pi, axis=1)

    def get_memberships(self):
        return self.predict
