from sklearn.decomposition import PCA
import numpy as np


class PCA:

    def __init__(self, data, method, n_comp):

        self.data = data
        self.method = method
        self.n_comp = n_comp

        # self.window = window
        # self.dates = dates
        # self.var_names = var_names
        # self._n_variables = data.shape[1]
        # self._n_windows = data.shape[0] - window + 1
        # self._pca_objects = []
        # self._data_list = []
        # self._dates_list = []
        # self._rolling_eigenvectors = []
        # self._multiplier = []


class PCARollingAnalysis(object):

    def __init__(self, data, window, dates=[], var_names=[]):
        self.data = data
        self.window = window
        self.dates = dates
        self.var_names = var_names
        self._n_variables = data.shape[1]
        self._n_windows = data.shape[0] - window + 1
        self._pca_objects = []
        self._data_list = []
        self._dates_list = []
        self._rolling_eigenvectors = []
        self._multiplier = []

    @property
    def n_variables(self):
        return self._n_variables

    @property
    def n_windows(self):
        return self._n_windows

    @property
    def pca_objects(self):
        return self._pca_objects

    @property
    def data_list(self):
        return self._data_list

    @property
    def dates_list(self):
        return self._dates_list

    @property
    def rolling_eigenvectors(self):
        return self._rolling_eigenvectors

    def _pca_aux(self, data_list):
        n_components = self.data.shape[1]
        pca = PCA(n_components)
        pca.fit(data_list)
        return pca

    def _adjusting_multiplier(self):
        n_rows = self._rolling_eigenvectors[0].shape[0]
        multiplier = np.ndarray(self._rolling_eigenvectors[0].shape)

        for i, ith_eig in enumerate(self._rolling_eigenvectors):
            aux = [np.dot(ith_eig[n_rows - 1], ith_eig[j]) for j in range(0, n_rows, 1)]
            id_ = [-1 if x < 0 else 1 for x in aux]
            multiplier[:, i] = np.array(id_)
            self._rolling_eigenvectors[i] = multiplier[:, i].reshape([n_rows, 1]) * self._rolling_eigenvectors[i]
        self._multiplier = multiplier

    def rolling_pca(self):
        n_rows = self.data.shape[0]
        self._data_list = [self.data[j - self.window:j, :] for j in range(self.window, n_rows + 1, 1)]
        self._dates_list = [self.dates[j - self.window:j] for j in range(self.window, n_rows + 1, 1)]
        self._pca_objects = list(map(self._pca_aux, self._data_list))
        self._rolling_eigenvectors = [np.vstack([x.components_[i] for x in self._pca_objects])
                                      for i in range(self.data.shape[1])]
        if len(self._data_list) > 1:
            self._adjusting_multiplier()

    def get_principal_components(self, pc_idx=(0, 1, 2), window_idx=-1):
        pca_obj = self._pca_objects[window_idx]
        data = self._data_list[window_idx]
        pc = pca_obj.transform(data)
        if len(self._multiplier) == 0:
            adjusted_pc = pc[:, pc_idx]
        else:
            aux_mult = self._multiplier[window_idx].reshape([1, data.shape[1]])
            adjusted_pc = aux_mult[:, pc_idx] * pc[:, pc_idx]
        # adjusted_pc = aux_mult[pc_idx] * pc[:, pc_idx]
        return adjusted_pc

    def get_eigenvectors(self, eig_idx=(0, 1, 2), window_idx=-1):
        """This method returns the eigenvectors for a particular window

        :param eig_idx: tuple of indices indicating which eigenvectors to return
        :param window_idx: window index (e.g. -1 is the last data window)
        :return: eigenvectors (each column is an eigenvector)
        """
        aux_eig = np.vstack([x[window_idx, :] for x in [self._rolling_eigenvectors[i] for i in eig_idx]])
        return aux_eig.T

    def get_rolling_explained_ratio(self, eig_idx=(0, 1, 2)):
        aux_explained = np.vstack([x.explained_variance_ratio_[list(eig_idx)] for x in self._pca_objects])
        return aux_explained

    def get_explained_ratio(self, eig_idx=(0, 1, 2), window_idx=-1):
        pca_obj = self._pca_objects[window_idx]
        aux_explained = pca_obj.explained_variance_ratio_[list(eig_idx)]
        return aux_explained

    def get_hedge_ratio(self, reference_idx, other_idx, window_idx=-1):
        n_eig = len(other_idx)
        pca_obj = self._pca_objects[window_idx]
        components = pca_obj.components_
        weights = np.matmul(np.linalg.inv(components[0:n_eig, other_idx]),
                            components[0:n_eig, reference_idx])
        return weights

    def get_weighted_spread(self, reference_idx, other_idx, window_idx=-1, use_all_data=False):
        weights = self.get_hedge_ratio(reference_idx, other_idx, window_idx)
        if use_all_data:
            data = self.data
        else:
            data = self._data_list[window_idx]
        spread = np.sum(data[:, other_idx] * weights, axis=1) - data[:, reference_idx]
        return spread

    def get_residual(self, factor_idx=0, window_idx=-1):
        """ Get residual
        """
        data = self._data_list[window_idx]
        idx = tuple(np.arange(0, factor_idx + 1))
        pc = self.get_principal_components(idx, window_idx)
        mean_ = self._pca_objects[window_idx].mean_
        eig_idx = tuple(range(0, self.n_variables))
        eig = self.get_eigenvectors(eig_idx, window_idx)
        eig_inv = np.linalg.inv(eig)
        pc_aux = pc.reshape([pc.shape[0], len(idx)])
        eig_inv_aux = eig_inv[idx, :].reshape([len(idx), self.n_variables])
        residual = data - (np.matmul(pc_aux[:, idx], eig_inv_aux) + mean_)
        return residual

    def get_rolling_residual(self, factor_idx=0):
        residual = [self.get_residual(factor_idx, x)[-1] for x in range(self.n_windows)]
        return residual

    def get_rolling_principal_components(self, pc_idx=(0, 1, 2)):
        principal_components = [self.get_principal_components(pc_idx, window_idx)[-1, :]
                                for window_idx in range(-1, -self.n_windows-1, -1)]
        principal_components = np.vstack(principal_components)
        principal_components = principal_components[range(-1, -self.n_windows-1, -1), :]
        return principal_components


