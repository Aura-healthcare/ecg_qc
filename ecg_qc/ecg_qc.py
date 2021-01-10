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

        qSQI_score = qSQI(ecg_signal, self.sampling_frequency)
        cSQI_score = cSQI(ecg_signal, self.sampling_frequency)

        sSQI_score = sSQI(ecg_signal)
        kSQI_score = kSQI(ecg_signal)

        pSQI_score = pSQI(ecg_signal, self.sampling_frequency)
        basSQI_score = basSQI(ecg_signal, self.sampling_frequency)

        sqi_scores = [[qSQI_score, cSQI_score, sSQI_score,
                       kSQI_score, pSQI_score, basSQI_score]]

        return sqi_scores

    def predict_quality(self, sqi_scores: list) -> int:
        X = self.data_encoder.transform(sqi_scores)
        prediction = int(self.model.predict(X))
        return prediction

    def get_signal_quality(self, ecg_signal):

        sqi_scores = self.compute_sqi_scores(ecg_signal)
        quality_predicted = self.predict_quality(sqi_scores)

        return quality_predicted
