import torch
import numpy as np

from .rbm_pytorch import RBM


# Class for the convolutional RBM model
class convolutional_RBM(RBM):

    def __init__(
        self,
        model_name,
        n_vis=784,
        n_hin=50,
        k=1,
        lr=0.01,
        max_epochs=200000,
        minMax_W=(-100, 100),
        energy_type='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
        batch_size=64,
        train_algo='CD',
        centering=False,
        average_data=None,
        sampling_model_beta=1,
        mytype=torch.double,
        half_kernel_size=1,
    ):
        # Initialize base class parameters
        super(convolutional_RBM, self).__init__(
            model_name,
            n_vis,
            n_vis,
            k,
            lr,
            max_epochs,
            minMax_W,
            energy_type,
            optimizer,
            regularization,
            l1_factor,
            l2_factor,
            ground_v,
            ground_h,
            batch_size,
            train_algo,
            centering,
            average_data,
            sampling_model_beta,
            mytype,
        )
        # Initialize new parameters
        self.half_kernel_size = half_kernel_size
        # self.W = self.W.to_sparse()

        # Create the adjacency matrix for each input data,
        # assuming that they are stored as row_i + N*column_j
        # * Note that we also assume closed boundaries
        self.nvis_sqrt = int(np.sqrt(self.n_visible))
        self.adjacency_mat = torch.zeros((n_vis, n_vis), device=self.device)
        for i in range(n_vis):
            column = int(np.floor(i / self.nvis_sqrt))
            row = int(i - self.nvis_sqrt * column)
            self.add_neigh(self.adjacency_mat, row, column)
        # self.adjacency_mat = self.adjacency_mat.to_sparse()

    def add_neigh(self, adjacency_mat, row, column):
        my_id = row + column * self.nvis_sqrt
        for i in range(row - self.half_kernel_size,
                       row + self.half_kernel_size + 1):
            for j in range(column - self.half_kernel_size,
                           column + self.half_kernel_size + 1):
                if i >= 0 and i < self.nvis_sqrt and j >= 0 and j < self.nvis_sqrt:
                    neigh_id = i + j * self.nvis_sqrt
                    adjacency_mat[my_id, neigh_id] = 1

    def after_step_keepup(self):
        if isinstance(self, convolutional_RBM):
            self.W = self.adjacency_mat * self.W

        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables()
        else:
            self.W_t = self.W.t()
