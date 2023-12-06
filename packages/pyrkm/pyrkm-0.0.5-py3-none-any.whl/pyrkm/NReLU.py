import torch
import sys

from .rbm_pytorch import RBM


class NReLU(RBM):

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
        super(NReLU, self).__init__(
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
        print('ERROR: NReLU not fully implemented')
        sys.exit()

    def v_to_h(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            return self.Bernoulli_v_to_h(v, beta)
        else:
            if beta > 1000:
                # I assume we are at T=0
                return self.Deterministic_v_to_h(v, beta)
            else:
                return self.NReLU_v_to_h(v, beta)

    def h_to_v(self, h, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            return self.Bernoulli_h_to_v(h, beta)
        else:
            if beta > 1000:
                # I assume we are at T=0
                return self.Deterministic_h_to_v(h, beta)
            else:
                return self.NReLU_h_to_v(h, beta)

    def NReLU_v_to_h(self, v, beta):
        # out = max(0, x + N(0,sigma(x)))
        x = self.model_beta * self.delta_eh(v)
        activation = x + torch.sqrt(self.my_sigmoid(x)) * torch.randn(
            x.shape, device=self.device)
        sample_h = torch.clip(activation, 0, 1)
        return x, sample_h

    def NReLU_h_to_v(self, h, beta=1):
        x = self.model_beta * self.delta_ev(h)
        # activation = x + x.std()*torch.randn(x.shape, device=self.device)
        activation = x + torch.sqrt(self.my_sigmoid(x)) * torch.randn(
            x.shape, device=self.device)
        sample_v = torch.clip(activation, 0, 1)  # visible is binary
        return x, sample_v

    # The parameters of the 'diode'-sigmoid are hard coded
    def my_sigmoid(self, x, xscale=5, xshift=2.5):
        scaled_x = x * xscale
        shifted_x = scaled_x - xshift
        clipped_x = torch.clip(shifted_x, -10, 10)
        sigmoid_approx = (clipped_x + 10) / 20
        return sigmoid_approx
