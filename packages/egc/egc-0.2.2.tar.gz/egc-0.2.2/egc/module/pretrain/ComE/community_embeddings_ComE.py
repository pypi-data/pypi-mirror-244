"""
Used for creating community embedding
"""
import logging as log

import numpy as np
import torch
from sklearn import mixture

from ....utils.ComE_utils import chunkize_serial

log.basicConfig(
    format="%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s",
    level=log.DEBUG,
)


class Community2Vec:
    """
    Class that train the community embedding
    """

    def __init__(self, lr):
        self.lr = lr
        self.g_mixture = None

    def fit(self, model, reg_covar=0, n_init=10):
        """
        Fit the GMM model with the current node embedding and save the result in the model
        :param model: model injected to add the mixture parameters
        """
        self.g_mixture = mixture.GaussianMixture(
            n_components=model.n_clusters,
            reg_covar=reg_covar,
            covariance_type="full",
            n_init=n_init,
        )

        print(f"Fitting: {model.n_clusters} communities")
        self.g_mixture.fit(model.node_embedding)

        model.centroid = self.g_mixture.means_.astype(np.float32)
        model.covariance_mat = self.g_mixture.covariances_.astype(np.float32)
        model.inv_covariance_mat = self.g_mixture.precisions_.astype(
            np.float32)
        model.pi = self.g_mixture.predict_proba(model.node_embedding).astype(
            np.float32)

    def train(self, nodes, model, beta, chunksize=150, epochs=1):
        for _ in range(epochs):
            # grad_input = np.zeros(model.node_embedding.shape).astype(
            #     np.float32)
            grad_input = torch.zeros(model.node_embedding.shape,
                                     dtype=torch.float32)
            if torch.cuda.is_available():
                grad_input = grad_input.cuda()
            for node_index in chunkize_serial(
                    map(
                        lambda node: model.vocab[node].index,
                        filter(
                            lambda node: node in model.vocab and
                            (model.vocab[node].sample_probability >= 1.0 or
                             model.vocab[node].sample_probability >= np.random.
                             random_sample()),
                            nodes,
                        ),
                    ),
                    chunksize,
            ):
                input_tensor = torch.FloatTensor(
                    model.node_embedding[node_index])
                # batch_grad_input = np.zeros(input.shape).astype(np.float32)
                batch_grad_input_tensor = torch.zeros(input_tensor.shape,
                                                      dtype=torch.float32)

                for com in range(model.n_clusters):
                    centroid_tensor = torch.FloatTensor(model.centroid[com])
                    diff_tensor = torch.unsqueeze(
                        input_tensor - centroid_tensor, -1)
                    pi_tensor_temp = torch.FloatTensor(model.pi[node_index,
                                                                com])
                    pi_tensor = pi_tensor_temp.reshape(len(node_index), 1, 1)
                    inv_covariance_mat_tensor = torch.FloatTensor(
                        model.inv_covariance_mat[com])
                    m_tensor = pi_tensor * inv_covariance_mat_tensor

                    if torch.cuda.is_available():
                        m_tensor = m_tensor.cuda()
                        diff_tensor = diff_tensor.cuda()
                        batch_grad_input_tensor = batch_grad_input_tensor.cuda(
                        )
                    batch_grad_input_tensor += torch.squeeze(
                        torch.matmul(m_tensor, diff_tensor), -1)

                    # diff = np.expand_dims(input - model.centroid[com], axis=-1)
                    # m = model.pi[node_index, com].reshape(
                    #     len(node_index), 1,
                    #     1) * (model.inv_covariance_mat[com])
                    #
                    # batch_grad_input += np.squeeze(np.matmul(m, diff), axis=-1)
                # grad_input[node_index] += batch_grad_input
                grad_input[node_index] += batch_grad_input_tensor
            grad_input *= beta / model.n_clusters

            model.node_embedding -= (np.array(grad_input.cpu()).clip(
                min=-0.25, max=0.25)) * self.lr
