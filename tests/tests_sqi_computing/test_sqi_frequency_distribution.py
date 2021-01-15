import pandas as pd
from ecg_qc.sqi_computing.sqi_frequency_distribution import pSQI, basSQI

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_pSQI(ecg_signal=ecg_signal, fs=fs):

    p_sqi_score = pSQI(ecg_signal, fs)

    assert isinstance(p_sqi_score, float)


def test_basSQI(ecg_signal=ecg_signal, fs=fs):

    bas_sqi_score = basSQI(ecg_signal, fs)

    assert isinstance(bas_sqi_score, float)
