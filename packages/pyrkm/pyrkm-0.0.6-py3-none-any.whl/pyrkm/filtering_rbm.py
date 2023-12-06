import torch
import torch.nn.init as init

from .rbm_pytorch import RBM


################################################################
# Class for the fitlering RBM model
class filtering_RBM(RBM):

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
        use_mask=False,
        mytype=torch.double,
        is_conditional=False,
    ):
        # Initialize base class parameters
        super(filtering_RBM, self).__init__(
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
        # If true, add conditional layer
        self.is_conditional = is_conditional
        # Initialize weights
        if is_conditional:
            self.D = torch.randn(
                (
                    n_hin,
                    n_vis,
                ),
                dtype=self.mytype,
                device=self.device,
            )
            self.D = self.D.contiguous()
            init.xavier_normal_(self.D)

        # use mask for recommendation systems
        self.use_mask = use_mask

    # Function to average the gradients, excluding the masked elements
    def maskedmean(self, x):
        mask_sum = (x != 0).to(torch.int).sum(dim=0)

        # Check if any element in mask_sum is zero
        if (mask_sum == 0).any():
            # print("Warning: Zero elements in mask_sum. Replacing with 1.")
            # Replace zero elements with 1 in mask_sum
            mask_sum = torch.where(mask_sum == 0, 1, mask_sum)

        return torch.div(x.sum(dim=0), mask_sum)

    def tstep_keepup(self):
        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables(self.is_conditional)
        else:
            self.W_t = self.W.t()
        if self.is_conditional:
            self.D_t = self.D.t()

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
        if self.is_conditional:
            self._D_pos = self.D_pos()
            self._D_neg = self.D_neg()
            self._D_diff = self._D_pos - self._D_neg
            self._D_diff_t = self._D_diff.t()

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
        if self.is_conditional:
            dEdD_data = partial_gradient_data[3]
            dEdD_model = partial_gradient_model[3]
            dD = -dEdD_data + dEdD_model
        if self.centering:
            dv = dv - torch.matmul(self.oh, dW)
            dh = dh - torch.matmul(self.ov, dW.t())
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * torch.sign(self.W)
            dv += self.l1 * torch.sign(self.v_bias)
            dh += self.l1 * torch.sign(self.h_bias)
        # Update parameters in-place
        # and clip
        if self.is_conditional:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(
                dh) + torch.norm(dD)
        else:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(dh)
        myclip = (self.lr * 10.0) / gnorm if gnorm > 10 else self.lr
        self.W.add_(myclip * dW)
        self.v_bias.add_(myclip * dv)
        self.h_bias.add_(myclip * dh)
        if self.is_conditional:
            self.D.add_(self.lr * dD * myclip)

    def delta_eh(self, v):
        if self.energy_type == 'hopfield':
            if self.use_mask:
                return self._delta_eh_hopfield_masked(v)
            else:
                return self._delta_eh_hopfield(v)
        elif self.energy_type == 'linear_circuit_4':
            if self.use_mask:
                return self._delta_eh_linear_circuit_4_masked(v)
            else:
                return self._delta_eh_linear_circuit_4(v)

    def delta_ev(self, h):
        if self.energy_type == 'hopfield':
            if self.use_mask:
                return self._delta_ev_hopfield_masked(h)
            else:
                return self._delta_ev_hopfield(h)
        elif self.energy_type == 'linear_circuit_4':
            if self.use_mask:
                return self._delta_ev_linear_circuit_4_masked(h)
            else:
                return self._delta_ev_linear_circuit_4(h)

    # **** Hopfield transfer functions
    def _delta_eh_hopfield(self, v):
        return torch.mm(v, self.W_t) + self.h_bias

    def _delta_ev_hopfield(self, h):
        return torch.mm(h, self.W) + self.v_bias

    # **** (masked) Hopfield transfer functions
    def _delta_eh_hopfield_masked(self, v):
        #        Wtm = self.W_t *self.mask.unsqueeze(-1)
        #        return torch.bmm(v.unsqueeze(1), Wtm).squeeze(1) + self.h_bias + torch.mm(self.mask , self.D_t)
        if self.is_conditional:
            return (torch.mm(v * self.mask, self.W_t) + self.h_bias +
                    torch.mm(self.mask, self.D_t))
        else:
            return torch.mm(v * self.mask, self.W_t) + self.h_bias

    def _delta_ev_hopfield_masked(self, h):
        return torch.mm(h, self.W) + self.v_bias

    # **** linear_circuit_4 transfer functions
    def _delta_ev_linear_circuit_4(self, h):
        return torch.mm(torch.mul(h, 2) - 1, self._k_diff) + self._vb_posneg

    def _delta_eh_linear_circuit_4(self, v):
        return torch.mm(torch.mul(v, 2) - 1, self._k_diff_t) + self._hb_posneg

    # **** (masked) linear_circuit_4 transfer functions
    def _delta_ev_linear_circuit_4_masked(self, h):
        return torch.mm(torch.mul(h, 2) - 1, self._k_diff) + self._vb_posneg

    def _delta_eh_linear_circuit_4_masked(self, v):
        if self.is_conditional:
            return (torch.mm(torch.mul(v * self.mask, 2) - 1, self._k_diff_t) +
                    self._hb_posneg +
                    torch.mm(torch.mul(self.mask, 2) - 1, self._D_diff_t))
        else:
            return (torch.mm(torch.mul(v * self.mask, 2) - 1, self._k_diff_t) +
                    self._hb_posneg)

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        if self.centering:
            dEdW = -torch.einsum('ij,ik->ijk', h - self.oh, v - self.ov)
        else:
            dEdW = -torch.einsum('ij,ik->ijk', h, v * self.mask)
        dEdv_bias = -v * self.mask
        dEdh_bias = -h
        if self.is_conditional:
            dEdD = -torch.einsum('ij,ik->ijk', h, self.mask)
        # They have to be renormalized according to the size of the mask
        # masksizefactor = self.n_visible/self.mask.sum(-1)
        if self.is_conditional:
            return (dEdW, dEdv_bias, dEdh_bias, dEdD)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, dEdD#*masksizefactor.unsqueeze(1).unsqueeze(1)
        else:
            return (dEdW, dEdv_bias, dEdh_bias, None)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, None

    def derivatives_linear_circuit_4(self, v, h):
        torch.square(v).unsqueeze(1)
        torch.square(1 - v).unsqueeze(1)
        negh = 1 - h
        h_square = torch.square(h).unsqueeze(2)
        hneg_square = torch.square(negh).unsqueeze(2)
        v_masked = v * self.mask
        negv_masked = 1 - v_masked
        v_square_masked = torch.square(v_masked).unsqueeze(1)
        vneg_square_masked = torch.square(1 - v_masked).unsqueeze(1)

        ein_h_vm = torch.einsum('ij,ik->ijk', h, v_masked)
        ein_negh_vm = torch.einsum('ij,ik->ijk', negh, v_masked)
        ein_h_negvm = torch.einsum('ij,ik->ijk', h, negv_masked)
        ein_negh_negvm = torch.einsum('ij,ik->ijk', negh, negv_masked)

        dEdk_pos = 0.5 * (
            (-2 * ein_h_vm + v_square_masked + h_square) +
            (-2 * ein_negh_negvm + vneg_square_masked + hneg_square))
        dEdk_neg = 0.5 * ((-2 * ein_h_negvm + vneg_square_masked + h_square) +
                          (-2 * ein_negh_vm + v_square_masked + hneg_square))
        dkdw_pos = self.dk_pos().unsqueeze(0)
        dkdw_neg = self.dk_neg().unsqueeze(0)
        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg

        dEdv_bias_pos = -self.ground_v * v_masked + 0.5 * torch.square(
            v_masked)
        dEdv_bias_neg = -self.ground_v * negv_masked + 0.5 * torch.square(
            negv_masked)
        dv_biasdv_pos = self.dv_bias_pos().unsqueeze(0)
        dv_biasdv_neg = self.dv_bias_neg().unsqueeze(0)
        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg

        dEdh_bias_pos = -self.ground_h * h + 0.5 * torch.square(h)
        dEdh_bias_neg = -self.ground_h * (negh) + 0.5 * torch.square(negh)
        dh_biasdh_pos = self.dh_bias_pos().unsqueeze(0)
        dh_biasdh_neg = self.dh_bias_neg().unsqueeze(0)
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg

        if self.is_conditional:
            ## No this gradient is wrong! (this is same shape as W, but it is not like this in C-RBM)
            negm = 1 - self.mask
            m_square = torch.square(self.mask).unsqueeze(1)
            mneg_square = torch.square(negm).unsqueeze(1)

            ein_h_m = torch.einsum('ij,ik->ijk', h, self.mask)
            ein_h_negm = torch.einsum('ij,ik->ijk', h, negm)
            ein_negh_m = torch.einsum('ij,ik->ijk', negh, self.mask)
            ein_negh_negm = torch.einsum('ij,ik->ijk', negh, negm)

            dEdD_pos = 0.5 * ((-2 * ein_h_m + m_square + h_square) +
                              (-2 * ein_negh_negm + mneg_square + hneg_square))
            dEdD_neg = 0.5 * ((-2 * ein_h_negm + mneg_square + h_square) +
                              (-2 * ein_negh_m + m_square + hneg_square))
            dDdw_pos = self.dD_pos().unsqueeze(0)
            dDdw_neg = self.dD_neg().unsqueeze(0)
            dEdD = dEdD_pos * dDdw_pos + dEdD_neg * dDdw_neg

            # negm = 1-self.mask
            # dEdD = torch.einsum('ij,ik->ijk',dEdh_bias_pos*dh_biasdh_pos, self.mask) + torch.einsum('ij,ik->ijk',dEdh_bias_neg*dh_biasdh_neg, negm)

        # They have to be renormalized according to the size of the mask
        # masksizefactor = self.n_visible/self.mask.sum(-1)
        if self.is_conditional:
            return (dEdW, dEdv_bias, dEdh_bias, dEdD)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, dEdD#*masksizefactor.unsqueeze(1).unsqueeze(1)
        else:
            return (dEdW, dEdv_bias, dEdh_bias, None)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, None

    # ***** Get high-level conditional weights
    def D_pos(self):
        return torch.relu(self.D)

    def D_neg(self):
        return torch.relu(-self.D)

    def dD_pos(self):
        return (self.D > 0).to(self.D.dtype)

    def dD_neg(self):
        return -(self.D < 0).to(self.D.dtype)
