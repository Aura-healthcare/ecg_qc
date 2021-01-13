from joblib import load
from ecg_qc.sqi_computing.sqi_rr_intervals import cSQI, qSQI
from ecg_qc.sqi_computing.sqi_power_spectrum import sSQI, kSQI
from ecg_qc.sqi_computing.sqi_frequency_distribution import basSQI, pSQI
import os

lib_path = os.path.dirname(__file__)


class ecg_qc:

    def __init__(self,
                 data_encoder='{}/ml/data_encoder/data_encoder.joblib'.format(
                     lib_path),
                 model='{}/ml/models/xgb.joblib'.format(lib_path),
                 sampling_frequency=1000):

        self.data_encoder = load(data_encoder)
        self.model = load(model)
        self.sampling_frequency = sampling_frequency

    def compute_sqi_scores(self, ecg_signal: list) -> list:

        q_sqi_score = qSQI(ecg_signal, self.sampling_frequency)
        c_sqi_score = cSQI(ecg_signal, self.sampling_frequency)

        s_sqi_score = sSQI(ecg_signal)
        k_sqi_score = kSQI(ecg_signal)

        p_sqi_score = pSQI(ecg_signal, self.sampling_frequency)
        bas_sqi_score = basSQI(ecg_signal, self.sampling_frequency)

        sqi_scores = [[q_sqi_score, c_sqi_score, s_sqi_score,
                       k_sqi_score, p_sqi_score, bas_sqi_score]]

        return sqi_scores

    def predict_quality(self, sqi_scores: list) -> int:
        X = self.data_encoder.transform(sqi_scores)
        prediction = int(self.model.predict(X))
        return prediction

    def get_signal_quality(self, ecg_signal):

        sqi_scores = self.compute_sqi_scores(ecg_signal)
        quality_predicted = self.predict_quality(sqi_scores)

        return quality_predicted
