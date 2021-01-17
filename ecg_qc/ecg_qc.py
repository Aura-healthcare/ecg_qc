from joblib import load
from ecg_qc.sqi_computing.sqi_rr_intervals import csqi, qsqi
from ecg_qc.sqi_computing.sqi_power_spectrum import ssqi, ksqi
from ecg_qc.sqi_computing.sqi_frequency_distribution import bassqi, psqi
import os

import numpy as np
from tqdm.notebook import tqdm
import pywt
from tensorflow import keras


lib_path = os.path.dirname(__file__)


class ecg_qc:

    def __init__(self,
                 data_encoder='{}/ml/data_encoder/data_encoder.joblib'.format(
                     lib_path),
                 model_type='xgb',
                 sampling_frequency=1000):

        self.model_type = model_type

        if self.model_type == 'xgb':
            self.model = load('{}/ml/models/xgb.joblib'.format(lib_path))
        elif self.model_type == 'rfc':
            self.model = load('{}/ml/models/rfc.joblib'.format(lib_path))
        elif self.model_type == 'cnn':
            self.model = keras.models.load_model(
                '{}/ml/models/CNN_model_all_patients/CNN_model_all_patients/'.
                format(lib_path))

        self.data_encoder = load(data_encoder)
        self.sampling_frequency = sampling_frequency

    def compute_sqi_scores(self, ecg_signal: list) -> list:

        q_sqi_score = qsqi(ecg_signal, self.sampling_frequency)
        c_sqi_score = csqi(ecg_signal, self.sampling_frequency)

        s_sqi_score = ssqi(ecg_signal)
        k_sqi_score = ksqi(ecg_signal)

        p_sqi_score = psqi(ecg_signal, self.sampling_frequency)
        bas_sqi_score = bassqi(ecg_signal, self.sampling_frequency)

        sqi_scores = [[q_sqi_score, c_sqi_score, s_sqi_score,
                       k_sqi_score, p_sqi_score, bas_sqi_score]]

        return sqi_scores

    def predict_quality(self, sqi_scores: list) -> int:

        X = self.data_encoder.transform(sqi_scores)
        prediction = int(self.model.predict(X))
        return prediction

    def preprocessing(self, ecg_signal: list) -> list:
        waveletname = 'morl'
        signal = ecg_signal[:2000:8]  # we reduce the number of values by 8 :
        # signal of 2000 values to 250 values
        size_dataset = 1  # 1 seul signal est donnée en entrée
        fs = len(signal)
        scales = range(1, fs)
        X_prod = np.ndarray(shape=(size_dataset, fs-1, fs-1, 3))
        for j in tqdm(range(0, 3)):
            coeff, freq = pywt.cwt(signal, scales, waveletname, 1)
            X_prod[0, :, :, j] = coeff[:, :fs-1]
        return X_prod

    def get_signal_quality(self, ecg_signal) -> int:

        if self.model_type == 'rfc' or self.model_type == 'xgb':
            sqi_scores = self.compute_sqi_scores(ecg_signal)
            quality_predicted = self.predict_quality(sqi_scores)
        else:
            x = self.preprocessing(ecg_signal)
            quality_predicted = int(self.model.predict_classes(x))

        return quality_predicted
