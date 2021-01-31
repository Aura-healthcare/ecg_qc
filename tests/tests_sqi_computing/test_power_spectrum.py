import pandas as pd
from ecg_qc.sqi_computing.sqi_power_spectrum import psqi, bassqi

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_psqi(ecg_signal=ecg_signal, fs=fs):

    p_sqi_score = psqi(ecg_signal, fs)

    assert isinstance(p_sqi_score, float)


def test_bassqi(ecg_signal=ecg_signal, fs=fs):

    bas_sqi_score = bassqi(ecg_signal, fs)

    assert isinstance(bas_sqi_score, float)
