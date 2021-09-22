from ecg_qc.sqi_computing.sqi_rr_intervals import csqi, qsqi
from ecg_qc.sqi_computing.sqi_frequency_distribution import ssqi, ksqi
from ecg_qc.sqi_computing.sqi_power_spectrum import bassqi, psqi
from ecg_qc.utilities.type_checking import check_type_ecg
from ecg_qc.utilities.model_loader import load_model
from sklearn.preprocessing import StandardScaler
import numpy as np


class EcgQc:
    """
    This class determines the quality of an ECG segment, usually lasting
    several seconds. It computes SQIs (Signal Quality Indicator) and use them
    in a pre-trained model to predict the quality:
        * 1 : good quality
        * 0 : bad quality

    Attributes
    ----------
    model_file : str
        Trained model to load to predict quality. Can be the name of included
        pre-trained model or a path to an other model.
    sampling_frequency : int
        Sampling frequency of the input ECG signal. Used for several SQI
        computing
    normalized : bool
        If True, will normalise input ecg signal

    Methods
    -------
    compute_sqi_scores(ecg_signal)
        Computes SQIs from an ECG signal segment
    predict_quality(sqi_scores)
        From a list of SQIs, predict the quality of a related ECG segment
    get_signal_quality(ecg_signal)
        From an ECG signal segment, directly returns the quality
    """
    def __init__(self,
                 model_file='rfc_norm_2s.pkl',
                 sampling_frequency: int = 256,
                 normalized: bool = False):

        self.model = load_model(model_file)
        self.sampling_frequency = sampling_frequency
        self.normalized = normalized

    def compute_sqi_scores(self,
                           ecg_signal: list) -> list:
        """
        From an ECG Signal segment, computes 6 SQI scores (q_sqi, c_sqi, s_sqi,
        k_sqi, p_sqi, bas_sqi)

        Parameters
        ----------
        ecg_signal : list
            Input ECG signal

        Returns
        -------
        sqi_scores : list
            SQI scores related to input ECG segment
        """

        ecg_signal = check_type_ecg(ecg_signal)

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
        """
        From an ECG segment SQI scores, use pre-trained model to compute
        the quality of the signal.

        Parameters
        ----------
        sqi_scores : list(list)
            SQI scores related to input ECG segment

        Returns
        -------
        prediction : int
            The signal quality predicted by the model
        """
        sqi_scores = np.array(sqi_scores)
        prediction = int(self.model.predict(sqi_scores))

        return prediction

    def get_signal_quality(self,
                           ecg_signal: list) -> int:
        """
        From an ECG segment signal, use pre-trained model to compute
        the quality of the signal. This method is a shortcut to using
        compute_sqi_scores then predict quality.

        Parameters
        ----------
        ecg_signal : list
            Input ECG signal

        Returns
        -------
        prediction : int
            The signal quality predicted by the model
        """
        sqi_scores = self.compute_sqi_scores(ecg_signal)
        quality_predicted = self.predict_quality(sqi_scores)

        return quality_predicted
