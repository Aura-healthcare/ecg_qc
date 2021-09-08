from joblib import load
from ecg_qc.sqi_computing.sqi_rr_intervals import csqi, qsqi
from ecg_qc.sqi_computing.sqi_frequency_distribution import ssqi, ksqi
from ecg_qc.sqi_computing.sqi_power_spectrum import bassqi, psqi
from sklearn.preprocessing import StandardScaler
import os
import numpy as np

lib_path = os.path.dirname(__file__)


class EcgQc:

    def __init__(self,
                 model=f'{lib_path}/ml/models/xgb_9s.joblib',
                 sampling_frequency: int = 1000,
                 normalized: bool = False):

        self.model = load(model)
        self.sampling_frequency = sampling_frequency
        self.normalized = normalized

    def compute_sqi_scores(self,
                           ecg_signal: list) -> list:

        if self.normalized:
            ecg_signal = StandardScaler().fit_transform(
                ecg_signal.reshape(-1, 1)).reshape(1, -1)[0]
	
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
 
        sqi_scores = np.array(sqi_scores)
        prediction = int(self.model.predict(sqi_scores))
	    
        return prediction

    def get_signal_quality(self,
                           ecg_signal: list) -> int:

        sqi_scores = self.compute_sqi_scores(ecg_signal)
        quality_predicted = self.predict_quality(sqi_scores)

        return quality_predicted
