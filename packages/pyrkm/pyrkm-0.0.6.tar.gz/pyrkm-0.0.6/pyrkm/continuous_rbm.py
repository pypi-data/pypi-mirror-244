import torch
import glob
import pickle

from .rbm_pytorch import RBM


# Class for continuous RBM, used for CelebA
class continuous_RBM(RBM):

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
    ):
        # Initialize base class parameters
        super(continuous_RBM, self).__init__(
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
        self.logsigma_sq = torch.zeros((n_vis, ),
                                       dtype=self.mytype,
                                       device=self.device)

    def pretrain(self, pretrained_model):
        # Check if you have model load points
        filename_list = glob.glob(
            'model_states/{}_t*.pkl'.format(pretrained_model))
        if len(filename_list) > 0:
            all_loadpoints = sorted([
                int(x.split('_t')[-1].split('.pkl')[0]) for x in filename_list
            ])
            last_epoch = all_loadpoints[-1]
            print('** Using as pretraining model {} at epoch {}'.format(
                pretrained_model, last_epoch))
            with open(
                    'model_states/{}_t{}.pkl'.format(pretrained_model,
                                                     last_epoch),
                    'rb') as file:
                temp_model = pickle.load(file)
                # *** Import pretrained parameters
                self.W = temp_model.W.to(self.mytype)
                self.h_bias = temp_model.h_bias.to(self.mytype)
                self.v_bias = temp_model.v_bias.to(self.mytype)
                self.logsigma_sq = temp_model.logsigma_sq.to(self.mytype)
        else:
            print('** No load points for {}'.format(pretrained_model))

    def v_to_h(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        return self.GaussBernoulli_v_to_h(v, beta)

    def h_to_v(self, h, beta=None):
        if beta is None:
            beta = self.model_beta
        return self.GaussBernoulli_h_to_v(h, beta)

    def GaussBernoulli_v_to_h(self, v, beta):
        if self.energy_type == 'hopfield':
            p_h = self._prob_h_given_v(v / self.sigma_sq, beta)
        else:
            p_h = self._prob_h_given_v(v, beta)
        sample_h = torch.bernoulli(p_h)
        return p_h, sample_h

    def GaussBernoulli_h_to_v(self, h, beta):
        if self.energy_type == 'hopfield':
            mean = self.delta_ev(h)
            sample_v = mean + torch.randn_like(mean) * self.sigma
        else:
            mean = self.delta_ev(h) * self.sigma_sq
            sample_v = mean + torch.randn_like(mean) * self.sigma

        return None, sample_v

    def tstep_keepup(self):
        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables()
        else:
            self.W_t = self.W.t()
            self.sigma_sq = torch.exp(self.logsigma_sq)
            self.sigma = torch.sqrt(self.sigma_sq)

    def SGD_update(
        self,
        partial_gradient_data,
        partial_gradient_model,
    ):
        # Get the correct gradients
        dEdW_data = partial_gradient_data[0]
        dEdW_model = partial_gradient_model[0]
        dEdv_bias_data = partial_gradient_data[1]
        dEdv_bias_model = partial_gradient_model[1]
        dEdh_bias_data = partial_gradient_data[2]
        dEdh_bias_model = partial_gradient_model[2]
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        if self.energy_type == 'hopfield':
            dEds_data = partial_gradient_data[3]
            dEds_model = partial_gradient_model[3]
            ds = -dEds_data + dEds_model
        # Update parameters in-place
        # and clip
        if self.energy_type == 'hopfield':
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(
                dh) + torch.norm(ds)
        else:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(dh)
        myclip = (self.lr * 10.0) / gnorm if gnorm > 10 else self.lr
        self.W.add_(dW * myclip)
        self.v_bias.add_(dv * myclip)
        self.h_bias.add_(dh * myclip)
        if self.energy_type == 'hopfield':
            self.logsigma_sq.add_(ds * myclip)

    def generate(self,
                 n_samples,
                 k,
                 h_binarized=True,
                 from_visible=False,
                 beta=None):
        if beta is None:
            beta = self.model_beta
        self.tstep_keepup()
        if from_visible:
            # generate from continuous random visible
            v = torch.randn(size=(n_samples, self.n_visible),
                            device=self.device,
                            dtype=self.mytype)
        else:
            if h_binarized:
                h = torch.randint(
                    high=2,
                    size=(n_samples, self.n_hidden),
                    device=self.device,
                    dtype=self.mytype,
                )
            else:
                h = torch.rand(n_samples,
                               self.n_hidden,
                               device=self.device,
                               dtype=self.mytype)
            _, v = self.h_to_v(h)
        v_model = self.forward(v, k, beta)
        return v_model.detach().cpu().numpy()

    def _update_circuit_variables(self):
        self._k_pos = self.k_pos()
        self._k_neg = self.k_neg()
        self._v_bias_pos = self.v_bias_pos()
        self._v_bias_neg = self.v_bias_neg()
        self._h_bias_pos = self.h_bias_pos()
        self._h_bias_neg = self.h_bias_neg()
        self._k_diff = self._k_pos - self._k_neg
        self._k_diff_t = self._k_diff.t()
        self._v_bias_pos_diff = self._v_bias_pos * (0.5 - self.ground_v)
        self._v_bias_neg_diff = self._v_bias_neg * (0.5 - self.ground_v)
        self._h_bias_pos_diff = self._h_bias_pos * (0.5 - self.ground_h)
        self._h_bias_neg_diff = self._h_bias_neg * (0.5 - self.ground_h)
        self._vb_posneg = -self._v_bias_pos_diff + self._v_bias_neg_diff
        self._hb_posneg = -self._h_bias_pos_diff + self._h_bias_neg_diff
        # for the gaussian units
        self.sigma = torch.pow(
            self._k_pos.sum(0) + self._k_neg.sum(0) + self._v_bias_pos, -0.5)
        self.sigma_sq = self.sigma * self.sigma

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        v_diff = v - self.v_bias
        v_over_sigma = v / self.sigma_sq

        if self.centering:
            dEdW = -torch.einsum('ij,ik->ijk', h - self.oh,
                                 v - self.ov) / self.sigma_sq
        else:
            dEdW = -torch.einsum('ij,ik->ijk', h, v_over_sigma)
        dEdv_bias = -(v_diff) / self.sigma_sq
        dEdh_bias = -h
        # dEds = -( (v-self.v_bias)**2/self.sigma_sq.unsqueeze(0)*0.5 - torch.mm(h,self.W)*v/self.sigma_sq.unsqueeze(0))
        dEds = -0.5 * (v_diff**2) / self.sigma_sq + torch.mm(
            h, self.W) * v_over_sigma
        return (dEdW, dEdv_bias, dEdh_bias, dEds)

    def derivatives_linear_circuit_4(self, v, h):
        v_square = torch.square(v).unsqueeze(1)
        vneg_square = torch.square(1 - v).unsqueeze(1)

        h_square = torch.square(h).unsqueeze(2)
        hneg_square = torch.square(1 - h).unsqueeze(2)

        dEdk_pos = (-torch.einsum('ij,ik->ijk', h, v) + 0.5 * v_square + 0.5 *
                    h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, 1 - v) +
                                 0.5 * vneg_square + 0.5 * hneg_square)
        dEdk_neg = (-torch.einsum('ij,ik->ijk', h, 1 - v) + 0.5 * vneg_square +
                    0.5 * h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, v) +
                                       0.5 * v_square + 0.5 * hneg_square)

        dkdw_pos = self.dk_pos().unsqueeze(0)
        dkdw_neg = self.dk_neg().unsqueeze(0)

        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg

        dEdv_bias_pos = -self.ground_v * v + 0.5 * torch.square(v)
        dEdv_bias_neg = -self.ground_v * (1 - v) + 0.5 * torch.square(1 - v)

        dv_biasdv_pos = self.dv_bias_pos().unsqueeze(0)
        dv_biasdv_neg = self.dv_bias_neg().unsqueeze(0)

        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg
        dEdh_bias_pos = -self.ground_h * h + 0.5 * torch.square(h)
        dEdh_bias_neg = -self.ground_h * (1 - h) + 0.5 * torch.square(1 - h)

        dh_biasdh_pos = self.dh_bias_pos().unsqueeze(0)
        dh_biasdh_neg = self.dh_bias_neg().unsqueeze(0)
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg

        return (dEdW, dEdv_bias, dEdh_bias, None)
