"""
Used for creating node embedding
"""
import logging as log
import threading
import time
from queue import Queue

import numpy as np

from ....module.pretrain.ComE.SDG_utils.training_sdg_inner import FAST_VERSION
from ....module.pretrain.ComE.SDG_utils.training_sdg_inner import train_o1
from ....utils.ComE_utils import chunkize_serial
from ....utils.ComE_utils import prepare_sentences
from ....utils.ComE_utils import RepeatCorpusNTimes

log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.DEBUG,
)
# print(f"imported cython version: {FAST_VERSION}")


class Node2Vec:
    """
    Create vector for node by using rand_walk path
    """

    def __init__(self, lr=0.2, workers=1, negative=0):
        self.workers = workers
        self.lr = float(lr)
        self.min_lr = 0.0001
        self.negative = negative
        self.window_size = 1

    def train(self, model, edges, chunksize=150, epochs=1):
        """
        Update the model's neural weights from a sequence of
        paths (can be a once-only generator stream).
        """
        assert model.node_embedding.dtype == np.float32

        print(
            f"""O1 training model with {self.workers} workers on {len(model.vocab)} vocabulary
                and {model.layer1_size} features and 'negative sampling'={self.negative}"""
        )

        if not model.vocab:
            raise RuntimeError(
                "you must first build vocabulary before training the model")

        edges = RepeatCorpusNTimes(edges, epochs)
        total_node = edges.corpus.shape[0] * edges.corpus.shape[1] * edges.n
        print(f"total edges: {total_node}")
        start, next_report, node_count = time.time(), [5.0], [0]

        # int(sum(v.count * v.sample_probability for v in self.vocab.values()))
        jobs = Queue(
            maxsize=2 *
            self.workers)  # buffer ahead only a limited number of jobs..
        # this is the reason we can't simply use ThreadPool :(
        lock = threading.Lock()

        def worker_train():
            """Train the model, lifting lists of paths from the jobs queue."""
            py_work = np.zeros(model.layer1_size, dtype=np.float32)

            while True:
                job = jobs.get(block=True)
                if job is None:  # data finished, exit
                    jobs.task_done()
                    # print('thread %s break' % threading.current_thread().name)
                    break

                lr = max(self.min_lr,
                         self.lr * (1 - 1.0 * node_count[0] / total_node))
                job_words = sum(
                    train_o1(
                        model.node_embedding,
                        edge,
                        lr,
                        self.negative,
                        model.table,
                        py_size=model.layer1_size,
                        py_work=py_work,
                    ) for edge in job if edge is not None)
                jobs.task_done()
                with lock:
                    node_count[0] += job_words

                    elapsed = time.time() - start
                    if elapsed >= next_report[0]:
                        print(
                            f"PROGRESS: at {100.0 * node_count[0] / total_node:.2f}%% "
                            f"\tnode_computed {node_count[0]}\talpha "
                            f"{lr:0.5f}\t {node_count[0] / elapsed if elapsed else 0.0:.0f}"
                            f" nodes/s")
                        next_report[0] = elapsed + 5.0  # don't flood the log,
                        # wait at least a second between progress reports
                # lock.acquire(timeout=30)
                # try:
                #     node_count[0] += job_words
                #
                #     elapsed = time.time() - start
                #     if elapsed >= next_report[0]:
                #         print(
                #             f"PROGRESS: at {100.0 * node_count[0] / total_node:.2f}%% "
                #             f"\tnode_computed {node_count[0]}\talpha "
                #             f"{lr:0.5f}\t {node_count[0] / elapsed if elapsed else 0.0:.0f}"
                #             f" nodes/s")
                #         next_report[
                #             0] = elapsed + 5.0  # don't flood the log,
                #         # wait at least a second between progress reports
                # finally:
                #     lock.release()

        workers = [
            threading.Thread(target=worker_train, name="thread_" + str(i))
            for i in range(self.workers)
        ]
        for thread in workers:
            thread.daemon = True  # make interrupting the process with ctrl+c easier
            thread.start()

        # convert input strings to Vocab objects (eliding OOV/downsampled words),
        # and start filling the jobs queue
        for _, job in enumerate(
                chunkize_serial(prepare_sentences(model, edges), chunksize)):
            jobs.put(job)

        for _ in range(self.workers):
            jobs.put(
                None
            )  # give the workers heads up that they can finish -- no more work!

        for thread in workers:
            thread.join()

        elapsed = time.time() - start
        print(f"training on {node_count[0]} words took {elapsed:0.1f}s,"
              f" {node_count[0] / elapsed if elapsed else 0.0:.0f} words/s")
